from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import datetime
from apexhub.settings import AUTH_USER_MODEL
from django.conf import settings
from ashop.validators import file_size_validation


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    USER_TYPE_ACS = "acs"
    USER_TYPE_STUDENT = "student"
    USER_TYPE_EXTERNAL = "external"

    USER_TYPE_CHOICES = (
        (USER_TYPE_STUDENT, "student"),
        (USER_TYPE_ACS, "acs"),
        (USER_TYPE_EXTERNAL, "external"),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(
        max_length=255, choices=USER_TYPE_CHOICES, default=USER_TYPE_STUDENT
    )
    avatar = models.ImageField(
        upload_to="avatar", validators=[file_size_validation], null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_student(self):
        return self.user_type == self.USER_TYPE_STUDENT

    @property
    def is_acs(self):
        return self.user_type == self.USER_TYPE_ACS

    @property
    def is_external(self):
        return self.user_type == self.USER_TYPE_EXTERNAL

    def has_perms(self, perm, obj=None):
        return self.is_admin
        # return True

    def has_perm(self, perm, obj=None):
        return self.is_admin
        # return True

    def has_module_perms(self, app_label):
        return True


class Student(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )
    PROGRAM_CHOICES = (
        ("bcis", "Bachelor of Computer Information System"),
        ("bit", "Bachelor of Tourism"),
        ("bba", "Bachelor of Business Administration"),
        ("bba-bi", "Bachelor of Business Administration BI"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_student"
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(
        max_length=255, choices=PROGRAM_CHOICES, blank=True, null=True
    )
    enrollment_date = models.DateTimeField(blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    # qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.enrollment_date = datetime.now()
    #     return super().save(*args, **kwargs)

    def __str__(self):
        # full_name = self.first_name + " " + self.last_name
        # return full_name
        return self.user.email

    def get_email_field_name(self):
        return self.user.email


class Acs(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_acs"
    )
    website = models.URLField()

    def __str__(self):
        return self.user.email


class External(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_external"
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    # created_at = models.DateField()

    def __str__(self):
        return self.user.email


class Rating(models.Model):
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings"
    )
    rate = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} : rated : ({self.rate}) on user : {self.rated_user}"
