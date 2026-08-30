from backend.app.fixtures import GENERATED_AT, build_fixture
from backend.app.models import Decision, Workspace


def build_workspace(scenario: str) -> Workspace:
    sources, attention = build_fixture(scenario)

    recommendation_reasons = [
        "The team calendar marks the launch review as the nearest fixed commitment.",
        "The task board shows two evidence notes still open on today's brief.",
    ]
    if scenario == "conflict":
        recommendation_reasons = [
            "The calendar and task board disagree on timing, so confirm the review time first.",
            "The task board still shows two evidence notes open on today's brief.",
        ]

    return Workspace(
        scenario=scenario,
        generated_at=GENERATED_AT,
        recommendation=Decision(
            title="Protect the launch review block",
            summary="Use the next focused block to close the decision brief before the review.",
            reasons=recommendation_reasons,
            source_ids=["calendar-launch", "task-launch"],
        ),
        alternatives=[
            Decision(
                title="Verify the vendor response",
                summary=(
                    "Check the inbox source when it becomes available or reaches its next window."
                ),
                reasons=[
                    "The response may change a launch assumption, but the source is not always "
                    "live."
                ],
                source_ids=["inbox-vendor"],
            ),
            Decision(
                title="Refresh market context",
                summary="Update the market digest after the fixed launch work is protected.",
                reasons=["The digest is informative but currently outside its freshness target."],
                source_ids=["news-market"],
            ),
        ],
        attention=attention,
        sources=sources,
    )
