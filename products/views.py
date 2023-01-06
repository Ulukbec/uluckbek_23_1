from django.shortcuts import render, redirect

from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Products, Category, Review
from django.views.generic import ListView, CreateView, DetailView

# Create your views here.

PAGINATION_LIMIT = 6


# def main_view(request):
#     if request.method == 'GET':
#         return render(request, 'layouts/index.html')


class MainView(ListView):
    model = Review
    template_name = 'layouts/index.html'


class ProductCBV(ListView):
    queryset = Products.objects.all()
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'products': kwargs['products'],
            'max_page': kwargs['max_page'],
            'user': kwargs['user'],
        }

    def get(self, request, **kwargs):
        categories_id = int(request.GET.get("category_id", 0))
        search = request.GET.get("Search")
        page = int(request.GET.get("page", 1))

        if categories_id:
            product = Products.objects.filter(category__in=[categories_id])
        else:
            product = Products.objects.all()

        if search:
            product = product.filter(title__icontains=search)

        max_page = product.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        product = product[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]

        return render(request, self.template_name, context=self.get_context_data(
            products=product,
            user=None if request.user.is_anonymous else request.user,
            max_page=range(1, round(max_page) + 1)
        ))


class CategoriesView(ListView):
    queryset = Category.objects.all()
    template_name = 'categories/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'categories': self.get_queryset()
        }


class PostCreate(CreateView):
    form_class = ProductCreateForm
    template_name = 'products/create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            Products.objects.create(
                user=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price', 0),
                review_table=form.cleaned_data.get('review_table', True)
            )
            return redirect('/products')

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            "form": self.form_class
        }


class ProductsDetailView(DetailView, CreateView):
    template_name = 'products/detail.html'

    def get(self, request, id=None, **kwargs):

        product = Products.objects.get(id=id)
        data = {
            'product': product,
            'review': product.review.all(),
            'categories': product.category.all(),
            'form': ReviewCreateForm,
            'user': None if request.user.is_anonymous else request.user
        }
        return render(request, 'products/detail.html', context=data)

    def post(self, request, id=None, **kwargs):

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
