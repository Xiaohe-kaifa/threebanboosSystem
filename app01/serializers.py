from .models import LoginInformation,CommodityInformation,OrdersInformation,CartItem,ChatMessageInformation, suggestionInformation,BusinessInformation
from rest_framework import serializers
from django.db import models




order_commodity_type_choices = (
        (0,'竹编家具'),
        (1,'工艺品'),
    )
class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrdersInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['order_commodity_type'] = dict(order_commodity_type_choices).get(representation['order_commodity_type'])
        return representation

commodityType_choices = (
        (0,'竹编家具'),
        (1,'工艺品'),
    )
class CommoditySerializers(serializers.ModelSerializer):
    class Meta:
        model = CommodityInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['commodityType'] = dict(commodityType_choices).get(representation['commodityType'])
        return representation

chatType_choices = (
        (1,'个人'),
        (0,'全部'),
    )
class ChatMessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChatMessageInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['chatType'] = dict(chatType_choices).get(representation['chatType'])
        return representation

business_agree_choices = (
        (1,'未读'),
        (0,'已同意'),
    )
class BusinessSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusinessInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['business_agree'] = dict(business_agree_choices).get(representation['business_agree'])
        return representation

username_type_choices = (
        (0,'管理员'),
        (1,'用户'),
        (2,'商家'),
        (3,'客服'),
    )
gender_choices = (
        (1,'男'),
        (0,'女'),
    )
status_choices = (
        (1,'在线'),
        (0,'离线'),
    )

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = LoginInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['gender'] = dict(gender_choices).get(representation['gender'])
        representation['status'] = dict(status_choices).get(representation['status'])
        representation['username_type'] = dict(username_type_choices).get(representation['username_type'])
        return representation


class SuccessSerializers(serializers.ModelSerializer):
    class Meta:
        model = LoginInformation
        fields = ['username','id']
feedback_status_choices = (
        (1,'已读'),
        (0,'未读'),
    )
feedback_choices = (
        (0,'产品方向'),
        (1,'技术方向'),
    )
class suggestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = suggestionInformation
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['feedback_status'] = dict(feedback_status_choices).get(representation['feedback_status'])
        representation['feedback'] = dict(feedback_choices).get(representation['feedback'])
        return representation

class CartItemSerializers(serializers.ModelSerializer):
    cart_commodity = CommoditySerializers()
    class Meta:
        model = CartItem
        fields = "__all__"
class PostCartItemSerializers(serializers.ModelSerializer):
    # cart_commodity = CommoditySerializers()
    class Meta:
        model = CartItem
        fields = "__all__"

    
