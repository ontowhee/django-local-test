from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookForm

from .models import Book

def index(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'books/index.html', context)


def create_book(request):
    if request.method == 'POST':
        name = request.GET.get("name")
        form = BookForm(request.POST, name)
        if form.is_valid():
            form.save()
            messages.success(request, 'New book added successfully!')
            return redirect('books:index')
    else:
        form = BookForm()

    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)
