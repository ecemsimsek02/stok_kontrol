from rest_framework import viewsets
from rest_framework.response import Response
from .models import CashRegister, Transaction, Expense
from .serializers import CashRegisterSerializer, TransactionSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .permissions import IsAdminUserRole

class CashRegisterViewSet(viewsets.ModelViewSet):
    queryset = CashRegister.objects.all()
    serializer_class = CashRegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def list(self, request, *args, **kwargs):
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)
        print("Staff:", request.user.is_staff)
        print("Superuser:", request.user.is_superuser)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        cash_register = serializer.save()
        cash_register.reset_balance()  # Reset balance at the start of the day

class CashRegisterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashRegister.objects.all()
    serializer_class = CashRegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_serializer_context(self):
        return {"request": self.request}

    
    

    

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def perform_create(self, serializer):
        expense = serializer.save()
        # You can add logic to update the total expenses if needed.
