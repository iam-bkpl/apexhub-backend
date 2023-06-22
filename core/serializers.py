from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from core.models import Acs, CustomUser, External, Student, Rating


class UserCreateSerializer(BaseUserCreateSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    def create(self, validated_data):
        user_type = validated_data.get("user_type")
        user = super().create(validated_data)

        if user_type == CustomUser.USER_TYPE_STUDENT:
            student_data = {
                "user": user,
            }
            student = Student.objects.create(**student_data)
            return user

        elif user_type == CustomUser.USER_TYPE_EXTERNAL:
            external_data = {
                "user": user,
            }
            external = External.objects.create(**external_data)
            return user

        elif user_type == CustomUser.USER_TYPE_ACS:
            acs_data = {
                "user": user,
            }
            acs = Acs.objects.create(**acs_data)
            return user

        return user

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "email", "password", "user_type"]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "email", "password", "user_type"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "contact", "user_type"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "gender",
            "address",
            "program",
            "enrollment_date",
        ]


class ExternalSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = External
        fields = [
            "id",
            "user",
            "name",
            "address",
            "phone_number",
            "website",
            "description",
        ]


class AcsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Acs
        fields = ["id", "user", "website"]


class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "rate", "user_id", "date_added"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        user_id = self.context["user_id"]
        return Rating.objects.create(
            product_id=product_id, user_id=user_id, **validated_data
        )
