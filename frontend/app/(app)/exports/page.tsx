export default function ExportsPage() {
  return (
    <>
      <section className="hero">
        <div className="stack">
          <p className="eyebrow">Export center</p>
          <h1>Deliver CSV, XLSX, or GeoJSON outputs</h1>
          <p className="muted">
            Export enriched parcel records with provenance metadata, job tracking, and legal-use warnings embedded in the workflow.
          </p>
        </div>
        <div className="banner">
          <strong>Export warning</strong>
          <p>Review data minimization before exporting ownership-related fields outside the internal team.</p>
        </div>
      </section>

      <section className="panel">
        <div className="panelHeader">
          <h2>Available exports</h2>
        </div>
        <div className="list">
          <div className="listItem"><span>Enriched parcels CSV</span><span>Completed</span></div>
          <div className="listItem"><span>GeoJSON for GIS review</span><span>Queued</span></div>
        </div>
      </section>
    </>
  );
}

