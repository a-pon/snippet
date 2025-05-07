from fastapi import APIRouter, HTTPException
from typing import List

from auth.auth import user_dependency
from db.db import db_dependency
from schemas.snippet import SnippetSchema, SnippetCreateSchema
from services import snippet as service

snippet_router = APIRouter(prefix='/snippets', tags=['snippets'])


@snippet_router.get('/', response_model=List[SnippetSchema])
async def get_all_snippets(db: db_dependency):
    return await service.get_snippets(db)


@snippet_router.get('/my', response_model=List[SnippetSchema])
async def get_my_snippets(current_user: user_dependency, db: db_dependency):
    return await service.get_snippets_by_author(current_user['sub_id'], db)


@snippet_router.post('/', response_model=SnippetSchema)
async def create_snippet(snippet_data: SnippetCreateSchema, current_user: user_dependency, db: db_dependency):
    return await service.create_snippet(snippet_data, current_user['sub_id'], db)


@snippet_router.put('/{snippet_id}', response_model=SnippetSchema)
async def update_snippet(snippet_id: int, snippet_data: SnippetCreateSchema, current_user: user_dependency, db: db_dependency):
    return await service.update_snippet(snippet_id, snippet_data, current_user['sub_id'], db)


@snippet_router.delete('/{snippet_id}')
async def delete_snippet(snippet_id: int, current_user: user_dependency, db: db_dependency):
    return await service.delete_snippet(snippet_id, current_user['sub_id'], db)


@snippet_router.get('/share/{uuid}', response_model=SnippetSchema)
async def share_snippet(uuid: str, db: db_dependency):
    snippet = await service.get_snippet_by_uuid(uuid, db)
    if not snippet:
        raise HTTPException(status_code=404, detail='Snippet not found')
    return snippet
