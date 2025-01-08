from datetime import datetime, timezone
from rest_framework import serializers
from .models import Expense, Group, Category, Settlement, User

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'split_type', 'date', 'receipt_image', 'created_by', 'group']
        extra_kwargs = {
            'created_by': {'read_only': True},
        }
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        if 'date' not in validated_data:
            validated_data['date'] = datetime.now()  
        return super().create(validated_data)
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'group_type']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['id', 'expense', 'payment_status', 'settlement_method', 'due_date']
