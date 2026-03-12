import { demoAuditLogs, demoDashboard, demoParcels } from "@/lib/demo-data";
import type { AuditLog, DashboardData, Parcel } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        Authorization: "Bearer demo-token"
      },
      cache: "no-store"
    });
    if (!response.ok) {
      return fallback;
    }
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getDashboardData(): Promise<DashboardData> {
  return demoDashboard;
}

export async function getParcels(): Promise<Parcel[]> {
  const response = await fetchJson<{ items: Parcel[] }>("/parcels", { items: demoParcels });
  return response.items;
}

export async function getParcel(parcelId: string): Promise<Parcel | undefined> {
  return fetchJson<Parcel | undefined>(`/parcels/${parcelId}`, demoParcels.find((item) => `${item.id}` === parcelId));
}

export async function getAuditLogs(): Promise<AuditLog[]> {
  return fetchJson<AuditLog[]>("/admin/audit-logs", demoAuditLogs);
}

