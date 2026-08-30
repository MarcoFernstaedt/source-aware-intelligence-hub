export type TruthState =
  | "live"
  | "scheduled"
  | "stale"
  | "unavailable"
  | "conflicting";
export type Scenario = "baseline" | "degraded" | "conflict";

export interface SourceCard {
  id: string;
  kind: string;
  title: string;
  summary: string;
  authority: string;
  freshness: string;
  truth_state: TruthState;
  confidence: number | null;
  deep_link: string;
}

export interface Decision {
  title: string;
  summary: string;
  reasons: string[];
  source_ids: string[];
}

export interface AttentionItem {
  id: string;
  severity: "critical" | "warning" | "notice";
  title: string;
  detail: string;
  source_ids: string[];
}

export interface Workspace {
  scenario: Scenario;
  generated_at: string;
  recommendation: Decision;
  alternatives: Decision[];
  attention: AttentionItem[];
  sources: SourceCard[];
}
