from server import settings
from rest_framework import viewsets, permissions, generics, authentication
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
from rest_framework.authtoken.models import Token

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
            token = Token.objects.create(user=user)
            print(token.key)
            # Send email confirmation
            # current_site = get_current_site(request)
            email_subject = "Confirm your Bookshelf Login!!"
            message = render_to_string('email_confirmation.html', {
                # 'domain': current_site.domain,
                'domain': 'localhost:3000',
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
        except Exception:
            return Response({"error": "Token is not valid, please request a new one"}, status=status.HTTP_401_UNAUTHORIZED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        print(request.data)
        user = authenticate(username=self.request.data['username'], password=self.request.data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                print(token.key)
                messages.success(request, "Logged In Sucessfully!!")
                return Response({"success": "Logged In Sucessfully!!", "user_id": request.user.id, "token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account is not active, please verify your email"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        logout(request)
        messages.success(request, "Logged Out Successfully!!")
        return Response({"success": "Logged Out Successfully!!"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes=[authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Create a user or users
    # POST /api/users/
    def create(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Create a book or books
    # POST /api/books/
    def create(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CheckoutView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        # print(request.data)
        user = User.objects.get(id=request.data['user_id'])
        order = Order.objects.create(customer=user, total=request.data['total'])
        
        if order:
            for index, item in enumerate(request.data['order_items']):
                book = Book.objects.get(id=item)
                order_item = OrderItem.objects.create(order=order, book=book, quantity=request.data['quantity'][index])
                book.stock -= int(request.data['quantity'][index])
                book.save()

            email_subject = "A receipt of your order from Bookshelf"
            message = render_to_string('email_checkout.html', {
                'order': order,
                'order_items': OrderItem.objects.filter(order=order),
            })
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            return Response({"success": "Your Order has been placed successfully!!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)
        

# class PurchaseList(generics.ListAPIView):
#     serializer_class = OrderItemSerializer

#     def get_queryset(self):
#         payload = []

#         user = self.request.user
#         orders = Order.objects.filter(customer=user)

#         for order in orders:
#             order_items = OrderItem.objects.filter(order=order)
#             print(Order.objects.all())
#             payload.append(order_items)

#         return payload
