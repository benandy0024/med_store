from django.shortcuts import render,redirect
from.forms import ProductForm
from django.views.generic import ListView,DetailView
from products.models import Product
# Create your views here.
def home(request):
    return render(request,'administration/home.html')
# def index(request):
#     return render(request,'administration/home.html')

class ProductListView(ListView):
    template_name ='administration/list_product.html'
    def get_queryset(self):
        self.request
        return Product.objects.all
def add_product(request):
    form=ProductForm(request.POST , request.FILES)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('administration:list')
    else:
        form=ProductForm()
    context={
        "form":form,
    }
    return render(request,'administration/add_product.html',context)

def update(request,slug):
    product_form=Product.objects.get(slug=slug)
    form=ProductForm(instance=product_form)
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES,instance=product_form)
        if form.is_valid():
            form.save()

            return redirect('administration:list')
    context={
        "form":form,
    }
    return render(request,'administration/add_product.html',context)
def delete(request,slug):
    product_form = Product.objects.get(slug=slug)
    if request.method=="POST":
        product_form.delete()
        return redirect('administration:list')
    context={
        "product":product_form
    }
    return render(request,'administration/delete.html',context)

