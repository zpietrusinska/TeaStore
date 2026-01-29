from django import forms

from .models import Tea, TeaCategory, Origin, Order, OrderItem


class TeaForm(forms.ModelForm):
    class Meta:
        model = Tea
        fields = "__all__"


class TeaCategoryForm(forms.ModelForm):
    class Meta:
        model = TeaCategory
        fields = "__all__"


class OriginForm(forms.ModelForm):
    class Meta:
        model = Origin
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["delivery_date"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ["unit_price"]
