from django.shortcuts import HttpResponse, render
from products.models import Products, Category


# Create your views here.

def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        categories_id = int(request.GET.get("category_id", 0))

        if categories_id:
            product = Products.objects.filter(category__in=[categories_id])
        else:
            product = Products.objects.all()
        return render(request, 'products/products.html', context={
            'products': product
        })


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)
        data = {
            'product': product,
            'review': product.review.all(),
            'categories': product.category.all()
        }
        return render(request, 'products/detail.html', context=data)


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        context = {
            'categories': categories.all()
        }

        return render(request, 'categories/index.html', context=context)
