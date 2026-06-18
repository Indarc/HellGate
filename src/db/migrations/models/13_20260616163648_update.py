from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "entity" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "identificator" TEXT NOT NULL,
    "entity_dict" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "entity";"""
