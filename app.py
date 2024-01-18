import asyncio
from db import Request, SessionLocal, create_database, engine
import datetime
from fastapi import FastAPI
from pydantic_models import QueryRequest, ResultResponse
from sqlalchemy.sql import select
from random import choice
import uvicorn
from sqladmin import Admin, ModelView



app = FastAPI()

async def startup():
    await create_database()


app.add_event_handler("startup", startup)

db = SessionLocal()

admin = Admin(app, engine)


class UserAdmin(ModelView, model=Request):
    column_list = '__all__'


admin.add_view(UserAdmin)

@app.post("/query")
async def get_query(request: QueryRequest):

    await asyncio.sleep(choice(range(60)))
    response = choice([True, False])
    req = Request(
        cadastre_number=request.cadastre_number,
        latitude=request.latitude,
        longitude=request.longitude,
        create_date=datetime.datetime.now(),
        response=response,
    )
    db.add(req)
    await db.commit()
    return {"message": response}


@app.get("/ping")
async def check_server_state():
    return {"message": "server state is UP"}

@app.post("/result")
async def post_result(response: ResultResponse):
    req = await db.execute(select(Request).filter(Request.id == response.id))
    rows = req.scalars().all()
    if rows:
        found_request = rows[0]
        found_request.response = response.result
        await db.flush()
        await db.commit()
        return {"message": "response updated"}
    else:
        return {"message": "no such element in db"}

                           

@app.get("/total_history")
async def get_all(): 
    querys = await db.execute(select(Request))
    return {"all requests": querys.scalars().all()}

@app.get("/history/{cadastre_number:str}")
async def get_history(cadastre_number: str):
    querys = await db.execute(select(Request).filter(Request.cadastre_number == cadastre_number))
    return {f"history for query by cadastre number {cadastre_number}": querys.scalars().all()}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)