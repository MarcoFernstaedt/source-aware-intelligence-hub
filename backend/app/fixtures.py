from collections.abc import Iterable

from backend.app.models import AttentionItem, SourceCard, TruthState

GENERATED_AT = "2026-04-14T09:30:00Z"
_SCENARIOS = frozenset({"baseline", "degraded", "conflict"})


def _source(
    identifier: str,
    kind: str,
    title: str,
    summary: str,
    authority: str,
    freshness: str,
    state: TruthState,
    confidence: int | None,
) -> SourceCard:
    return SourceCard(
        id=identifier,
        kind=kind,
        title=title,
        summary=summary,
        authority=authority,
        freshness=freshness,
        truth_state=state,
        confidence=confidence,
        deep_link=f"/demo/source/{identifier}",
    )


def _baseline_sources() -> list[SourceCard]:
    return [
        _source(
            "calendar-launch",
            "Calendar",
            "Atlas launch review",
            "Review window begins at 10:00 and has no attendee conflicts.",
            "Team calendar",
            "Checked 2 minutes ago",
            TruthState.LIVE,
            98,
        ),
        _source(
            "task-launch",
            "Tasks",
            "Launch decision brief",
            "Brief is due today; two evidence notes still need review.",
            "Project task board",
            "Checked 4 minutes ago",
            TruthState.LIVE,
            94,
        ),
        _source(
            "inbox-vendor",
            "Inbox",
            "Vendor response",
            "A synthetic reply is queued for the next scheduled collection.",
            "Shared demo inbox",
            "Next check at 10:15",
            TruthState.SCHEDULED,
            86,
        ),
        _source(
            "news-market",
            "News",
            "Market digest",
            "Last successful digest is outside its 30-minute freshness target.",
            "Curated public feed",
            "Last checked 52 minutes ago",
            TruthState.STALE,
            63,
        ),
        _source(
            "status-workshop",
            "Service status",
            "Atlas Workshop systems",
            "All synthetic demo services report normal operation.",
            "Demo status monitor",
            "Checked 1 minute ago",
            TruthState.LIVE,
            99,
        ),
    ]


def _replace(sources: Iterable[SourceCard], identifier: str, **changes: object) -> list[SourceCard]:
    return [
        source.model_copy(update=changes) if source.id == identifier else source
        for source in sources
    ]


def build_fixture(scenario: str) -> tuple[list[SourceCard], list[AttentionItem]]:
    if scenario not in _SCENARIOS:
        raise ValueError("invalid scenario")

    sources = _baseline_sources()
    attention = [
        AttentionItem(
            id="news-stale",
            severity="warning",
            title="Market digest is stale",
            detail="Treat the digest as context only until its next successful refresh.",
            source_ids=["news-market"],
        )
    ]

    if scenario == "degraded":
        sources = _replace(
            sources,
            "inbox-vendor",
            summary="The synthetic inbox connector is intentionally unavailable.",
            freshness="Last attempt failed 6 minutes ago",
            truth_state=TruthState.UNAVAILABLE,
            confidence=None,
        )
        attention.insert(
            0,
            AttentionItem(
                id="inbox-unavailable",
                severity="critical",
                title="Inbox source is unavailable",
                detail="Do not infer whether the vendor replied; verify through another source.",
                source_ids=["inbox-vendor"],
            ),
        )
    elif scenario == "conflict":
        sources = _replace(
            sources,
            "task-launch",
            summary="Task board lists 11:00, which conflicts with the calendar's 10:00 review.",
            freshness="Checked 4 minutes ago",
            truth_state=TruthState.CONFLICTING,
            confidence=72,
        )
        attention.insert(
            0,
            AttentionItem(
                id="launch-time-conflict",
                severity="critical",
                title="Launch review time conflicts",
                detail="Calendar and task board disagree; confirm the time before acting.",
                source_ids=["calendar-launch", "task-launch"],
            ),
        )

    return sources, attention
