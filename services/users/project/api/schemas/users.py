from project.utils.ma import ma
from project.api.models.users import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password", )
        dump_only = ("id", )
