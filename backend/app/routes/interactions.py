from fastapi import APIRouter
from ..schemas import InteractionCreate, InteractionUpdate

router = APIRouter(tags=["interactions"])
_db: list[dict] = []

@router.post('/interactions')
def create_interaction(payload: InteractionCreate):
    new = payload.model_dump()
    new['id'] = len(_db)+1
    _db.append(new)
    return new

@router.patch('/interactions/{interaction_id}')
def edit_interaction(interaction_id: int, payload: InteractionUpdate):
    for row in _db:
        if row['id']==interaction_id:
            row.update(payload.model_dump(exclude_none=True))
            return row
    return {'error':'not found'}