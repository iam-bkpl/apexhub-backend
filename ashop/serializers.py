from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from ashop.models import (
    Category,
    Comment,
    OrderItem,
    Payment,
    Product,
    ProductImage,
)
from core.serializers import CustomUserSerializer
from core.models import CustomUser

# from core.send_email import send_product_order_email


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ["id", "image"]


# class RatingSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Rating
#         fields = ["id", "rate", "user_id", "date_added"]

#     def create(self, validated_data):
#         product_id = self.context["product_id"]
#         user_id = self.context["user_id"]
#         return Rating.objects.create(
#             product_id=product_id, user_id=user_id, **validated_data
#         )


class CommentSerialier(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user_id", "text", "date_added"]

    def create(self, validated_data):
        user_id = self.context["user_id"]
        product_id = self.context["product_id"]

        return Comment.objects.create(
            user_id=user_id, product_id=product_id, **validated_data
        )


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    comments = CommentSerialier(many=True, read_only=True)
    seller = CustomUserSerializer(read_only=True)
    slug = serializers.ReadOnlyField()
    # category = CategorySerializer(read_only=True)
    qr_code = serializers.FileField(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "name",
            "slug",
            "description",
            "price",
            "date_added",
            "is_active",
            "qr_code",
            "images",
            "comments",
            "category",
        ]

    def create(self, validated_data):
        validated_data["seller_id"] = self.context["seller_id"]
        return super().create(validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "seller"]


# class OrderItemSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer()
#     class Meta:
#         model = OrderItem
#         fields = ['id','product','quantity','price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    buyer = CustomUserSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "buyer", "product", "date", "payment_status", "paid"]

    def create(self, validated_data):
        buyer_id = self.context.get("buyer_id")
        product_id = self.context.get("product_id")

        try:
            # Check if an order already exists for the given product and buyer
            existing_order = OrderItem.objects.get(
                product_id=product_id, buyer_id=buyer_id
            )
            raise serializers.ValidationError(
                "Order has already been placed for this product."
            )
        except ObjectDoesNotExist:
            # send_product_order_email(product_id, buyer_id)
            return OrderItem.objects.create(
                buyer_id=buyer_id, product_id=product_id, **validated_data
            )


# class GetOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['id','product_id',;]


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderItemSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "order", "payment_method", "amount", "proof"]

    def create(self, validated_data):
        # buyer =  CustomUser.objects.get(id= self.context['buyer_id'])
        # order = OrderItem.objects.get(id=self.context['order_id'])
        buyer_id = self.context["buyer_id"]
        order_id = self.context["order_id"]

        order_item = OrderItem.objects.filter(id=order_id)
        # validated_data['amount'] = order_item.product.price

        return Payment.objects.create(
            buyer_id=buyer_id, order_id=order_id, **validated_data
        )
