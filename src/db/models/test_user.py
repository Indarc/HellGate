from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

import json


class TestUserModel(Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    user_entity = fields.JSONField(encoder=lambda x: json.dumps(x, ensure_ascii=False), decoder=lambda x: json.loads(x))
    status = fields.BooleanField(default=True)

    class Meta:
        table = "test_users"


UserShema = pydantic_model_creator(TestUserModel)