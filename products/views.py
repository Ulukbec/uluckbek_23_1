from django.shortcuts import HttpResponse, render, redirect

from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Products, Category, Review

# Create your views here.

PAGINTIONS_LIMIT = 6


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        categories_id = int(request.GET.get("category_id", 0))
        search = request.GET.get("Search")
        page = int(request.GET.get("page", 1))

        if categories_id:
            product = Products.objects.filter(category__in=[categories_id])
        else:
            product = Products.objects.all()

        if search:
            product = product.filter(title__icontains=request.GET.get('Search'))

        max_page = product.__len__() / PAGINTIONS_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        product = product[PAGINTIONS_LIMIT * (page - 1): PAGINTIONS_LIMIT * page]

        return render(request, 'products/products.html', context={
            'products': product,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, round(max_page) + 1)
        })


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)
        data = {
            'product': product,
            'review': product.review.all(),
            'categories': product.category.all(),
            'form': ReviewCreateForm,
            'user': None if request.user.is_anonymous else request.user
        }
        return render(request, 'products/detail.html', context=data)

    if request.method == "POST":
        product = Products.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                user=request.user,
                product_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'categories': product.category.all(),
                'form': form,
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
                user=request.user,
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
