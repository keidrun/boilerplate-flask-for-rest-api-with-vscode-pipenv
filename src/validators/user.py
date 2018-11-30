from marshmallow import Schema, fields, validates, ValidationError

__all__ = ['UserPostSchema', 'UserPutSchema']


def _check_gender(gender):
    if not gender in ['male', 'female']:
        raise ValidationError("Gender must be 'male' or 'female'")


class UserPostSchema(Schema):
    name = fields.String(required=True, validate=lambda s: 3 <= len(s) <= 50)
    age = fields.Number(validate=lambda n: n >= 0)
    gender = fields.String()
    email = fields.Email(required=True)

    @validates('gender')
    def validate_gender(self, value):
        _check_gender(value)


class UserPutSchema(Schema):
    name = fields.String(validate=lambda s: 3 <= len(s) <= 50)
    age = fields.Number(validate=lambda n: n >= 0)
    gender = fields.String()
    email = fields.Email()

    @validates('gender')
    def validate_gender(self, value):
        _check_gender(value)
