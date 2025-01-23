from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect

def index(request):
    # Database Query
    category_list = Category.objects.order_by('-likes')[:5] # Negative indicates descending order
    page_list = Page.objects.order_by('-views')[:5]

    # Create and populate the context_dict
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Render Response
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try: 
        # The .get() method raises DoesNotExist Error if cant return model instance
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve associated pages - list of associated pages or empty list
        pages = Page.objects.filter(category=category)

        # Populate context_dict
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    # Render Response
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            # If valid save to database
            form.save(commit=True)
            return redirect('/rango/')
        
        else:

            # Print errors to terminal
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

