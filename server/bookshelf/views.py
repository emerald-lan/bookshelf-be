import os
from server import settings
from rest_framework import viewsets, permissions, generics
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        # print(settings.EMAIL_HOST_PASSWORD)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

            # Send email confirmation
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ GFG - Django Login!!"
            message = render_to_string('email_confirmation.html', {
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            return Response({"success": "Your account has been created successfully. Please check your email to confirm your email address."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Token is not valid, please request a new one"}, status=status.HTTP_401_UNAUTHORIZED)

            if user.is_active:
                return Response({"error": "This user has already been verified"}, status=status.HTTP_401_UNAUTHORIZED)
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been verified successfully!!")
            return Response({"success": "Your account has been verified successfully!!"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": "Token is not valid, please request a new one"}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Retrieve a user
    # GET /api/users/{id}/
    def retrieve(self, request, pk=None):
        # Admin can retrieve any user
        if (self.request.user.is_superuser):
            instance = User.objects.filter(id=pk).first()
            return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)
        
        # User can only retrieve their own information
        elif (self.request.user.id != int(pk)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            instance = self.request.user
            return Response(self.serializer_class(instance).data,
                            status=status.HTTP_200_OK)

    # Create a user or users
    # POST /api/users/
    def create(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update a user
    # PUT /api/users/{id}/
    def update(self, request, pk=None):
        # Admin can update any user
        if (self.request.user.is_superuser):
            instance = User.objects.filter(id=pk).first()
            serializer = self.serializer_class(instance=instance,
                                                data=request.data,
                                                )
        
        # User can only update their own information
        elif (self.request.user.id != int(pk)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            instance = self.request.user
            serializer = self.serializer_class(instance=instance,
                                                data=request.data,
                                                )
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a user
    # DELETE /api/users/{id}/
    def destroy(self, request, pk=None):
        # Admin can delete any user
        if (self.request.user.is_superuser):
            instance = User.objects.filter(id=pk).first()
        
        # User can only delete their own information
        elif (self.request.user.id != int(pk)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            instance = self.get_object()

        instance.delete()
        return Response(status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

