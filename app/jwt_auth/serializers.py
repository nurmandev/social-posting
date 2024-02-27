from rest_framework import serializers

from db_schema.models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "label"]

class UserInfoSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = UserInfo
        fields = ["name", "last_name", "first_name", "name_furi", "last_name_furi", "first_name_furi", "phone", "role"]
        
class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "user_id", 'email', "user_info", "created_at", "updated_at", 'is_active', 'permission']
        
        