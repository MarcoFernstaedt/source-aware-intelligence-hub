from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TruthState(StrEnum):
    LIVE = "live"
    SCHEDULED = "scheduled"
    STALE = "stale"
    UNAVAILABLE = "unavailable"
    CONFLICTING = "conflicting"


class SourceCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9-]{3,40}$")
    kind: str = Field(max_length=32)
    title: str = Field(max_length=80)
    summary: str = Field(max_length=240)
    authority: str = Field(max_length=80)
    freshness: str = Field(max_length=80)
    truth_state: TruthState
    confidence: int | None = Field(default=None, ge=0, le=100)
    deep_link: str = Field(max_length=100)

    @field_validator("deep_link")
    @classmethod
    def allow_safe_local_demo_links(cls, value: str) -> str:
        prefix = "/demo/source/"
        identifier = value.removeprefix(prefix)
        if not value.startswith(prefix) or not identifier.replace("-", "").isalnum():
            raise ValueError("deep link must be a safe local demo path")
        return value


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(max_length=100)
    summary: str = Field(max_length=240)
    reasons: list[str] = Field(min_length=1, max_length=3)
    source_ids: list[str] = Field(min_length=1, max_length=4)


class AttentionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9-]{3,40}$")
    severity: str = Field(pattern=r"^(critical|warning|notice)$")
    title: str = Field(max_length=100)
    detail: str = Field(max_length=240)
    source_ids: list[str] = Field(min_length=1, max_length=4)


class Workspace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario: str
    generated_at: str
    recommendation: Decision
    alternatives: list[Decision] = Field(min_length=2, max_length=2)
    attention: list[AttentionItem]
    sources: list[SourceCard]
