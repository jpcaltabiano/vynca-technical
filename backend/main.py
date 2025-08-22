from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from app.db.database import get_db_session, init_db
from app.api.graphql import schema
from strawberry.fastapi import GraphQLRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(
    schema,
    context_getter=lambda req, resp: {"db_session": get_db_session()},
)

app.include_router(graphql_app, prefix="/graphql")