import ashop.models
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ashop.validators import file_size_validation
from apexhub.settings import AUTH_USER_MODEL
from ckeditor.fields import RichTextField


from django.utils.text import slugify
import random
import string
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", default="1"
    )
    is_featured = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it doesn't exist
            base_slug = slugify(self.name)
            timestamp_slug = timezone.now().strftime(
                "%Y%m%d%H%M"
            )  # Add timestamp component
            slug = f"{base_slug}-{timestamp_slug}"
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{timestamp_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class FeaturedProduct(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="product/images", validators=[file_size_validation]
    )

    def __str__(self):
        return self.product.name


class OrderItem(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    buyer = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orderitems"
    )
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="orderitems"
    )
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer} ordered and payment status is {self.payment_status}"


class Payment(models.Model):
    PAYMENT_METHOD_WALLET = "wallet"
    PAYMENT_METHOD_BANK_TRANSFER = "bank_transfer"
    PAYMENT_METHOD_CASH_IN_HAND = "cash_in_hand"

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_WALLET, "Wallet Payments"),
        (PAYMENT_METHOD_BANK_TRANSFER, "Bank Transfer"),
        (PAYMENT_METHOD_CASH_IN_HAND, "Cash in Hand"),
    ]

    buyer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=255,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CASH_IN_HAND,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof = models.ImageField(upload_to="payment_bills", blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.buyer} | Order: {self.order}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order,
#         on_delete=models.PROTECT,
#         related_name='items'
#     )
#     product = models.ForeignKey(Product,
#                                 on_delete=models.PROTECT,
#                                 related_name='order_items')
#     quantity = models.PositiveSmallIntegerField()
#     price = models.DecimalField(max_digits=6, decimal_places=2)

#     def __str__(self):
#         return f"{self.order}"


# class Rating(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name="ratings"
#     )
#     rate = models.IntegerField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} rated {self.rate} on {self.product}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} commented on {self.product}"
