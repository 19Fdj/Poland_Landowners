import Link from "next/link";

import { KPIGrid } from "@/components/kpi-grid";
import { ParcelTable } from "@/components/parcel-table";
import { getDashboardData, getParcels } from "@/lib/api";

export default async function DashboardPage() {
  const [dashboard, parcels] = await Promise.all([getDashboardData(), getParcels()]);

  return (
    <>
      <section className="hero">
        <div className="stack">
          <p className="eyebrow">Production-ready MVP</p>
          <h1>Turn parcel IDs into lawful diligence records</h1>
          <p className="muted">
            Validate cadastral identifiers, enrich parcels through connector-based public sources, and maintain a
            strict evidence trail for any ownership-related data.
          </p>
          <div className="buttonRow">
            <Link href="/imports" className="button">Bulk import parcels</Link>
            <Link href="/exports" className="button secondary">Review exports</Link>
          </div>
        </div>
        <div className="banner">
          <strong>Legal disclaimer</strong>
          <p>{dashboard.legalDisclaimer}</p>
        </div>
      </section>

      <KPIGrid items={dashboard.kpis} />

      <div className="detailGrid">
        <div className="panel">
          <div className="panelHeader">
            <h2>Recent imports</h2>
          </div>
          <div className="list">
            {dashboard.recentImports.map((item) => (
              <div key={item.id} className="listItem">
                <span>{item.fileName}</span>
                <span>{item.processedRows} rows, {item.errorRows} errors</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panelHeader">
            <h2>Failed lookups</h2>
          </div>
          <div className="list">
            {dashboard.failedLookups.map((item) => (
              <div key={item.identifier} className="listItem">
                <span>{item.identifier}</span>
                <span>{item.error}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <ParcelTable parcels={parcels} />
    </>
  );
}

