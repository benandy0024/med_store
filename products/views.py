from django.shortcuts import render,get_object_or_404,Http404
from django.views.generic import ListView,DetailView
from .models import Product,Category
from carts.models import Cart,CartItem
from analytics.mixin import ObjectViewedMixin
# Create your views here.
def home(request):
    qs=Product.objects.all()[1:3]
    cat=Category.objects.all()
    for item in qs:
        print(item.category.all())
    context={
        'qs':qs,
        'cat':cat
    }
    return render(request,'medecine/home.html',context)
class ProductListView(ListView):
    template_name = 'medecine/new_list_view.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs, )
        cat = Category.objects.all()
        context['cat'] = cat
        return context
#ObjectViewedMixin
class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset =  Product.objects.all()
    template_name = 'medecine/detail_view.html'
    def get_context_data(self,*args, **kwargs,):
        context=super(ProductDetailView, self).get_context_data(*args, **kwargs,)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        cartitem=cart_obj.cartitem_set.all()
        context['carts']=cart_obj
        return context

    #raise Http404 error
    def get_object(self, queryset=None, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:

            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            #  get_by_id(slug) model manager method
            qs = Product.objects.get_by_id(slug)
            instance = qs.first()
        except:
            raise Http404('hmmmm')

        return instance