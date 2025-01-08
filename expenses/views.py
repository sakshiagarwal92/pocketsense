from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Expense, Group, Category, Settlement, IndividualExpense
from .serializers import ExpenseSerializer, GroupSerializer, CategorySerializer, SettlementSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import models
from datetime import datetime

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle expense recording and splitting logic.
        """
        amount = request.data.get('amount')
        category_id = request.data.get('category')
        split_type = request.data.get('split_type')
        group_id = request.data.get('group')

        group = Group.objects.get(id=group_id)

        date_str = request.data.get('date', None)
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format, expected YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            date_obj = timezone.now().date()  

        members = group.members.all()
        if not members:
            return Response(
                {"error": "Group has no members to split the expense."},
                status=status.HTTP_400_BAD_REQUEST
            )

        expense = Expense.objects.create(
            amount=amount,
            category_id=category_id,
            split_type=split_type,
            group=group,
            created_by=request.user, 
            date=date_obj  
        )

        if split_type == 'equal':
            per_member_share = amount / len(members)
            for member in members:
               
                IndividualExpense.objects.create(
                    expense=expense,
                    member=member,
                    amount=per_member_share
                )
        elif split_type == 'unequal':
            pass  

        serializer = self.get_serializer(expense)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user in group.members.all():
            return Response({'error': 'User is already a member'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.add(user)
        return Response({'status': 'Member added successfully'}, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def settle_expense(self, request, pk=None):
        settlement = self.get_object()
        
        if settlement.payment_status == 'completed':
            return Response({'error': 'Expense already settled'}, status=status.HTTP_400_BAD_REQUEST)

        settlement.payment_status = 'completed'
        settlement.save()
        
        expense = settlement.expense
        
        return Response({'status': 'Settlement completed'}, status=status.HTTP_200_OK)
