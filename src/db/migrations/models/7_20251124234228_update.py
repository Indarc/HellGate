from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "status" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "test_users" ADD "status" BOOL NOT NULL DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "status";
        ALTER TABLE "test_users" DROP COLUMN "status";"""
