from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .forms import TeaForm
from .models import TeaCategory, Origin, Tea, Order, OrderItem
from .serializers import (
    TeaCategorySerializer,
    OriginSerializer,
    TeaSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserRegistrationSerializer,
)

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


def _has_view_permission(user, model):
    return user.has_perm(f"{model._meta.app_label}.view_{model._meta.model_name}")


def _required_perm_for_method(method, model):
    if method == "GET":
        action = "view"
    elif method == "POST":
        action = "add"
    elif method in ["PUT", "PATCH"]:
        action = "change"
    elif method == "DELETE":
        action = "delete"
    else:
        return None
    return f"{model._meta.app_label}.{action}_{model._meta.model_name}"


def _check_model_permission(request, model):
    perm = _required_perm_for_method(request.method, model)
    if not perm:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not request.user.has_perm(perm):
        return Response(
            {"detail": "Brak uprawnien do tej operacji."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tea_list(request):
    permission_error = _check_model_permission(request, Tea)
    if permission_error:
        return permission_error

    if request.method == "GET":
        teas = Tea.objects.all()
        serializer = TeaSerializer(teas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = TeaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tea_detail(request, pk):
    permission_error = _check_model_permission(request, Tea)
    if permission_error:
        return permission_error

    try:
        tea = Tea.objects.get(pk=pk)
    except Tea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeaSerializer(tea)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tea_update_delete(request, pk):
    permission_error = _check_model_permission(request, Tea)
    if permission_error:
        return permission_error

    try:
        tea = Tea.objects.get(pk=pk)
    except Tea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = TeaSerializer(tea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    tea.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    permission_error = _check_model_permission(request, TeaCategory)
    if permission_error:
        return permission_error

    if request.method == "GET":
        categories = TeaCategory.objects.all()
        serializer = TeaCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = TeaCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    permission_error = _check_model_permission(request, TeaCategory)
    if permission_error:
        return permission_error

    try:
        category = TeaCategory.objects.get(pk=pk)
    except TeaCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TeaCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = TeaCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def origin_list(request):
    permission_error = _check_model_permission(request, Origin)
    if permission_error:
        return permission_error

    if request.method == "GET":
        origins = Origin.objects.all()
        serializer = OriginSerializer(origins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = OriginSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def origin_detail(request, pk):
    permission_error = _check_model_permission(request, Origin)
    if permission_error:
        return permission_error

    try:
        origin = Origin.objects.get(pk=pk)
    except Origin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OriginSerializer(origin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = OriginSerializer(origin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    origin.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    permission_error = _check_model_permission(request, Order)
    if permission_error:
        return permission_error

    if request.method == "GET":
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    permission_error = _check_model_permission(request, Order)
    if permission_error:
        return permission_error

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save(user=order.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_item_list(request):
    permission_error = _check_model_permission(request, OrderItem)
    if permission_error:
        return permission_error

    if request.method == "GET":
        items = OrderItem.objects.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = OrderItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_item_detail(request, pk):
    permission_error = _check_model_permission(request, OrderItem)
    if permission_error:
        return permission_error

    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrderItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def teas_search(request):
    if not _has_view_permission(request.user, Tea):
        return Response({"detail": "Brak uprawnien do podgladu herbat."}, status=status.HTTP_403_FORBIDDEN)

    name = request.query_params.get("name")
    if not name:
        return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)

    teas = Tea.objects.filter(name__icontains=name)
    serializer = TeaSerializer(teas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders_my(request):
    if not _has_view_permission(request.user, Order):
        return Response({"detail": "Brak uprawnien do podgladu zamowien."}, status=status.HTTP_403_FORBIDDEN)

    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Proste widoki HTML w stylu z projektu wzorcowego
def tea_list_html(request):
    teas = Tea.objects.all()
    return render(request, "teastore/tea/list.html", {"teas": teas})


def tea_detail_html(request, id):
    try:
        tea = Tea.objects.get(id=id)
    except Tea.DoesNotExist:
        raise Http404("Obiekt Tea o podanym id nie istnieje.")

    if request.method == "GET":
        return render(request, "teastore/tea/detail.html", {"tea": tea})

    if request.method == "POST":
        tea.delete()
        return redirect("tea-list-html")

    return redirect("tea-list-html")


def tea_create_html(request):
    if request.method == "POST":
        form = TeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tea-list-html")
    else:
        form = TeaForm()

    return render(request, "teastore/tea/create.html", {"form": form})
