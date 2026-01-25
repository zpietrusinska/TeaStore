from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import TeaCategory, Origin, Tea, Order, OrderItem
from .permissions import CustomDjangoModelPermissions
from .serializers import (
    TeaCategorySerializer,
    OriginSerializer,
    TeaSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserRegistrationSerializer,
)


class TeaCategoryViewSet(viewsets.ModelViewSet):
    queryset = TeaCategory.objects.all()
    serializer_class = TeaCategorySerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]


class OriginViewSet(viewsets.ModelViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]


class TeaViewSet(viewsets.ModelViewSet):
    queryset = Tea.objects.all()
    serializer_class = TeaSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]


def _ensure_user_group():
    group, _ = Group.objects.get_or_create(name="TeaStoreUser")
    model_perms = [
        (TeaCategory, ["view"]),
        (Origin, ["view"]),
        (Tea, ["view"]),
        (Order, ["add", "view"]),
        (OrderItem, ["add", "view"]),
    ]
    for model, perms in model_perms:
        content_type = ContentType.objects.get_for_model(model)
        for perm in perms:
            codename = f"{perm}_{model._meta.model_name}"
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            group.permissions.add(permission)
    return group


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        group = _ensure_user_group()
        user.groups.add(group)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
