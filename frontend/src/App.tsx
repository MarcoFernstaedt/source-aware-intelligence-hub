import { useEffect, useMemo, useState } from "react";

import { getWorkspace } from "./api";
import { safeLocalLink } from "./security";
import type {
  Decision,
  Scenario,
  SourceCard,
  TruthState,
  Workspace,
} from "./types";

const SCENARIOS: Array<{ id: Scenario; label: string; note: string }> = [
  { id: "baseline", label: "Baseline", note: "Mixed freshness" },
  { id: "degraded", label: "Source unavailable", note: "Failure mode" },
  { id: "conflict", label: "Conflicting sources", note: "Disagreement" },
];

const STATE_LABELS: Record<TruthState, string> = {
  live: "Live",
  scheduled: "Scheduled",
  stale: "Stale",
  unavailable: "Unavailable",
  conflicting: "Conflicting",
};

function SourceReferences({
  ids,
  sources,
}: {
  ids: string[];
  sources: SourceCard[];
}) {
  const byId = useMemo(
    () => new Map(sources.map((source) => [source.id, source])),
    [sources],
  );
  return (
    <ul className="source-refs" aria-label="Sources for this outcome">
      {ids.map((id) => {
        const source = byId.get(id);
        return source ? (
          <li key={id}>
            {source.kind}: {source.title}
          </li>
        ) : null;
      })}
    </ul>
  );
}

function AlternativeCard({
  decision,
  sources,
}: {
  decision: Decision;
  sources: SourceCard[];
}) {
  return (
    <article className="alternative-card">
      <p className="eyebrow">Alternative</p>
      <h3>{decision.title}</h3>
      <p>{decision.summary}</p>
      <p className="reason">{decision.reasons[0]}</p>
      <SourceReferences ids={decision.source_ids} sources={sources} />
    </article>
  );
}

function SourceStatus({ source }: { source: SourceCard }) {
  const destination = safeLocalLink(source.deep_link);
  return (
    <article
      className="source-card"
      data-state={source.truth_state}
      id={`source-${source.id}`}
    >
      <div className="source-card__top">
        <p className="eyebrow">{source.kind}</p>
        <span className="truth-state">
          <span aria-hidden="true" className="state-dot" />
          {STATE_LABELS[source.truth_state]}
        </span>
      </div>
      <h3>{source.title}</h3>
      <p>{source.summary}</p>
      <dl>
        <div>
          <dt>Authority</dt>
          <dd>{source.authority}</dd>
        </div>
        <div>
          <dt>Freshness</dt>
          <dd>{source.freshness}</dd>
        </div>
        <div>
          <dt>Confidence</dt>
          <dd>
            {source.confidence === null
              ? "Confidence unavailable"
              : `${source.confidence}%`}
          </dd>
        </div>
      </dl>
      {destination ? (
        <a className="text-link" href={destination}>
          Inspect synthetic source
          <span className="sr-only">: {source.title}</span>
        </a>
      ) : (
        <span>Link unavailable</span>
      )}
    </article>
  );
}

