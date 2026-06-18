from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

import json


class EntityModel(Model):
    identificator = fields.TextField()
    data = fields.JSONField(encoder=lambda x: json.dumps(x, ensure_ascii=False), decoder=lambda x: json.loads(x))

    class Meta:
        table = "entity"


UserShema = pydantic_model_creator(EntityModel)