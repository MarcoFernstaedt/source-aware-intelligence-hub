from backend.app.models import TruthState
from backend.app.service import build_workspace


def test_default_workspace_recommends_focus_block_with_grounded_reasons() -> None:
    workspace = build_workspace("baseline")

    assert workspace.recommendation.title == "Protect the launch review block"
    assert len(workspace.alternatives) == 2
    assert workspace.recommendation.source_ids == ["calendar-launch", "task-launch"]
    assert all(reason.strip() for reason in workspace.recommendation.reasons)


def test_scenario_matrix_exposes_every_truth_state_without_fabricating_health() -> None:
    states = {
        source.truth_state
        for scenario in ("baseline", "degraded", "conflict")
        for source in build_workspace(scenario).sources
    }

    assert states == set(TruthState)
    degraded = build_workspace("degraded")
    assert any(item.severity == "critical" for item in degraded.attention)
    assert all(
        source.confidence is None
        for source in degraded.sources
        if source.truth_state == "unavailable"
    )


def test_ranking_is_deterministic() -> None:
    first = build_workspace("conflict").model_dump_json()
    second = build_workspace("conflict").model_dump_json()
    assert first == second


def test_conflict_changes_recommendation_reason_without_hiding_disagreement() -> None:
    workspace = build_workspace("conflict")

    assert any("disagree" in reason.lower() for reason in workspace.recommendation.reasons)
    assert "calendar-launch" in workspace.recommendation.source_ids
    assert "task-launch" in workspace.recommendation.source_ids


def test_all_source_links_are_safe_local_demo_paths() -> None:
    for scenario in ("baseline", "degraded", "conflict"):
        for source in build_workspace(scenario).sources:
            assert source.deep_link.startswith("/demo/source/")
            assert "://" not in source.deep_link
