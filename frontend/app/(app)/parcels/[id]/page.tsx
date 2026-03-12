import Link from "next/link";
import { notFound } from "next/navigation";

import { ParcelMap } from "@/components/parcel-map";
import { getParcel } from "@/lib/api";

export default async function ParcelDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const parcel = await getParcel(id);

  if (!parcel) {
    notFound();
  }

  return (
    <>
      <section className="hero">
        <div className="stack">
          <p className="eyebrow">Parcel detail</p>
          <h1>{parcel.normalized_identifier}</h1>
          <p className="muted">
            {parcel.gmina}, {parcel.powiat}, {parcel.voivodeship}
          </p>
          <div className="buttonRow">
            <Link href="/dashboard" className="button secondary">Back to dashboard</Link>
            <a className="button" href="https://ekw.ms.gov.pl/" target="_blank" rel="noreferrer">
              Open registry search page
            </a>
          </div>
        </div>
        <div className="banner">
          <strong>Ownership workflow guardrail</strong>
          <p>
            Owner identity is shown only when backed by lawful public or user-supplied evidence. This screen never
            bypasses registry access controls.
          </p>
        </div>
      </section>

      <div className="detailGrid">
        <div className="stack">
          <div className="panel">
            <div className="panelHeader">
              <h2>Summary</h2>
            </div>
            <div className="list">
              <div className="listItem"><span>Area</span><span>{parcel.area_m2?.toLocaleString("en-US")} m2</span></div>
              <div className="listItem"><span>Land use</span><span>{parcel.land_use_classification ?? "Unknown"}</span></div>
              <div className="listItem"><span>Pipeline status</span><span>{parcel.pipeline_status}</span></div>
              <div className="listItem"><span>KW number</span><span>{parcel.kw_number ?? "Not stored"}</span></div>
            </div>
          </div>

          <div className="panel">
            <div className="panelHeader">
              <h2>Evidence timeline</h2>
            </div>
            <div className="timeline">
              {parcel.observations.map((observation) => (
                <div key={observation.id} className="timelineItem">
                  <strong>{observation.field_name}</strong>
                  <p>{observation.field_value}</p>
                  <p className="muted">
                    {observation.source_name} • confidence {Math.round(observation.confidence * 100)}%
                  </p>
                </div>
              ))}
              {parcel.documents.map((document) => (
                <div key={document.id} className="timelineItem">
                  <strong>{document.document_type}</strong>
                  <p>{document.file_name}</p>
                  <p className="muted">{document.source_reference ?? document.file_path}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="stack">
          <div className="panel">
            <div className="panelHeader">
              <h2>Map</h2>
            </div>
            <ParcelMap
              lat={parcel.centroid_lat}
              lon={parcel.centroid_lon}
              label={parcel.normalized_identifier}
            />
          </div>

          <div className="panel">
            <div className="panelHeader">
              <h2>Ownership panel</h2>
            </div>
            <div className="list">
              {parcel.ownership_records.map((record) => (
                <div key={record.id} className="listItem">
                  <span>
                    {record.owner_name ?? "Unnamed owner"} ({record.owner_type})
                  </span>
                  <span>{Math.round(record.confidence * 100)}%</span>
                </div>
              ))}
            </div>
            <p className="muted">{parcel.notes}</p>
          </div>
        </div>
      </div>
    </>
  );
}

