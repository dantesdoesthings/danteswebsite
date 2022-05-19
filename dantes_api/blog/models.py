from fastapi import APIRouter, Depends

router = APIRouter(
    prefix='/blog',
    tags=['blog'],
    # dependencies=[Depends()]
    responses={404: {'description': 'Not found'}}
)

@router.get('/')
async def read_blog():
    return {'content': None}