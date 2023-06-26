from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from core.models import CustomUser, Rating


class UserCreateSerializer(BaseUserCreateSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    def create(self, validated_data):
        user_type = validated_data.get("user_type")
        user = super().create(validated_data)

        # if user_type == CustomUser.USER_TYPE_STUDENT:
        #     student_data = {
        #         "user": user,
        #     }
        #     student = Student.objects.create(**student_data)
        #     return user

        # elif user_type == CustomUser.USER_TYPE_EXTERNAL:
        #     external_data = {
        #         "user": user,
        #     }
        #     external = External.objects.create(**external_data)
        #     return user

        # elif user_type == CustomUser.USER_TYPE_ACS:
        #     acs_data = {
        #         "user": user,
        #     }
        #     acs = Acs.objects.create(**acs_data)
        #     return user

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


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "gender",
            "address",
            "program",
            "enrollment_date",
            "is_seller",
            "ratings",
        ]


class ExternalSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomUser
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
        model = CustomUser
        fields = ["id", "user", "website"]
