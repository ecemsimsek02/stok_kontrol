from rest_framework import serializers
from .models import Profile, Vendor, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']  # Güvenli şekilde şifre oluşturur
        )
        user.is_staff = True       # Admin paneline erişim için
        user.is_superuser = True   # Süper kullanıcı yetkisi (opsiyonel)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Profile modelini JSON formatına çeviren serializer."""
    user = UserSerializer(read_only=True)  # Kullanıcı bilgilerini içerecek
    image_url = serializers.SerializerMethodField()  # Profil resminin URL'sini ekler

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'slug', 'profile_picture', 'image_url',
            'telephone', 'email', 'first_name', 'last_name', 
            'status', 'role'
        ]
    
    def get_image_url(self, obj):
        """Profil resminin tam URL'sini döndürür."""
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return request.build_absolute_uri(obj.profile_picture.url)
        return None


class VendorSerializer(serializers.ModelSerializer):
    """Vendor modelini JSON formatına çeviren serializer."""
    
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'slug', 'phone_number', 'address']


class CustomerSerializer(serializers.ModelSerializer):
    """Customer modelini JSON formatına çeviren serializer."""
    full_name = serializers.SerializerMethodField()  # Tam isim için özel alan ekledik

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'address', 'email', 'phone', 'loyalty_points'
        ]
    
    def get_full_name(self, obj):
        """Müşterinin tam adını döndürür."""
        return obj.get_full_name()
