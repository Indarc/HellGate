from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" DROP COLUMN "identificator";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" ADD "identificator" TEXT NOT NULL;"""
