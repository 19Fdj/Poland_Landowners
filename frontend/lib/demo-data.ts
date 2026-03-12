import type { AuditLog, DashboardData, Parcel } from "@/lib/types";

export const demoParcels: Parcel[] = [
  {
    id: 1,
    original_identifier: "141201_2.0003.45/6",
    normalized_identifier: "141201_2.0003.45/6",
    voivodeship: "mazowieckie",
    powiat: "powiat plocki",
    gmina: "Drobin",
    obreb: "0003",
    parcel_number: "45/6",
    kw_number: null,
    area_m2: 18234,
    land_use_classification: "RIIIb",
    centroid_lat: 52.7343,
    centroid_lon: 19.9894,
    bounding_box: { min_lon: 19.9879, min_lat: 52.7334, max_lon: 19.9911, max_lat: 52.7351 },
    pipeline_status: "enriched",
    notes: "Demo parcel seeded for local development.",
    observations: [
      {
        id: 101,
        source_name: "demo_polish_cadastre",
        source_type: "demo",
        field_name: "area_m2",
        field_value: "18234.0",
        confidence: 0.85,
        observed_at: "2026-03-12T09:00:00Z",
        source_reference: "Synthetic demo dataset"
      }
    ],
    ownership_records: [
      {
        id: 201,
        parcel_id: 1,
        owner_name: "Verified extract pending upload",
        owner_type: "unknown",
        source_type: "manual_verified",
        source_reference: "KW workflow link only. No personal data stored until evidence is uploaded.",
        verified_by: "analyst@example.com",
        verified_at: "2026-03-11T14:20:00Z",
        confidence: 0.2,
        lawful_basis_note: "Placeholder record without owner identity."
      }
    ],
    documents: [
      {
        id: 301,
        parcel_id: 1,
        document_type: "registry-link",
        file_name: "ekw.ms.gov.pl",
        file_path: "https://ekw.ms.gov.pl/",
        source_reference: "Public registry landing page",
        uploaded_by: "system"
      }
    ]
  },
  {
    id: 2,
    original_identifier: "301105_5.0012.144",
    normalized_identifier: "301105_5.0012.144",
    voivodeship: "wielkopolskie",
    powiat: "powiat slupecki",
    gmina: "Orchowo",
    obreb: "0012",
    parcel_number: "144",
    kw_number: "PO1S/00012345/7",
    area_m2: 41200,
    land_use_classification: "RIVa",
    centroid_lat: 52.5159,
    centroid_lon: 18.0392,
    bounding_box: { min_lon: 18.0381, min_lat: 52.5146, max_lon: 18.0402, max_lat: 52.5173 },
    pipeline_status: "ownership_verified",
    notes: "Ownership data stored from user-supplied extract.",
    observations: [
      {
        id: 102,
        source_name: "demo_polish_cadastre",
        source_type: "demo",
        field_name: "land_use_classification",
        field_value: "RIVa",
        confidence: 0.85,
        observed_at: "2026-03-12T09:00:00Z",
        source_reference: "Synthetic demo dataset"
      }
    ],
    ownership_records: [
      {
        id: 202,
        parcel_id: 2,
        owner_name: "Green Agro Sp. z o.o.",
        owner_type: "company",
        source_type: "user_supplied",
        source_reference: "Official extract uploaded on 2026-03-10",
        verified_by: "reviewer@example.com",
        verified_at: "2026-03-10T12:00:00Z",
        confidence: 0.9,
        lawful_basis_note: "B2B outreach preparation based on uploaded official extract."
      }
    ],
    documents: [
      {
        id: 302,
        parcel_id: 2,
        document_type: "extract",
        file_name: "kw_extract_demo.pdf",
        file_path: "/demo/kw_extract_demo.pdf",
        source_reference: "User-supplied official extract",
        uploaded_by: "reviewer@example.com"
      }
    ]
  }
];

export const demoDashboard: DashboardData = {
  kpis: [
    { label: "Parcels uploaded", value: 238 },
    { label: "Parcels resolved", value: 221, tone: "good" },
    { label: "Verified ownership", value: 47, tone: "good" },
    { label: "Failed lookups", value: 17, tone: "bad" }
  ],
  recentImports: [
    { id: 18, fileName: "Mazowieckie_batch_03.xlsx", status: "completed", processedRows: 1200, errorRows: 9 },
    { id: 17, fileName: "Farmland_pipeline.csv", status: "completed", processedRows: 430, errorRows: 2 }
  ],
  failedLookups: [
    { identifier: "141201_2.0003.bad", error: "Invalid parcel format" },
    { identifier: "000000_0.0000.0", error: "No demo source record found; fallback low confidence only" }
  ],
  legalDisclaimer:
    "Use only on a valid legal basis. Do not store personal data unless it comes from a lawful public source or user-supplied verified evidence."
};

export const demoAuditLogs: AuditLog[] = [
  {
    id: 1,
    user_email: "admin@example.com",
    action: "parcel.resolved",
    entity_type: "parcel",
    entity_id: "1",
    details: { source: "demo_polish_cadastre" },
    created_at: "2026-03-12T09:00:00Z"
  },
  {
    id: 2,
    user_email: "reviewer@example.com",
    action: "ownership.created",
    entity_type: "ownership_record",
    entity_id: "202",
    details: { parcel_id: 2 },
    created_at: "2026-03-12T10:20:00Z"
  }
];

