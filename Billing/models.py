from django.db import models
from accounts.models import GuestEmail
from django.db import models
from django.conf import settings
from  django.db.models.signals import post_save,pre_save
import stripe
# Create your models here.
stripe.api_key="sk_test_HBJfc8IKGbe6DDjcIA2Jl8P900NGSbqtBI"
User=settings.AUTH_USER_MODEL
# Create your models here.
class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        created=False
        obj=None
        if user.is_authenticated:
            # logged in user checkout ;remember payement stuff
            obj, created=self.model.objects.get_or_create(
                user=user, email=user.email
            )
        elif guest_email_id is not None:
            # logged in user checkout, auto reload  payement stuff
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = BillingProfile.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj,created
class BillingProfile(models.Model):
    user=models.OneToOneField(User,unique=True,null=True,blank=True,on_delete='CASCADE')
    email=models.EmailField()
    active=models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id=models.CharField(max_length=120,null=True,blank=True)
    objects=BillingProfileManager()

    def __str__(self):
        return self.email
def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        print("Actual api request send to stripe/braintree")
        customer=stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id=customer.id
pre_save.connect(billing_profile_created_receiver,sender=BillingProfile)

def user_creaeted_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)
post_save.connect(user_creaeted_receiver,sender=User)
