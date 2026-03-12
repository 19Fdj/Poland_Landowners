from app.core.config import settings
from app.services.connectors.base import ParcelConnector
from app.services.connectors.demo_poland import DemoPolandParcelConnector
from app.services.connectors.uldk import ULDKParcelConnector


class FallbackParcelConnector(ParcelConnector):
    connector_name = "fallback_connector"

    def __init__(self, primary: ParcelConnector, fallback: ParcelConnector) -> None:
        self.primary = primary
        self.fallback = fallback

    def resolve(self, normalized_identifier: str):
        try:
            return self.primary.resolve(normalized_identifier)
        except Exception:
            return self.fallback.resolve(normalized_identifier)


def get_parcel_connector() -> ParcelConnector:
    demo = DemoPolandParcelConnector()
    uldk = ULDKParcelConnector(
        base_url=settings.uldk_base_url,
        timeout_seconds=settings.uldk_timeout_seconds,
    )
    if settings.parcel_connector == "demo":
        return demo
    if settings.parcel_connector == "uldk":
        return uldk
    return FallbackParcelConnector(primary=uldk, fallback=demo)
