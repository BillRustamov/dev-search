from rest_framework import serializers

from main import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    # last_login = serializers.CharField(read_only=True)
    # groups = serializers.CharField(read_only=True)
    # user_permissions = serializers.CharField(read_only=True)
    updated = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    is_superuser = serializers.CharField(read_only=True)
    is_staff = serializers.CharField(read_only=True)

    class Meta:
        model = models.Profile
        # fields = '__all__'
        exclude = ['last_login', 'user_permissions', 'groups']

    def create(self, validated_data):
        password = validated_data.pop("password")
        profile = models.Profile.objects.create(**validated_data)
        profile.set_password(raw_password=password)
        profile.save()

        return profile

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            password = validated_data.pop("password")
            instance.set_password(raw_password=password)
            instance.save()

        return super().update(instance, validated_data)