export default function App() {
  const [scenario, setScenario] = useState<Scenario>("baseline");
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    setError(null);
    getWorkspace(scenario, controller.signal)
      .then(setWorkspace)
      .catch((reason: unknown) => {
        if (!controller.signal.aborted) {
          setError(
            reason instanceof Error
              ? reason.message
              : "Workspace is temporarily unavailable.",
          );
        }
      });
    return () => controller.abort();
  }, [scenario, retry]);

  const loading = !workspace || workspace.scenario !== scenario;

  return (
    <div className="app-shell">
      <header className="site-header">
        <a
          className="brand"
          href="/"
          aria-label="Source-Aware Intelligence Hub home"
        >
          <span className="brand-mark" aria-hidden="true">
            S
          </span>
          <span>
            Source-Aware <strong>Intelligence Hub</strong>
          </span>
        </a>
        <span className="demo-badge">Synthetic demo</span>
      </header>

      <main id="main">
        <section className="intro" aria-labelledby="page-title">
          <div>
            <p className="kicker">Truth-state-first decision support</p>
            <h1 id="page-title">
              Know what to do next—
              <br />
              <span>and why you can trust it.</span>
            </h1>
            <p className="lede">
              A credential-free workspace that ranks one outcome, preserves
              alternatives, and makes source authority, freshness, and failure
              visible.
            </p>
          </div>
          <div
            className="safety-note"
            role="note"
            aria-label="Demo safety boundary"
          >
            <span aria-hidden="true">◎</span>
            <div>
              <strong>Read-only by design</strong>
              <p>
                All records are deterministic and fictional. No external action
                or live integration is available.
              </p>
            </div>
          </div>
        </section>

        <section className="scenario-panel" aria-labelledby="scenario-heading">
          <div>
            <p className="eyebrow">Failure lab</p>
            <h2 id="scenario-heading">Change the source conditions</h2>
          </div>
          <div className="scenario-buttons">
            {SCENARIOS.map((item) => (
              <button
                key={item.id}
                type="button"
                aria-pressed={scenario === item.id}
                onClick={() => setScenario(item.id)}
              >
                <span>{item.label}</span>
                <small>{item.note}</small>
              </button>
            ))}
          </div>
        </section>

        <div className="load-status" aria-live="polite" aria-atomic="true">
          {loading && !error ? "Loading verified source state…" : null}
          {error ? (
            <div role="alert">
              <strong>Decision workspace unavailable.</strong> {error}{" "}
              <button
                type="button"
                onClick={() => setRetry((value) => value + 1)}
              >
                Retry
              </button>
            </div>
          ) : null}
        </div>

        {!loading && workspace ? (
          <div className="workspace">
            <section
              className="attention-section"
              aria-labelledby="attention-heading"
            >
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Exception first</p>
                  <h2 id="attention-heading">Attention queue</h2>
                </div>
                <span>
                  {workspace.attention.length}{" "}
                  {workspace.attention.length === 1 ? "item" : "items"}
                </span>
              </div>
              <div className="attention-list">
                {workspace.attention.map((item) => (
                  <article
                    className="attention-item"
                    data-severity={item.severity}
                    key={item.id}
                  >
                    <span className="attention-icon" aria-hidden="true">
                      !
                    </span>
                    <div>
                      <h3>{item.title}</h3>
                      <p>{item.detail}</p>
                      <SourceReferences
                        ids={item.source_ids}
                        sources={workspace.sources}
                      />
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section
              className="decision-section"
              aria-labelledby="decision-heading"
            >
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Ranked outcome</p>
                  <h2 id="decision-heading">Decision brief</h2>
                </div>
                <span>Updated from synthetic snapshot</span>
              </div>
              <article className="recommendation-card">
                <div className="rank" aria-label="Recommended outcome">
                  01
                </div>
                <div>
                  <p className="recommend-label">Recommended now</p>
                  <h2>{workspace.recommendation.title}</h2>
                  <p className="recommend-summary">
                    {workspace.recommendation.summary}
                  </p>
                  <ul className="reasons">
                    {workspace.recommendation.reasons.map((reason) => (
                      <li key={reason}>{reason}</li>
                    ))}
                  </ul>
                  <SourceReferences
                    ids={workspace.recommendation.source_ids}
                    sources={workspace.sources}
                  />
                </div>
              </article>
              <div className="alternatives">
                {workspace.alternatives.map((decision) => (
                  <AlternativeCard
                    key={decision.title}
                    decision={decision}
                    sources={workspace.sources}
                  />
                ))}
              </div>
            </section>

            <section
              className="sources-section"
              aria-labelledby="sources-heading"
            >
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Evidence layer</p>
                  <h2 id="sources-heading">Source truth</h2>
                </div>
                <span>{workspace.sources.length} normalized sources</span>
              </div>
              <div className="source-grid">
                {workspace.sources.map((source) => (
                  <SourceStatus source={source} key={source.id} />
                ))}
              </div>
            </section>
          </div>
        ) : null}
      </main>

      <footer>
        <p>
          Portfolio demonstration · deterministic data · no credentials · no
          external mutations
        </p>
      </footer>
    </div>
  );
}
