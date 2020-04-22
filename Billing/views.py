from django.shortcuts import render,redirect
from  django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from accounts.forms import LoginForm,RegisterForm,GuestForm
from accounts.models import GuestEmail
import stripe

# Create your views here.
def guest_register_page(request):
    form=GuestForm(request.POST or None)
    context = {
        'form': form,
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
        email=form.cleaned_data.get("email")
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
    return redirect('accounts:register')

stripe.api_key="sk_test_HBJfc8IKGbe6DDjcIA2Jl8P900NGSbqtBI"
published_key="pk_test_QZinzyFakYCKsVwpJI0ttgBC00VIepUNf2"
def payment_method_view(request):
    context={
        "published_key":published_key,
    }
    return render(request,"payment_method.html",context)


def payment_method_create_view(request):
    if request.method=="POST" and request.is_ajax():
        return JsonResponse({"message:done"})
    return HttpResponse("error")