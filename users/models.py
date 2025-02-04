import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.regex_helper import normalize
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

ORDINARY_USER, MANAGER, ADMIN = ('ordinary_user', 'manager', 'admin')
VIA_EMAIL, VIA_PHONE_NOMBER = ('via_email', 'via_phone_number')
NEW, CODE_VERIFIED, DONE, PHOTO_STEP = ('new', 'code_verified', 'done', 'photo')


class User(AbstractUser, BaseModel):
    USER_ROLE = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE_NOMBER, VIA_PHONE_NOMBER),
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_STEP, PHOTO_STEP)
    )
    user_role = models.CharField(max_length=100, choices=USER_ROLE, default=ORDINARY_USER)
    auth_type = models.CharField(max_length=16, choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=199, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, unique=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True,
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'pnj', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def create_verification_code(self, verify_type):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code,

        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f"instagram - {uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(1, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE_NOMBER, VIA_PHONE_NOMBER),
        (VIA_EMAIL, VIA_EMAIL),
    )
    code = models.CharField(max_length=10, unique=True)
    verify_type = models.CharField(max_length=19, choices=TYPE_CHOICES, default=CODE_VERIFIED)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='verify_codes')
    expires_times = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == VIA_EMAIL:  # 3-fevral 23-34 + 5 minut
                self.expires_times = datetime.now() + timedelta(milliseconds=EMAIL_EXPIRE)
            else:
                self.expires_times = datetime.now() + timedelta(milliseconds=PHONE_EXPIRE)

        super(UserConfirmation, self).save(*args, **kwargs)
