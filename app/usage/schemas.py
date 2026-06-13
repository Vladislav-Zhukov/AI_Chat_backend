from pydantic import BaseModel


class UsageStatsRead(BaseModel):
    requests_count: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int