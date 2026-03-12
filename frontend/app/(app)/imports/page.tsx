export default function ImportsPage() {
  return (
    <>
      <section className="hero">
        <div className="stack">
          <p className="eyebrow">Bulk import wizard</p>
          <h1>Load parcel identifiers at portfolio scale</h1>
          <p className="muted">
            Supports single input, bulk paste, CSV/XLSX upload, per-row validation, deduplication, and asynchronous enrichment jobs.
          </p>
        </div>
        <div className="banner">
          <strong>Import compliance</strong>
          <p>Only import ownership-related columns if they come from lawful public or user-supplied records.</p>
        </div>
      </section>

      <section className="panel">
        <div className="panelHeader">
          <h2>Import template</h2>
        </div>
        <div className="importGrid">
          <div className="field">
            <label htmlFor="project">Project name</label>
            <input id="project" placeholder="Mazowieckie solar tranche" />
          </div>
          <div className="field">
            <label htmlFor="tags">Tags</label>
            <input id="tags" placeholder="solar, 2026, priority-a" />
          </div>
          <div className="field">
            <label htmlFor="paste">Manual batch paste</label>
            <textarea id="paste" defaultValue={"141201_2.0003.45/6\n301105_5.0012.144"} />
          </div>
          <div className="field">
            <label htmlFor="file">CSV/XLSX upload</label>
            <input id="file" type="file" />
            <p className="muted">Expected column: `identifier`. Optional: `project_name`, `tags`.</p>
          </div>
        </div>
      </section>
    </>
  );
}

