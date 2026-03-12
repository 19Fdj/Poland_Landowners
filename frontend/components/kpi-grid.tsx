import type { DashboardData } from "@/lib/types";

export function KPIGrid({ items }: { items: DashboardData["kpis"] }) {
  return (
    <section className="kpiGrid">
      {items.map((item) => (
        <article key={item.label} className={`kpiCard ${item.tone ?? "neutral"}`}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
        </article>
      ))}
    </section>
  );
}

