from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

# whenever you're outputing any messages in the python code that
# going to be output to the screen it's a good to pass through
# this translation system


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object """

    class Meta:
        model = get_user_model()  # returns user model class
        fields = ("email", "password", "name")

        # for extra settings in ModelSerializer

        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

        def create(self, validated_data):
            """ create a new user with encrypted password and return it"""
            return get_user_model().objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            """Update a user, setting the password correctly and return it"""
            # remove password after it has been retrieved
            password = validated_data.pop("password", None)
            user = super().update(instance, validated_data)
            if password:
                user.set_password(password)
                user.save()
            return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )  # access context of request
        if not user:
            msg = _("unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user

        return attrs


# pass this request context into viewSet
# ViewSet will pass the context into the serializer and then into this class
