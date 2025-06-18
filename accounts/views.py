import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView 
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from django.contrib.auth import login
from .forms import CreateUserForm 
from .forms import CustomerForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import ProfileUpdateForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile, Customer, Vendor
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, CustomerForm, VendorForm
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer, VendorSerializer, CustomerSerializer , UserSerializer # Serializer'ı içe aktar
from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import logging
from django.db.models import Q
import sqlite3
from django.db import connection
logger = logging.getLogger('custom')

#from axes.models import AccessAttempt
from django.contrib.auth import authenticate
# Register View
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        # 1. Serializer ile veriyi doğrula
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # 2. Kullanıcıyı oluştur
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        ip_address = request.META.get('REMOTE_ADDR')

        # AccessAttempt tablosunda bu kullanıcı ve IP için başarısız giriş sayısı
        failed_attempts = AccessAttempt.objects.filter(
            username=username,
            ip_address=ip_address,
            failures_since_start__gte=3,  # sınır neyse
            is_login_failure=True,
        )

        if failed_attempts.exists():
            return Response(
                {"detail": "Çok sayıda başarısız giriş denemesi nedeniyle hesabınız geçici olarak kilitlendi."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Normal authentication süreci
        response = super().post(request, *args, **kwargs)
        return response
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


# Profile Views
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    
    def render_to_response(self, context, **response_kwargs):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)


#@api_view(['POST'])
#@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])  # Bu sayede request.user dolu olur
#@method_decorator(csrf_exempt, name='dispatch')
def profile_create(request):
    if Profile.objects.filter(user=request.user).exists():
        return Response(
            {'error': 'Bu kullanıcıya ait zaten bir profil mevcut.'},
            status=400
        )

    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # user elle atanıyor
        return Response({'message': 'Profil başarıyla oluşturuldu'}, status=201)
    return Response(serializer.errors, status=400)


class ProfileDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, id=pk)
        if profile.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        profile.delete()
        return Response({"message": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
# Customer Views


@csrf_exempt
def CustomerCreateView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CustomerForm(data)
            if form.is_valid():
                customer = form.save()
                logger.info(f"{request.user.username} tarafından {customer.id} numaralı müşteri eklendi.")
                return JsonResponse({'message': 'Customer created successfully'}, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

class CustomerUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response({'message': 'Müşteri silindi.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_list(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vendor_create(request):
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def vendor_update(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=404)

    serializer = VendorSerializer(vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def vendor_delete(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=404)

    vendor.delete()
    return Response({'message': 'Satıcı silindi.'}, status=status.HTTP_200_OK)


# Search customers (for select2 or autocomplete functionality)
@csrf_exempt
@require_POST
@login_required
def get_customers(request):
    try:
        data = json.loads(request.body)
        term = data.get('term', '')
        customers = Customer.objects.filter(name__icontains=term)
        serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(serializer.data, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get('search', '').strip()
        if search:
            customers = Customer.objects.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        else:
            customers = Customer.objects.all()

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_list_vulnerable(request):
    search = request.GET.get("search", "")
    
    # SQL Injection'a açık sorgu
    raw_query = f"SELECT * FROM accounts_vendor WHERE name LIKE '%{search}%'"
    
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return Response(results)
