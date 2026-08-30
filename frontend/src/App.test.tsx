import { axe, toHaveNoViolations } from "jest-axe";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";
import type { Workspace } from "./types";

expect.extend(toHaveNoViolations);

const baseline: Workspace = {
  scenario: "baseline",
  generated_at: "2026-04-14T09:30:00Z",
  recommendation: {
    title: "Protect the launch review block",
    summary: "Close the decision brief before the review.",
    reasons: ["Calendar is authoritative.", "Task evidence remains open."],
    source_ids: ["calendar-launch", "task-launch"],
  },
  alternatives: [
    {
      title: "Verify vendor response",
      summary: "Wait for collection.",
      reasons: ["Source is scheduled."],
      source_ids: ["inbox-vendor"],
    },
    {
      title: "Refresh market context",
      summary: "Refresh later.",
      reasons: ["Source is stale."],
      source_ids: ["news-market"],
    },
  ],
  attention: [
    {
      id: "news-stale",
      severity: "warning",
      title: "Market digest is stale",
      detail: "Treat as context only.",
      source_ids: ["news-market"],
    },
  ],
  sources: [
    {
      id: "calendar-launch",
      kind: "Calendar",
      title: "Atlas launch review",
      summary: "Review at 10:00.",
      authority: "Team calendar",
      freshness: "2 minutes ago",
      truth_state: "live",
      confidence: 98,
      deep_link: "/demo/source/calendar-launch",
    },
    {
      id: "task-launch",
      kind: "Tasks",
      title: "Launch brief",
      summary: "Two notes open.",
      authority: "Task board",
      freshness: "4 minutes ago",
      truth_state: "live",
      confidence: 94,
      deep_link: "/demo/source/task-launch",
    },
    {
      id: "inbox-vendor",
      kind: "Inbox",
      title: "Vendor response",
      summary: "Queued.",
      authority: "Demo inbox",
      freshness: "10:15",
      truth_state: "scheduled",
      confidence: 86,
      deep_link: "/demo/source/inbox-vendor",
    },
    {
      id: "news-market",
      kind: "News",
      title: "Market digest",
      summary: "Outside target.",
      authority: "Curated feed",
      freshness: "52 minutes ago",
      truth_state: "stale",
      confidence: 63,
      deep_link: "/demo/source/news-market",
    },
  ],
};

const degraded: Workspace = {
  ...baseline,
  scenario: "degraded",
  attention: [
    {
      id: "inbox-down",
      severity: "critical",
      title: "Inbox source is unavailable",
      detail: "Do not infer a reply.",
      source_ids: ["inbox-vendor"],
    },
  ],
  sources: baseline.sources.map((source) =>
    source.id === "inbox-vendor"
      ? { ...source, truth_state: "unavailable", confidence: null }
      : source,
  ),
};

beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL) => {
      const scenario = String(input).includes("degraded") ? degraded : baseline;
      return new Response(JSON.stringify(scenario), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }),
  );
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("decision workspace", () => {
  it("renders the recommendation, alternatives, attention, and source truth", async () => {
    render(<App />);
    expect(
      await screen.findByRole("heading", {
        name: "Protect the launch review block",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Verify vendor response" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Refresh market context" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Market digest is stale")).toBeInTheDocument();
    expect(screen.getAllByText("Live").length).toBeGreaterThan(0);
  });

  it("demonstrates a degraded source without claiming confidence", async () => {
    const user = userEvent.setup();
    render(<App />);
    await screen.findByRole("heading", {
      name: "Protect the launch review block",
    });
    await user.click(
      screen.getByRole("button", { name: /Source unavailable/ }),
    );

    expect(
      await screen.findByText("Inbox source is unavailable"),
    ).toBeInTheDocument();
    expect(screen.getByText("Unavailable")).toBeInTheDocument();
    expect(screen.getByText("Confidence unavailable")).toBeInTheDocument();
  });

  it("has no detectable automated accessibility violations", async () => {
    const { container } = render(<App />);
    await screen.findByRole("heading", {
      name: "Protect the launch review block",
    });
    await waitFor(async () =>
      expect(await axe(container)).toHaveNoViolations(),
    );
  });

  it("fails closed when a nested workspace contract is malformed", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async () =>
          new Response(
            JSON.stringify({
              ...baseline,
              recommendation: {
                ...baseline.recommendation,
                source_ids: ["missing-source"],
              },
            }),
            { status: 200, headers: { "Content-Type": "application/json" } },
          ),
      ),
    );

    render(<App />);

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Workspace response could not be verified.",
    );
    expect(
      screen.queryByRole("heading", {
        name: "Protect the launch review block",
      }),
    ).not.toBeInTheDocument();
  });
});
