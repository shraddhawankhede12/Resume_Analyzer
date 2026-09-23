from pydantic import BaseModel


class SkillBar(BaseModel):
    skill: str
    score: int


class EnhanceItem(BaseModel):
    skill: str
    tips: list[str]


class AnalysisResult(BaseModel):
    score: int
    summary: str
    matched: list[str]
    missing: list[str]
    skillBars: list[SkillBar]
    enhance: list[EnhanceItem]
