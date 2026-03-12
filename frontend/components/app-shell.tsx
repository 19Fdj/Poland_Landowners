import Link from "next/link";
import { ReactNode } from "react";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/imports", label: "Imports" },
  { href: "/exports", label: "Exports" },
  { href: "/admin", label: "Admin" }
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Renewables land origination</p>
          <h1>Poland Rural Landowner Finder</h1>
          <p className="muted">
            Internal diligence only. Ownership workflows must rely on lawful public or user-supplied evidence.
          </p>
        </div>
        <nav className="nav">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="navLink">
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="sidebarCard">
          <strong>Compliance guardrails</strong>
          <p className="muted">
            No CAPTCHA bypassing. No paywall evasion. No private personal data scraping.
          </p>
        </div>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}

