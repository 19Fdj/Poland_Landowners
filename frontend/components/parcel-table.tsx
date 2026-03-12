import Link from "next/link";

import type { Parcel } from "@/lib/types";

export function ParcelTable({ parcels }: { parcels: Parcel[] }) {
  return (
    <div className="panel">
      <div className="panelHeader">
        <h2>Parcel portfolio</h2>
        <p className="muted">Search-ready parcel records with source attribution and ownership workflow state.</p>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Identifier</th>
            <th>Admin unit</th>
            <th>Area</th>
            <th>Status</th>
            <th>Ownership</th>
          </tr>
        </thead>
        <tbody>
          {parcels.map((parcel) => (
            <tr key={parcel.id}>
              <td>
                <Link href={`/parcels/${parcel.id}`}>{parcel.normalized_identifier}</Link>
              </td>
              <td>{parcel.gmina}, {parcel.voivodeship}</td>
              <td>{parcel.area_m2?.toLocaleString("en-US")} m2</td>
              <td><span className="pill">{parcel.pipeline_status.replaceAll("_", " ")}</span></td>
              <td>{parcel.ownership_records[0]?.owner_type ?? "unknown"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

