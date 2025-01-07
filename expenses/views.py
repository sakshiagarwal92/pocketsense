# expenses/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Expense, Group, Category, Settlement
from .serializers import ExpenseSerializer, GroupSerializer, CategorySerializer, SettlementSerializer
from rest_framework.permissions import IsAuthenticated

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
        
        # Handle the logic to create and split expenses.
        # Add your custom logic for equal or unequal split here.
        
        group = Group.objects.get(id=group_id)
        
        # Expense creation
        expense = Expense.objects.create(
            amount=amount,
            category_id=category_id,
            split_type=split_type,
            group=group,
            created_by=request.user
        )
        
        # Splitting logic
        if split_type == 'equal':
            # Split amount equally among all group members
            members = group.members.all()
            per_member_share = amount / len(members)
            for member in members:
                # Logic to add individual expense share for each member
                # For now, you could add an entry in a new model for each member's share
                pass  # Add logic for saving individual shares
        
        elif split_type == 'unequal':
            # Handle custom splitting logic if needed
            # For now, we can return a placeholder response
            pass
        
        return super().create(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user')

        # Ensure the user exists and is not already a member
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
        
        # Check if the settlement is already completed
        if settlement.payment_status == 'completed':
            return Response({'error': 'Expense already settled'}, status=status.HTTP_400_BAD_REQUEST)

        # Update payment status to 'completed'
        settlement.payment_status = 'completed'
        settlement.save()
        
        # Optionally, update the related expense's settlement status or other related models
        expense = settlement.expense
        # Perform additional logic (e.g., updating expense's status or creating records)
        
        return Response({'status': 'Settlement completed'}, status=status.HTTP_200_OK)
