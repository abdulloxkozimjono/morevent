from __future__ import annotations

import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


def avatar_upload(instance: "Profile", filename: str) -> str:
    ext = (filename.rsplit(".", 1)[-1] if "." in filename else "jpg").lower()
    # user_id/uuid.ext – kolliziyadan saqlanish
    return f"avatars/{instance.user_id}/{uuid.uuid4().hex}.{ext}"


class UserManager(BaseUserManager):
    """AbstractUser bilan ishlayapmiz; create_user ichida minimal tekshiruvlar."""
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra):
        if not username:
            raise ValueError("Username talab qilinadi")
        if email:
            # model darajasida EmailValidator bor, lekin bu yerda ham normalize qilamiz
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra)
        if password:
            User.validate_password_strength(password)  # modeldagi helper
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_active", True)
        if extra.get("is_staff") is not True or extra.get("is_superuser") is not True:
            raise ValueError("Superuser uchun is_staff=True va is_superuser=True bo‘lishi kerak")
        return self.create_user(username=username, email=email, password=password, **extra)


class User(AbstractUser):
    """MVP: username bilan login; email unique; rol va geolokatsiya maydonlari."""
    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("user", "User"),
        ("business", "Business"),
        ("admin", "Admin"),
    )

    # username uchun qat’iy validatorlar
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(r"^[A-Za-z0-9_]+$", _("Username faqat harf, raqam va '_' bo‘lishi mumkin.")),
            MinLengthValidator(3, _("Username kamida 3 ta belgi bo‘lishi kerak.")),
        ],
        error_messages={"unique": _("Bunday username allaqachon mavjud.")},
    )

    # email unique + format tekshiruvi
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[EmailValidator(message=_("Email formati noto‘g‘ri."))],
        error_messages={"unique": _("Bu email allaqachon ishlatilgan.")},
        blank=True,
        null=True,
    )

    # ixtiyoriy telefon (O‘zbekistan formati)
    phone = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\+998\d{9}$", _("Telefon raqami: +998XXXXXXXXX"))],
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="guest")
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)

    premium = models.BooleanField(default=False)

    # referal kodi: avtomatik generatsiya
    referral_code = models.CharField(max_length=12, unique=True, blank=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # 10 belgilik, collision ehtimoli past; unique constraint himoya qiladi
            self.referral_code = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username or self.email or f"user:{self.pk}"

    # ——— Helper: parol mustahkamligini model darajasida ham tekshiraman
    @staticmethod
    def validate_password_strength(pwd: str):
        if len(pwd) < 8:
            raise ValueError("Parol kamida 8 belgidan iborat bo‘lishi kerak.")
        if not any(c.islower() for c in pwd):
            raise ValueError("Parolda kamida bitta kichik harf bo‘lishi shart.")
        if not any(c.isupper() for c in pwd):
            raise ValueError("Parolda kamida bitta katta harf bo‘lishi shart.")
        if not any(c.isdigit() for c in pwd):
            raise ValueError("Parolda kamida bitta raqam bo‘lishi shart.")
        if not any(c in "!@#$%^&*()_+-=[]{};:'\",.<>/?|`~" for c in pwd):
            raise ValueError("Parolda kamida bitta maxsus belgi bo‘lishi shart.")


class Profile(models.Model):
    """User profili: avatar, bio, bildirishnoma sozlamalari."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=avatar_upload, blank=True, null=True)
    bio = models.CharField(max_length=280, blank=True)
    push_notifications = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Profile({self.user_id})"
