# views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics, status, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer, ChangePasswordSerializer, UsersSerializer, UserProfileSerializer

User = get_user_model()
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserRegistrationView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
            email_sub = "Confirm Your Account"
            email_body = render_to_string('account_confirmation.html',{'confirm_link': confirm_link,})
            email = EmailMultiAlternatives(email_sub, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({"message": "User created successfully", "token": token}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def isActivate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return Response({"message": "Account confirmed successfully"}, status=status.HTTP_200_OK)
        return redirect('login')
    else:
        return redirect('register')

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_no = serializer.validated_data['phone_no']
            password = serializer.validated_data['password']
            user = authenticate(
                phone_no=phone_no,
                password=password,
            )
        
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutView(APIView):
    def get(self, request):
        try:
            # Check if the user has an associated token
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            # Token does not exist, handle the situation if needed
            pass
        
        # Perform Django's logout
        logout(request)
        
        # Redirect to the login page or any other page
        return redirect('login')         

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request, *args, **kwargs):
        """
        This action allows the user to retrieve or update their own profile.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        if request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(request.user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        # Optional: Add logic to ensure that the requesting user can delete the specified user
        if user != request.user and not request.user.is_superuser:
            return Response({'detail': 'Not authorized to delete this user.'}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
