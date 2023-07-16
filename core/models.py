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
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def generate_username(self, email):
        username = slugify(email.split("@")[0])
        new_username = username
        existing_user = self.filter(username=username).exists()
        counter = 1

        while existing_user:
            new_username = f"{username}{counter}"
            existing_user = self.filter(username=username).exists()
            counter += 1

        return new_username

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")

        username = self.generate_username(email)
        extra_fields.setdefault("username", username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_ACS = "acs"
    USER_TYPE_STUDENT = "student"
    USER_TYPE_EXTERNAL = "external"

    USER_TYPE_CHOICES = (
        (USER_TYPE_STUDENT, "student"),
        (USER_TYPE_ACS, "acs"),
        (USER_TYPE_EXTERNAL, "external"),
    )

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

    # Additional fields from the Student model
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=1, blank=True, null=True, choices=GENDER_CHOICES
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(
        max_length=255, blank=True, null=True, choices=PROGRAM_CHOICES
    )
    enrollment_date = models.DateField(blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    # Additional fields from the Acs model
    website = models.URLField(blank=True)

    # Additional fields from the External model
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_authorized_to_external = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.user_type}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.__class__.objects.generate_username(self.email)

        super().save(*args, **kwargs)

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

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Rating(models.Model):
    rated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings"
    )
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    rate = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} : rated : ({self.rate}) on user : {self.rated_user}"


class Contact(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
