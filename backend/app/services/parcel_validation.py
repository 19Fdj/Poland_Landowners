import re

PARCEL_ID_PATTERN = re.compile(
    r"^(?P<terc>\d{6})_(?P<obr>\d\.\d{4})\.(?P<parcel>\d+(?:/\d+)?)$"
)


def normalize_parcel_identifier(value: str) -> str:
    compact = value.strip().replace(" ", "")
    return compact.upper()


def validate_parcel_identifier(value: str) -> list[str]:
    normalized = normalize_parcel_identifier(value)
    errors: list[str] = []
    if len(normalized) > 128:
        errors.append("Identifier is too long.")
    if "_" not in normalized or "." not in normalized:
        errors.append("Identifier must include TERC, obręb, and parcel segments.")
    if not PARCEL_ID_PATTERN.match(normalized):
        errors.append(
            "Expected format like 141201_2.0003.45/6 (TERC_obreb.parcel-number)."
        )
    return errors

