from __future__ import annotations

import json
from pathlib import Path

from app.services.connectors.base import ParcelConnector, ParcelResolutionResult


class DemoPolandParcelConnector(ParcelConnector):
    connector_name = "demo_polish_cadastre"

    def __init__(self) -> None:
        data_path = Path(__file__).resolve().parents[4] / "seeds" / "demo_parcels.json"
        with data_path.open("r", encoding="utf-8") as file_obj:
            self._data = {item["normalized_identifier"]: item for item in json.load(file_obj)}

    def resolve(self, normalized_identifier: str) -> ParcelResolutionResult:
        if normalized_identifier not in self._data:
            terc = normalized_identifier[:2]
            voivodeship = {
                "14": "mazowieckie",
                "30": "wielkopolskie",
                "12": "małopolskie",
            }.get(terc, "unknown")
            return ParcelResolutionResult(
                normalized_identifier=normalized_identifier,
                voivodeship=voivodeship,
                powiat="demo-powiat",
                gmina="demo-gmina",
                obreb=normalized_identifier.split("_", maxsplit=1)[1].split(".", maxsplit=1)[0],
                parcel_number=normalized_identifier.rsplit(".", maxsplit=1)[1],
                area_m2=10000.0,
                land_use_classification="RIVa",
                centroid_lat=52.2297,
                centroid_lon=21.0122,
                bounding_box={"min_lon": 21.0, "min_lat": 52.22, "max_lon": 21.02, "max_lat": 52.24},
                geometry_wkt=(
                    "MULTIPOLYGON(((21.0 52.22,21.02 52.22,21.02 52.24,21.0 52.24,21.0 52.22)))"
                ),
                source_name=self.connector_name,
                confidence=0.55,
                source_reference="Demo fallback dataset for local development",
            )

        item = self._data[normalized_identifier]
        return ParcelResolutionResult(
            normalized_identifier=normalized_identifier,
            voivodeship=item["voivodeship"],
            powiat=item["powiat"],
            gmina=item["gmina"],
            obreb=item["obreb"],
            parcel_number=item["parcel_number"],
            area_m2=item["area_m2"],
            land_use_classification=item["land_use_classification"],
            centroid_lat=item["centroid_lat"],
            centroid_lon=item["centroid_lon"],
            bounding_box=item["bounding_box"],
            geometry_wkt=item["geometry_wkt"],
            source_name=self.connector_name,
            confidence=0.85,
            source_reference=item["source_reference"],
        )

