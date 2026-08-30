import type {
  AttentionItem,
  Decision,
  Scenario,
  SourceCard,
  TruthState,
  Workspace,
} from "./types";

const SCENARIOS = new Set<Scenario>(["baseline", "degraded", "conflict"]);
const TRUTH_STATES = new Set<TruthState>([
  "live",
  "scheduled",
  "stale",
  "unavailable",
  "conflicting",
]);
const SEVERITIES = new Set<AttentionItem["severity"]>([
  "critical",
  "warning",
  "notice",
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function hasExactKeys(
  record: Record<string, unknown>,
  expected: string[],
): boolean {
  const actual = Object.keys(record).sort();
  return (
    actual.length === expected.length &&
    actual.every((key, index) => key === expected[index])
  );
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.length > 0;
}

function isStringArray(value: unknown): value is string[] {
  return (
    Array.isArray(value) && value.length > 0 && value.every(isNonEmptyString)
  );
}

function isDecision(value: unknown): value is Decision {
  if (!isRecord(value)) return false;
  return (
    hasExactKeys(value, ["reasons", "source_ids", "summary", "title"]) &&
    isNonEmptyString(value.title) &&
    isNonEmptyString(value.summary) &&
    isStringArray(value.reasons) &&
    isStringArray(value.source_ids)
  );
}

function isAttentionItem(value: unknown): value is AttentionItem {
  if (!isRecord(value)) return false;
  return (
    hasExactKeys(value, ["detail", "id", "severity", "source_ids", "title"]) &&
    isNonEmptyString(value.id) &&
    isNonEmptyString(value.title) &&
    isNonEmptyString(value.detail) &&
    typeof value.severity === "string" &&
    SEVERITIES.has(value.severity as AttentionItem["severity"]) &&
    isStringArray(value.source_ids)
  );
}

function isSourceCard(value: unknown): value is SourceCard {
  if (!isRecord(value)) return false;
  return (
    hasExactKeys(value, [
      "authority",
      "confidence",
      "deep_link",
      "freshness",
      "id",
      "kind",
      "summary",
      "title",
      "truth_state",
    ]) &&
    isNonEmptyString(value.id) &&
    isNonEmptyString(value.kind) &&
    isNonEmptyString(value.title) &&
    isNonEmptyString(value.summary) &&
    isNonEmptyString(value.authority) &&
    isNonEmptyString(value.freshness) &&
    typeof value.truth_state === "string" &&
    TRUTH_STATES.has(value.truth_state as TruthState) &&
    (value.confidence === null ||
      (typeof value.confidence === "number" &&
        Number.isInteger(value.confidence) &&
        value.confidence >= 0 &&
        value.confidence <= 100)) &&
    isNonEmptyString(value.deep_link)
  );
}

function referencesKnownSources(
  values: string[],
  sourceIds: Set<string>,
): boolean {
  return values.every((identifier) => sourceIds.has(identifier));
}

function isWorkspace(value: unknown): value is Workspace {
  if (!isRecord(value)) return false;
  if (
    !hasExactKeys(value, [
      "alternatives",
      "attention",
      "generated_at",
      "recommendation",
      "scenario",
      "sources",
    ]) ||
    typeof value.scenario !== "string" ||
    !SCENARIOS.has(value.scenario as Scenario) ||
    !isNonEmptyString(value.generated_at) ||
    !isDecision(value.recommendation) ||
    !Array.isArray(value.alternatives) ||
    value.alternatives.length !== 2 ||
    !value.alternatives.every(isDecision) ||
    !Array.isArray(value.attention) ||
    !value.attention.every(isAttentionItem) ||
    !Array.isArray(value.sources) ||
    value.sources.length === 0 ||
    !value.sources.every(isSourceCard)
  ) {
    return false;
  }

  const sourceIds = new Set(value.sources.map((source) => source.id));
  if (sourceIds.size !== value.sources.length) return false;
  return (
    referencesKnownSources(value.recommendation.source_ids, sourceIds) &&
    value.alternatives.every((decision) =>
      referencesKnownSources(decision.source_ids, sourceIds),
    ) &&
    value.attention.every((item) =>
      referencesKnownSources(item.source_ids, sourceIds),
    )
  );
}

export async function getWorkspace(
  scenario: Scenario,
  signal?: AbortSignal,
): Promise<Workspace> {
  const response = await fetch(
    `/api/workspace?scenario=${encodeURIComponent(scenario)}`,
    {
      method: "GET",
      headers: { Accept: "application/json" },
      credentials: "same-origin",
      signal,
    },
  );
  if (!response.ok) throw new Error("Workspace is temporarily unavailable.");
  const body: unknown = await response.json();
  if (!isWorkspace(body))
    throw new Error("Workspace response could not be verified.");
  return body;
}
