from app.services.parcel_validation import normalize_parcel_identifier, validate_parcel_identifier


def test_normalize_parcel_identifier() -> None:
    assert normalize_parcel_identifier(" 141201_2.0003.45/6 ") == "141201_2.0003.45/6"


def test_validate_parcel_identifier_accepts_expected_format() -> None:
    assert validate_parcel_identifier("141201_2.0003.45/6") == []


def test_validate_parcel_identifier_rejects_bad_format() -> None:
    errors = validate_parcel_identifier("bad-id")
    assert errors

