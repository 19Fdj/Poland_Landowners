from dataclasses import dataclass
from typing import Protocol


@dataclass
class ParcelResolutionResult:
    normalized_identifier: str
    voivodeship: str | None
    powiat: str | None
    gmina: str | None
    obreb: str | None
    parcel_number: str | None
    area_m2: float | None
    land_use_classification: str | None
    centroid_lat: float | None
    centroid_lon: float | None
    bounding_box: dict[str, float] | None
    geometry_wkt: str | None
    source_name: str
    confidence: float
    source_reference: str


class ParcelConnector(Protocol):
    connector_name: str

    def resolve(self, normalized_identifier: str) -> ParcelResolutionResult: ...

