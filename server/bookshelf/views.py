from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


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
            instance = self.get_object()
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
            instance = self.get_object()
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

    def get_object(self):
        return self.request.user


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

