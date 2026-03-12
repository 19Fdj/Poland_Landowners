import { getAuditLogs } from "@/lib/api";

export default async function AdminPage() {
  const auditLogs = await getAuditLogs();

  return (
    <>
      <section className="hero">
        <div className="stack">
          <p className="eyebrow">Admin console</p>
          <h1>Manage controls and review audit history</h1>
          <p className="muted">
            Source connectors, throttling, legal disclaimers, failed imports, and access logs are administered here.
          </p>
        </div>
        <div className="banner">
          <strong>Privacy note</strong>
          <p>Access logs should be retained according to internal GDPR retention settings and reviewed regularly.</p>
        </div>
      </section>

      <div className="detailGrid">
        <section className="panel">
          <div className="panelHeader">
            <h2>Connector settings</h2>
          </div>
          <div className="list">
            <div className="listItem"><span>Demo Polish cadastre connector</span><span>Active</span></div>
            <div className="listItem"><span>Retry policy</span><span>3 attempts with exponential backoff</span></div>
            <div className="listItem"><span>Rate limit</span><span>5 req/s per source</span></div>
          </div>
        </section>

        <section className="panel">
          <div className="panelHeader">
            <h2>Audit log</h2>
          </div>
          <div className="list">
            {auditLogs.map((log) => (
              <div key={log.id} className="listItem">
                <span>{log.action}</span>
                <span>{log.user_email ?? "system"}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}

