"use client";

import type { Route } from "next";
import Link from "next/link";
import type { ChangeEvent } from "react";
import { useMemo, useState } from "react";

import type { Parcel, ParcelResolveResult } from "@/lib/types";

type Props = {
  parcels: Parcel[];
  title?: string;
  compact?: boolean;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export function ParcelSearchPanel({
  parcels,
  title = "Parcel search",
  compact = false
}: Props) {
  const [singleValue, setSingleValue] = useState("");
  const [bulkValue, setBulkValue] = useState("");
  const [results, setResults] = useState<ParcelResolveResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<"search" | "validate">("search");

  const parcelByIdentifier = useMemo(
    () => new Map(parcels.map((parcel) => [parcel.normalized_identifier, parcel])),
    [parcels]
  );

  async function resolveIdentifiers(values: string[], nextMode: "search" | "validate") {
    setLoading(true);
    setError(null);
    setMode(nextMode);
    try {
      const endpoint = nextMode === "search" ? "/parcels/resolve" : "/parcels/validate";
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(
          values.map((value) =>
            nextMode === "search" ? { identifier: value } : { value }
          )
        )
      });

      if (!response.ok) {
        throw new Error("The validation service is unavailable right now.");
      }

      const payload = (await response.json()) as
        | ParcelResolveResult[]
        | Array<{ original: string; normalized: string | null; valid: boolean; errors: string[] }>;
      if (nextMode === "search") {
        setResults(payload as ParcelResolveResult[]);
      } else {
        setResults(
          (payload as Array<{ original: string; normalized: string | null; valid: boolean; errors: string[] }>).map(
            (item) => ({
              original: item.original,
              normalized: item.normalized,
              valid: item.valid,
              error: item.errors.join(" "),
              parcel: null
            })
          )
        );
      }
    } catch (caughtError) {
      const message =
        caughtError instanceof Error
          ? caughtError.message
          : "Unexpected validation error.";
      setError(message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleSingleSearch() {
    const value = singleValue.trim();
    if (!value) {
      setError("Enter at least one parcel identifier.");
      setResults([]);
      return;
    }
    await resolveIdentifiers([value], "search");
  }

  async function handleBulkValidate() {
    const values = splitIdentifiers(bulkValue);
    if (!values.length) {
      setError("Paste one or more parcel identifiers to validate.");
      setResults([]);
      return;
    }
    await resolveIdentifiers(values, "validate");
  }

  async function handleBulkSearch() {
    const values = splitIdentifiers(bulkValue);
    if (!values.length) {
      setError("Paste one or more parcel identifiers to search.");
      setResults([]);
      return;
    }
    await resolveIdentifiers(values, "search");
  }

  async function handleFileUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    const text = await file.text();
    const values = splitIdentifiers(text);
    setBulkValue(values.join("\n"));
    if (values.length) {
      await resolveIdentifiers(values, "validate");
    } else {
      setError("No parcel identifiers were found in the uploaded file.");
    }
  }

  const validCount = results.filter((item) => item.valid).length;

  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>{title}</h2>
          <p className="muted">
            Search one parcel for real cadastral data, validate a pasted batch, or upload a CSV/TXT file of identifiers.
          </p>
        </div>
      </div>

      <div className={compact ? "stack" : "searchGrid"}>
        <div className="stack">
          <div className="field">
            <label htmlFor="single-search">Single parcel identifier</label>
            <input
              id="single-search"
              placeholder="141201_2.0003.45/6"
              value={singleValue}
              onChange={(event) => setSingleValue(event.target.value)}
            />
          </div>
          <button type="button" className="button primaryButton" onClick={handleSingleSearch} disabled={loading}>
            {loading && mode === "search" ? "Searching..." : "Search parcel"}
          </button>
        </div>

        <div className="stack">
          <div className="field">
            <label htmlFor="bulk-search">Bulk paste</label>
            <textarea
              id="bulk-search"
              placeholder={"141201_2.0003.45/6\n301105_5.0012.144"}
              value={bulkValue}
              onChange={(event) => setBulkValue(event.target.value)}
            />
          </div>
          <div className="buttonRow">
            <button type="button" className="button primaryButton" onClick={handleBulkSearch} disabled={loading}>
              {loading && mode === "search" ? "Searching..." : "Search batch"}
            </button>
            <button type="button" className="button primaryButton" onClick={handleBulkValidate} disabled={loading}>
              {loading && mode === "validate" ? "Validating..." : "Validate batch"}
            </button>
            <label className="button secondary fileButton">
              Upload CSV/TXT
              <input type="file" accept=".csv,.txt" onChange={handleFileUpload} hidden />
            </label>
            <Link href={"/imports" as Route} className="button secondary">
              Open import workspace
            </Link>
          </div>
        </div>
      </div>

      {error ? <div className="banner">{error}</div> : null}

      {results.length ? (
        <div className="stack">
          <div className="resultSummary">
            <strong>{validCount}</strong>
            <span>of {results.length} identifiers are valid</span>
          </div>

          <div className="list">
            {results.map((result) => {
              const matchedParcel = result.normalized
                ? parcelByIdentifier.get(result.normalized)
                : undefined;
              return (
                <div key={result.original} className="resultCard">
                  <div className="resultRow">
                    <div>
                      <strong>{result.original}</strong>
                      <p className="muted">
                        {result.valid
                          ? `Normalized as ${result.normalized}`
                          : result.error}
                      </p>
                    </div>
                    <span className={`pill ${result.valid ? "pillGood" : "pillBad"}`}>
                      {result.valid ? "valid" : "invalid"}
                    </span>
                  </div>
                  {result.parcel ? (
                    <div className="stack">
                      <div className="miniGrid">
                        <div>
                          <strong>Location</strong>
                          <p className="muted">
                            {result.parcel.gmina ?? "Unknown gmina"}, {result.parcel.powiat ?? "Unknown powiat"}
                          </p>
                        </div>
                        <div>
                          <strong>Area</strong>
                          <p className="muted">
                            {result.parcel.area_m2
                              ? `${result.parcel.area_m2.toLocaleString("en-US")} m2`
                              : "Unavailable"}
                          </p>
                        </div>
                        <div>
                          <strong>Land use</strong>
                          <p className="muted">{result.parcel.land_use_classification ?? "Unavailable"}</p>
                        </div>
                        <div>
                          <strong>Source</strong>
                          <p className="muted">{result.parcel.observations[0]?.source_name ?? "Stored record"}</p>
                        </div>
                      </div>
                    </div>
                  ) : matchedParcel ? (
                    <Link
                      href={`/parcels/${matchedParcel.id}` as Route}
                      className="button secondary inlineButton"
                    >
                      Open parcel record
                    </Link>
                  ) : result.valid ? (
                    <p className="muted">
                      Identifier is valid. Use search to resolve and store its cadastral data.
                    </p>
                  ) : null}
                </div>
              );
            })}
          </div>
        </div>
      ) : null}
    </section>
  );
}

function splitIdentifiers(input: string): string[] {
  return input
    .split(/[\n,;\t]+/)
    .map((value) => value.trim())
    .filter(Boolean);
}
