export type PipelineStatus =
  | "new"
  | "validated"
  | "enriched"
  | "ownership_pending"
  | "ownership_verified"
  | "outreach_ready"
  | "archived";

export type Parcel = {
  id: number;
  original_identifier: string;
  normalized_identifier: string;
  voivodeship: string | null;
  powiat: string | null;
  gmina: string | null;
  obreb: string | null;
  parcel_number: string | null;
  kw_number: string | null;
  area_m2: number | null;
  land_use_classification: string | null;
  centroid_lat: number | null;
  centroid_lon: number | null;
  bounding_box: Record<string, number> | null;
  pipeline_status: PipelineStatus;
  notes: string | null;
  observations: SourceObservation[];
  ownership_records: OwnershipRecord[];
  documents: DocumentRecord[];
};

export type SourceObservation = {
  id: number;
  source_name: string;
  source_type: string;
  field_name: string;
  field_value: string;
  confidence: number;
  observed_at: string;
  source_reference: string | null;
};

export type OwnershipRecord = {
  id: number;
  parcel_id: number;
  owner_name: string | null;
  owner_type: string;
  source_type: string;
  source_reference: string;
  verified_by: string | null;
  verified_at: string | null;
  confidence: number;
  lawful_basis_note: string;
};

export type DocumentRecord = {
  id: number;
  parcel_id: number | null;
  document_type: string;
  file_name: string;
  file_path: string;
  source_reference: string | null;
  uploaded_by: string | null;
};

export type DashboardData = {
  kpis: Array<{ label: string; value: number; tone?: "good" | "bad" | "neutral" }>;
  recentImports: Array<{ id: number; fileName: string; status: string; processedRows: number; errorRows: number }>;
  failedLookups: Array<{ identifier: string; error: string }>;
  legalDisclaimer: string;
};

export type AuditLog = {
  id: number;
  user_email: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
};

export type ParcelResolveResult = {
  original: string;
  valid: boolean;
  normalized: string | null;
  error: string | null;
  parcel: Parcel | null;
};
