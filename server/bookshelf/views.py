from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    fname = request.data.get('firstName')
    lname = request.data.get('lastName')
    email = request.data.get('email')
    password = request.data.get('password')
    repeated_password = request.data.get('repeatedPassword')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists. Please try a different username."})

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."})

    if len(username) > 20:
        return Response({"error": "Username must be under 20 characters."})

    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters."})
    
    if password != repeated_password:
        return Response({"error": "Passwords do not match."})

    if not username.isalnum():
        return Response({"error": "Username must be alphanumeric."})

    user = User(username=username, email=email, first_name=fname, last_name=lname)
    user.set_password(password)
    user.is_active = False
    user.save()

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

