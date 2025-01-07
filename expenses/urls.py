# expenses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, GroupViewSet, CategoryViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'settlements', SettlementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
