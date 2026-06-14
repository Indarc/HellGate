from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "items" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "identificator" TEXT NOT NULL,
    "data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "test_users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_entity" JSONB NOT NULL,
    "status" BOOL NOT NULL DEFAULT True
);
        DROP TABLE IF EXISTS "test_users";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "items";
        DROP TABLE IF EXISTS "test_users";"""
