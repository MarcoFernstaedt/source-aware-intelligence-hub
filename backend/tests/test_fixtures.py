from backend.app.fixtures import build_fixture
from backend.app.models import TruthState


def test_fictional_scenario_fixture_is_deterministic_and_preserves_failure_truth() -> None:
    first = build_fixture("degraded")
    second = build_fixture("degraded")

    assert first == second
    sources, attention = first
    assert any(source.truth_state is TruthState.UNAVAILABLE for source in sources)
    assert attention[0].severity == "critical"
