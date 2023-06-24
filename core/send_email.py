from django.core.mail import send_mail, BadHeaderError, send_mass_mail, EmailMessage
from core.models import CustomUser
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from acs.models import JobPost
from ashop.models import Product

from_email = settings.EMAIL_HOST_USER


@shared_task
def send_application_email(job_id, user_id):
    job = JobPost.objects.get(id=job_id)
    user = CustomUser.objects.get(id=user_id)

    subject = "New Job Application"
    body = f"A new job application has been submitted.\nJob Title: {job.title}\nUser Email: {user.email}"

    acs_users = CustomUser.objects.filter(user_type="acs")

    for acs_user in acs_users:
        to_email = acs_user.email

    try:
        email = EmailMessage(subject, body, from_email, [to_email])
        email.send()
    except BadHeaderError:
        pass
    return


# @shared_task
# def send_product_order_email(product_id, buyer_id):
#     product = Product.objects.get(id=product_id)
#     buyer = CustomUser.objects.get(id=buyer_id)

#     subject = "A new Order has been placed"
#     body = f"A new order has been place: \n On product : {product.name} \n Customer/ Buyer : {buyer.email} \n"

#     seller = CustomUser.objects.filter(id=product.seller.id)

#     to_email = seller.user.email

#     try:
#         email = EmailMessage(subject, body, from_email, [to_email])
#         email.send()
#     except BadHeaderError:
#         pass
#     return
