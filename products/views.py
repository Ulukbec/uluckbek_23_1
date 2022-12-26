from django.shortcuts import HttpResponse, render, redirect

from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Products, Category, Review


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
            'categories': product.category.all(),
            'category_form': ReviewCreateForm
        }
        return render(request, 'products/detail.html', context=data)

    if request.method == "POST":
        product = Products.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                product_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'categories': product.category.all(),
                'category_form': form,
                'review': product.review.all()
            })


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        context = {
            'categories': categories.all()
        }

        return render(request, 'categories/index.html', context=context)


def product_creat_view(request):
    if request.method == 'GET':
        return render(request, 'products/create.html', context={
            "form": ProductCreateForm
        })

    if request.method == "POST":
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Products.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price', 0),
                review_table=form.cleaned_data.get('review_table', True)
            )

            return redirect('/products/')
        else:
            return render(request, 'products/create.html', context={
                "form": form
            })
