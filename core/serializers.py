import django.db.models
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from core.models import CustomUser, Rating
from core.models import Contact


class UserCreateSerializer(BaseUserCreateSerializer):
    # user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "email", "password", "user_type"]
        # fields = "__all__"
        # fields = [
        #     "id",
        #     "email",
        #     "username",
        #     "contact",
        #     "user_type",
        #     "avatar",
        #     "is_active",
        #     "is_staff",
        #     "is_admin",
        #     "is_superuser",
        #     "last_login",
        #     "first_name",
        #     "last_name",
        #     "gender",
        #     "program",
        #     "is_seller",
        #     "name",
        #     "address",
        #     "phone",
        #     "website",
        #     "description",
        #     "is_authorized_to_external",
        # ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "email", "password", "user_type", "first_name"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "contact",
            "user_type",
            "avatar",
            "is_active",
            "is_staff",
            "is_admin",
            "is_superuser",
            "last_login",
            "first_name",
            "last_name",
            "is_seller",
            "name",
            "address",
            "phone",
            "website",
            "description",
            "is_authorized_to_external",
        ]


class RatingSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(read_only=True)
    # rated_user = CustomUserSerializer(read_only=True)
    # rater = CustomUserSerializer(read_only=True)
    rated_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "rated_user", "rate", "date_added"]

    def create(self, validated_data):
        rated_user_id = self.context["rated_user_id"]
        rater_id = self.context["rater_id"]
        return Rating.objects.create(
            rated_user_id=rated_user_id, rater_id=rater_id, **validated_data
        )


# class StudentSerializer(serializers.ModelSerializer):
#     rate = serializers.SerializerMethodField()


class StudentSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    def get_rate(self, student):
        ratings = student.ratings.all()
        rate_count = ratings.count()
        total_rate = sum(rating.rate for rating in ratings)

        if rate_count > 0:
            average_rate = total_rate / rate_count
            rounded_rate = round(average_rate, 1)
            return rounded_rate

        return total_rate

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "avatar",
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
            "address",
            "program",
            "is_seller",
            "rate",
        ]


class ExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "website",
            "description",
        ]

    def create(self, validated_data):
        return CustomUser.objects.create(
            user_type=CustomUser.USER_TYPE_EXTERNAL, **validated_data
        )


class AcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "website", "is_authorized_to_external"]

    def create(self, validated_data):
        return CustomUser.objects.create(
            user_type=CustomUser.USER_TYPE_ACS, **validated_data
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
        ]
