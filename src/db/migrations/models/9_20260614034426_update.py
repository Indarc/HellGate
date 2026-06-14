from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" RENAME COLUMN "data" TO "item_dict";
        ALTER TABLE "items" DROP COLUMN "identificator";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" RENAME COLUMN "item_dict" TO "data";
        ALTER TABLE "items" ADD "identificator" TEXT NOT NULL;"""
