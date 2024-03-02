from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("That email is not available")
        return email

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("That username is not available")
        return username

    def validate_password(self, password):
        password_minimum_length = 8
        if len(password) < password_minimum_length:
            raise serializers.ValidationError(
                f"Password minimum length allowed is {password_minimum_length}"
            )
        return password

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key != "password"
        }
        data["password"] = validated_data["password"]
        user = self.Meta.model.objects.create_user(**data)
        return user

    class Meta:
        model = get_user_model()
        ref_name = 'UserAccount'
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )
