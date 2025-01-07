from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    # Add your custom fields here
    college = models.CharField(max_length=255, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)
    default_payment_methods = models.CharField(max_length=255, blank=True, null=True)

    # Override groups and permissions relationships to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    split_type = models.CharField(max_length=50, choices=[('equal', 'Equal'), ('unequal', 'Unequal')])
    date = models.DateField(default=timezone.now)  # Correct usage
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    group_type = models.CharField(max_length=50, choices=[
        ('hostel_roommates', 'Hostel Roommates'),
        ('project_teams', 'Project Teams'),
        ('trip_groups', 'Trip Groups')
    ])


class Settlement(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="settlements")
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    settlement_method = models.CharField(max_length=50)
    due_date = models.DateField()


class IndividualExpense(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="individual_expenses")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="individual_expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.member.username} owes {self.amount} for {self.expense}"
