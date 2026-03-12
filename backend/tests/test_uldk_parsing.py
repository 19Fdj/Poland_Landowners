from app.services.connectors.uldk import normalize_label, parse_dzinfo_html
from app.services.parcel_validation import validate_parcel_identifier


def test_parse_dzinfo_html_extracts_public_fields() -> None:
    html = """
    <table>
      <tr><td>Powiat</td><td>powiat plocki</td></tr>
      <tr><td>Gmina</td><td>Drobin</td></tr>
      <tr><td>Obręb</td><td>0003</td></tr>
      <tr><td>Numer działki</td><td>45/6</td></tr>
      <tr><td>Pole pow. w ewidencji gruntów (ha)</td><td>1,8234</td></tr>
      <tr><td>Oznaczenie użytku</td><td>RIIIb</td></tr>
      <tr><td>Oznaczenie konturu</td><td>R</td></tr>
    </table>
    """
    parsed = parse_dzinfo_html(html)
    assert parsed["powiat"] == "powiat plocki"
    assert parsed["gmina"] == "Drobin"
    assert parsed["parcel_number"] == "45/6"
    assert parsed["area_ha"] == "1,8234"


def test_normalize_label_collapses_whitespace() -> None:
    assert normalize_label("  Numer   działki : ") == "Numer działki"


def test_validate_parcel_identifier_accepts_arkusz_format() -> None:
    assert validate_parcel_identifier("246901_1.0004.AR_10.351/215") == []
