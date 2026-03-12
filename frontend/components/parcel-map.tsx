"use client";

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";

type Props = {
  lat: number | null;
  lon: number | null;
  label: string;
};

export function ParcelMap({ lat, lon, label }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current || lat === null || lon === null) {
      return;
    }

    const map = new maplibregl.Map({
      container: containerRef.current,
      style:
        process.env.NEXT_PUBLIC_MAP_STYLE_URL ?? "https://demotiles.maplibre.org/style.json",
      center: [lon, lat],
      zoom: 13
    });

    new maplibregl.Marker({ color: "#1b5e20" }).setLngLat([lon, lat]).setPopup(
      new maplibregl.Popup({ closeButton: false }).setHTML(`<strong>${label}</strong>`)
    ).addTo(map);

    return () => map.remove();
  }, [label, lat, lon]);

  return <div ref={containerRef} className="mapPanel" aria-label="Parcel map" />;
}

