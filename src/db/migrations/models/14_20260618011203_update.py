from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" RENAME COLUMN "item_dict" TO "data";
        ALTER TABLE "entity" RENAME COLUMN "entity_dict" TO "data";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" RENAME COLUMN "data" TO "item_dict";
        ALTER TABLE "entity" RENAME COLUMN "data" TO "entity_dict";"""
