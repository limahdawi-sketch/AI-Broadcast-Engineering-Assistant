from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=8000)
    language: str = Field(default="en", pattern="^(ar|en)$")


class DiagnoseResponse(BaseModel):
    prompt: str
    chatgpt_url: str
    claude_url: str