from fastapi import HTTPException
from sqlalchemy import select

from db.db import db_dependency
from models import Snippet
from schemas.snippet import SnippetCreateSchema


async def get_snippets(db: db_dependency, offset: int = 0, limit: int = 10):
    result = await db.execute(select(Snippet).offset(offset).limit(limit))
    return result.scalars().all()


async def get_snippet_by_id(snippet_id: int, db: db_dependency):
    result = await db.execute(select(Snippet).filter(Snippet.id == snippet_id))
    return result.scalars().first()


async def get_snippet_by_uuid(uuid: str, db: db_dependency):
    result = await db.execute(select(Snippet).filter(Snippet.uuid == uuid))
    return result.scalars().first()


async def get_snippets_by_author(author_id: int, db: db_dependency):
    result = await db.execute(select(Snippet).where(Snippet.author_id == author_id))
    return result.scalars().all()


async def create_snippet(snippet_data: SnippetCreateSchema, author_id: int, db: db_dependency):
    snippet = Snippet(**snippet_data.model_dump(), author_id=author_id)
    db.add(snippet)
    await db.commit()
    await db.refresh(snippet)
    return snippet


async def update_snippet(snippet_id: int, snippet_data: SnippetCreateSchema, author_id: int, db: db_dependency):
    result = await db.execute(select(Snippet).where(Snippet.id == snippet_id))
    snippet = result.scalars().first()
    if not snippet or snippet.author_id != author_id:
        raise HTTPException(status_code=404, detail='Snippet not found or forbidden')
    snippet.code = snippet_data.code
    await db.commit()
    await db.refresh(snippet)
    return snippet


async def delete_snippet(snippet_id: int, author_id: int, db: db_dependency):
    result = await db.execute(select(Snippet).where(Snippet.id == snippet_id))
    snippet = result.scalars().first()
    if not snippet or snippet.author_id != author_id:
        raise HTTPException(status_code=404, detail='Snippet not found or forbidden')
    await db.delete(snippet)
    await db.commit()
    return {'response': 'Snippet deleted successfully'}
