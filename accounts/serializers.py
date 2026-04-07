from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(view_name='api-users-detail')

    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        source='groups',
        required=False
    )

    class Meta:
        model = UserModel
        fields = ['id', 'url', 'username', 'email', 'first_name', 'last_name', 'academic_rank', 'groups', 'group_ids']

    def update(self, instance, validated_data):
        if 'groups' in validated_data:
            groups = validated_data.pop('groups')
            instance.groups.set(groups)
        return super().update(instance, validated_data)