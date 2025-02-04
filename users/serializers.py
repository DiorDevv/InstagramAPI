from shared.utility import check_email_or_phone
from .models import User, UserConfirmation, VIA_EMAIL, VIA_PHONE_NOMBER, NEW, CODE_VERIFIED, DONE, PHOTO_STEP
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignupSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignupSerializers, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status',
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}

        }

    def validate(self, data):
        super(SignupSerializers, self).validate(data)  # MUHIM: natijani saqlash
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        if input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL,
            }

        elif input_type == 'phone':
            data = {
                'email': user_input,
                'auth_type': VIA_PHONE_NOMBER,
            }

        else:
            data = {
                'success': False,
                'message': 'Nomer yoki email',
            }

            raise ValidationError(data)
        print("data", data)
        return data
