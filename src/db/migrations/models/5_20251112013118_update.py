from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME TO "test_users";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "test_users" RENAME TO "users";"""
