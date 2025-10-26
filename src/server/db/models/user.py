from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

import json


class User(Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    user_entity = fields.JSONField(encoder=lambda x: json.dumps(x, ensure_ascii=False), decoder=lambda x: json.loads(x))

    class Meta:
        table = "user"


UserShema = pydantic_model_creator(User)