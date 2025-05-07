from datetime import datetime

from pydantic import BaseModel


class SnippetSchema(BaseModel):
    id: int
    uuid: str
    code: str
    created_at: datetime
    author_id: int

    model_config = {
        "from_attributes": True
    }


class SnippetCreateSchema(BaseModel):
    code: str
