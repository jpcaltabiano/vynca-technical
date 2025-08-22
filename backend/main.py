from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from app.db.database import get_db_session, init_db, async_session
from app.api.graphql import schema
from strawberry.fastapi import GraphQLRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

async def get_context(request: Request):
    session = async_session()
    return {"db_session": session}

graphql_app = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")
