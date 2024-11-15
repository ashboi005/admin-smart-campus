from django.shortcuts import render, redirect
from .models import Maintenance
from django.shortcuts import get_object_or_404
import httpx
from django.contrib import messages


def dashboard_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    count_response = httpx.get("https://smart-campus-tiet-production.up.railway.app/api/book-count")
    books_count = count_response.json()
    budget_getter = httpx.get("https://smart-campus-tiet-production.up.railway.app/api/get-budget")
    budget = budget_getter.json()



    if request.method == 'POST':
      if 'add_book_form' in request.POST:
            book_name = request.POST['book_name']
            author_name = request.POST['book_author']
            book_quantity = request.POST['book_quantity']
            data_to_add_book = {
                "book_name": book_name,
                "author": author_name,
                "quantity": book_quantity
                            }
            add_a_book = httpx.post("https://smart-campus-tiet-production.up.railway.app/api/add-bought-item", json=data_to_add_book)
            messages.success(request, "book added successfully")

      if 'update_budget_form' in request.POST:
          updated_budget = request.POST['updated-budget']
          data_to_update_budget = {
              "Budget" : updated_budget
          }
          update = httpx.post("https://smart-campus-tiet-production.up.railway.app/api/edit-budget", json=data_to_update_budget)
          messages.success(request, "budget updated successfully")

      if 'delete_book_form' in request.POST:
          delete_book_name = request.POST['delete-book-name']
          delete_book_author = request.POST['delete-book-author']
          delete_book_data = {
              "book_name": delete_book_name,
              "author": delete_book_author
          }
          delete_book =  httpx.post("https://smart-campus-tiet-production.up.railway.app/api/delete-book", json=delete_book_data)
          messages.success(request, "book deleted from db")
          
    return render(request, "library.html", {"count" : books_count, "budget" : budget})

def events_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    return render(request, "events.html")

from django.shortcuts import render, get_object_or_404
from .models import Maintenance

def maintenance_view(request):
    maintenance = get_object_or_404(Maintenance, id=1)
    if request.method == 'POST':
        maintenance_mode = 'maintenance' in request.POST
        maintenance.maintenance_mode = maintenance_mode
        maintenance.save()
    
    return render(request, "maintenance.html", {"maintenance": maintenance.maintenance_mode})

