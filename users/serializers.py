from rest_framework import serializers
from users.models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    company = serializers.CharField(min_length=20, read_only=True)
    firstName = serializers.CharField(min_length=20, read_only=True)
    lastName = serializers.CharField(min_length=20, read_only=True)
    github = serializers.CharField(min_length=150, read_only=True)
    linkedIn = serializers.CharField(min_length=150, read_only=True)


    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password', 'type', 'id', 'company', 'firstName', 'lastName', 'github', 'linkedIn')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, read_only=True)
    company = serializers.CharField(min_length=20, read_only=True)
    firstName = serializers.CharField(min_length=20, read_only=True)
    lastName = serializers.CharField(min_length=20, read_only=True)
    class Meta:
        model = NewUser
        # fields = ('email', 'user_name', 'type', 'id', 'company', 'firstName', 'lastName', )
        fields = '__all__'
