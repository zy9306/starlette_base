from tortoise import fields, models
from tortoise.manager import Manager


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = fields.BooleanField(default=False)

    all_objects = Manager()

    class Meta:
        abstract = True
        manager = SoftDeleteManager()


class BaseModel(models.Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
