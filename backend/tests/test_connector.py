from app.services.connectors.demo_poland import DemoPolandParcelConnector


def test_demo_connector_returns_seeded_result() -> None:
    connector = DemoPolandParcelConnector()
    result = connector.resolve("141201_2.0003.45/6")
    assert result.voivodeship == "mazowieckie"
    assert result.area_m2 == 18234.0
