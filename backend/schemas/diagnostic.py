from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: str
    title: str
    description: str
    root: str


class OptionOut(BaseModel):
    label: str
    next: str


class NodeOut(BaseModel):
    id: str
    is_result: bool
    # question branch
    question: str | None = None
    options: list[OptionOut] = []
    # result branch
    severity: str | None = None
    title: str | None = None
    steps: list[str] = []
