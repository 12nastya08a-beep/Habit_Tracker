from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(write_only=True, min_length=6)
  password_confirmation = serializers.CharField(write_only=True)

  first_name = serializers.CharField(required=False, allow_blank=True)
  last_name = serializers.CharField(required=False, allow_blank=True)

  class Meta:
    model = User
    fields = (
        'username',
        'email',
        'password',
        'password_confirmation',
        'first_name',
        'last_name',
    )

  def validate(self, attrs):
    if attrs.get('password') != attrs.get('password_confirmation'):
      raise serializers.ValidationError(
          {'password_confirmation': 'Паролі не збігаються.'}
      )
    return attrs

  def create(self, validated_data):
    validated_data.pop('password_confirmation', None)
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        first_name=validated_data.get('first_name', ''),
        last_name=validated_data.get('last_name', ''),
    )
    return user
