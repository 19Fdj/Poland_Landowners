from __future__ import annotations

import re
from collections.abc import Callable
from html import unescape
from urllib.parse import quote_plus

import httpx
from pyproj import Transformer
from shapely import ops, wkb
from shapely.geometry.base import BaseGeometry

from app.models import SourceType
from app.services.connectors.base import ParcelConnector, ParcelResolutionResult

ULDK_STATUS_OK = "0"
VOIVODESHIP_BY_CODE = {
    "02": "dolnośląskie",
    "04": "kujawsko-pomorskie",
    "06": "lubelskie",
    "08": "lubuskie",
    "10": "łódzkie",
    "12": "małopolskie",
    "14": "mazowieckie",
    "16": "opolskie",
    "18": "podkarpackie",
    "20": "podlaskie",
    "22": "pomorskie",
    "24": "śląskie",
    "26": "świętokrzyskie",
    "28": "warmińsko-mazurskie",
    "30": "wielkopolskie",
    "32": "zachodniopomorskie",
}
DETAIL_LABELS = {
    "powiat": "powiat",
    "gmina": "gmina",
    "obręb": "obreb_name",
    "obr\u0119b": "obreb_name",
    "numer działki": "parcel_number",
    "numer dzia\u0142ki": "parcel_number",
    "pole pow. w ewidencji gruntów (ha)": "area_ha",
    "pole pow. w ewidencji gruntow (ha)": "area_ha",
    "oznaczenie użytku": "land_use_classification",
    "oznaczenie u\u017cytku": "land_use_classification",
    "oznaczenie konturu": "land_use_contour",
}


class ULDKConnectorError(RuntimeError):
    pass


class ULDKParcelConnector(ParcelConnector):
    connector_name = "gugik_uldk"

    def __init__(
        self,
        *,
        base_url: str,
        timeout_seconds: float = 20.0,
        client_factory: Callable[[], httpx.Client] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._client_factory = client_factory or self._default_client_factory
        self._to_wgs84 = Transformer.from_crs("EPSG:2180", "EPSG:4326", always_xy=True)

    def _default_client_factory(self) -> httpx.Client:
        return httpx.Client(timeout=self.timeout_seconds, follow_redirects=True)

    def resolve(self, normalized_identifier: str) -> ParcelResolutionResult:
        with self._client_factory() as client:
            geometry_2180 = self._fetch_geometry(client, normalized_identifier)
            geometry_4326 = ops.transform(self._to_wgs84.transform, geometry_2180)
            details = self._fetch_details(client, normalized_identifier)

        centroid = geometry_4326.centroid
        min_lon, min_lat, max_lon, max_lat = geometry_4326.bounds
        parcel_number = details.get("parcel_number") or normalized_identifier.rsplit(".", maxsplit=1)[-1]
        area_ha = self._coerce_float(details.get("area_ha"))
        land_use = self._combine_land_use(
            details.get("land_use_classification"), details.get("land_use_contour")
        )
        return ParcelResolutionResult(
            normalized_identifier=normalized_identifier,
            voivodeship=VOIVODESHIP_BY_CODE.get(normalized_identifier[:2]),
            powiat=details.get("powiat"),
            gmina=details.get("gmina"),
            obreb=details.get("obreb_name") or normalized_identifier.split("_", maxsplit=1)[1].split(".", maxsplit=1)[0],
            parcel_number=parcel_number,
            area_m2=(area_ha * 10000.0) if area_ha is not None else float(geometry_2180.area),
            land_use_classification=land_use,
            centroid_lat=centroid.y,
            centroid_lon=centroid.x,
            bounding_box={
                "min_lon": min_lon,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "max_lat": max_lat,
            },
            geometry_wkt=geometry_4326.wkt,
            source_name=self.connector_name,
            source_type=SourceType.OFFICIAL_PUBLIC,
            confidence=0.9,
            source_reference=(
                f"{self.base_url}/?request=GetParcelById&id={quote_plus(normalized_identifier)}"
            ),
        )

    def _fetch_geometry(self, client: httpx.Client, normalized_identifier: str) -> BaseGeometry:
        response = client.get(
            f"{self.base_url}/",
            params={"request": "GetParcelById", "id": normalized_identifier},
        )
        response.raise_for_status()
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        if not lines or lines[0] != ULDK_STATUS_OK:
            raise ULDKConnectorError(
                f"ULDK parcel geometry lookup failed for {normalized_identifier}: {response.text[:200]}"
            )
        if len(lines) < 2:
            raise ULDKConnectorError(f"ULDK returned no geometry for {normalized_identifier}")
        return wkb.loads(bytes.fromhex(lines[1]))

    def _fetch_details(self, client: httpx.Client, normalized_identifier: str) -> dict[str, str]:
        response = client.get(
            f"{self.base_url}/dzinfo.php",
            params={"dzialka": normalized_identifier},
        )
        response.raise_for_status()
        return parse_dzinfo_html(response.text)

    @staticmethod
    def _coerce_float(value: str | None) -> float | None:
        if value is None:
            return None
        normalized = value.replace(" ", "").replace(",", ".")
        try:
            return float(normalized)
        except ValueError:
            return None

    @staticmethod
    def _combine_land_use(classification: str | None, contour: str | None) -> str | None:
        parts = [part for part in [classification, contour] if part]
        if not parts:
            return None
        return " / ".join(parts)


def parse_dzinfo_html(html: str) -> dict[str, str]:
    text = unescape(re.sub(r"<[^>]+>", "\n", html))
    lines = [normalize_label(line) for line in text.splitlines()]
    values = [line for line in lines if line]

    parsed: dict[str, str] = {}
    for index, line in enumerate(values):
        key = DETAIL_LABELS.get(line.lower())
        if key is None or index + 1 >= len(values):
            continue
        parsed[key] = values[index + 1]
    return parsed


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" :\t\r\n")
