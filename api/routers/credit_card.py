from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.credit_card import CreditCardService
from schemas.credit_card import CreditCard
from middlewares.jwt_auth import JWTBearer
from config.database import async_session

credit_card_router = APIRouter()


@credit_card_router.get('/credit_cards', tags=['credit_cards'], dependencies=[Depends(JWTBearer())])
async def get_credit_cards(request: Request):
    user_id = request.state.user_id
    async with async_session() as db:
        credit_cards = await CreditCardService(db).get_credit_cards(user_id)

    response = jsonable_encoder(credit_cards)
    return JSONResponse(status_code=200, content=response)


@credit_card_router.get('/credit_cards/{id}', tags=['credit_cards'], dependencies=[Depends(JWTBearer())])
async def get_credit_card(request: Request, id: int = Path(ge=1, le=2000),) -> CreditCard:
    user_id = request.state.user_id
    async with async_session() as db:
        result = await CreditCardService(db).get_credit_card(id, user_id)

    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@credit_card_router.post('/credit_cards', tags=['credit_cards'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_credit_cards(request: Request, credit_card: CreditCard) -> dict:
    user_id = request.state.user_id
    async with async_session() as db:
        await CreditCardService(db).create_credit_card(credit_card,user_id)

    return JSONResponse(status_code=201, content={"message": "Credit Card created"})


@credit_card_router.put('/credit_cards/{id}', tags=['credit_cards'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
async def update_bank(request: Request, id: int, bank: CreditCard) -> dict:
    user_id = request.state.user_id
    async with async_session() as db:
        updated_bank = await CreditCardService(db).update_credit_card(id, bank)

    if not updated_bank:
        return JSONResponse(status_code=404, content={"message": "CreditCard not found"})
    
    return JSONResponse(status_code=200, content={"message": "CreditCard updated", "bank": jsonable_encoder(updated_bank)})


@credit_card_router.delete('/credit_cards/{id}', tags=['credit_cards'], response_model=dict, status_code=200,  dependencies=[Depends(JWTBearer())])
async def delete_bank(request: Request, id: int) -> dict:
    user_id = request.state.user_id
    async with async_session() as db:
        deleted = await CreditCardService(db).delete_credit_card(id, user_id)

    if not deleted:
        return JSONResponse(status_code=404, content={"message": "CreditCard not found"})
    
    return JSONResponse(status_code=200, content={"message": "CreditCard deleted"})