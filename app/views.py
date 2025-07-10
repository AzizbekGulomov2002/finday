from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense
from datetime import datetime
from django.views.decorators.http import require_http_methods

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_http_methods(['GET', 'POST'])
def expense_view(request):
    # Filtering parameters
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # Start with all expenses, ordered by date
    qs = Expense.objects.all().order_by('-date')
    total = None

    # Apply date filtering if both start and end dates are provided
    if start and end:
        try:
            s = datetime.fromisoformat(start).date()
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(date__range=[s, e])
            total = qs.aggregate(Sum('amount'))['amount__sum']
        except ValueError:
            # Handle invalid date format
            messages.error(request, "Sana formati noto'g'ri. Iltimos, YYYY-MM-DD formatida kiriting.")
            total = None
            # Clear invalid dates from context to prevent pre-filling bad values
            start = None
            end = None
    
    # --- Pagination ---
    paginator = Paginator(qs, 10) # Show 10 expenses per page
    page = request.GET.get('page') # Get current page number from URL

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        expenses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        expenses = paginator.page(paginator.num_pages)
    # --- End Pagination ---

    # Handle Create or Update operations for POST requests
    if request.method == 'POST':
        exp_id = request.POST.get('id')
        name = request.POST.get('name')
        amount_str = request.POST.get('amount')
        date_str = request.POST.get('date')

        # Basic validation for required fields
        if not name or not amount_str or not date_str:
            messages.error(request, "Barcha maydonlar to'ldirilishi shart.")
            # Redirect back to the list or re-render the form with errors
            return redirect('app:expense_list') 

        try:
            amount = float(amount_str) # Convert amount to float
            date = datetime.fromisoformat(date_str).date()
        except ValueError:
            messages.error(request, "Miqdor yoki sana formati noto'g'ri. Miqdor raqam, sana YYYY-MM-DD formatida bo'lishi kerak.")
            return redirect('app:expense_list')

        if exp_id:
            # Update existing expense
            exp = get_object_or_404(Expense, pk=int(exp_id))
            exp.name, exp.amount, exp.date = name, amount, date
            exp.save()
            messages.success(request, "Xarajat muvaffaqiyatli yangilandi!")
        else:
            # Create new expense
            Expense.objects.create(name=name, amount=amount, date=date)
            messages.success(request, "Yangi xarajat muvaffaqiyatli qo'shildi!")
        
        # Always redirect after a successful POST to prevent re-submission
        return redirect('app:expense_list')
    
    # Render the template for GET requests
    return render(request, 'expense.html', {
        'expenses': expenses, # Pass the paginated object
        'total': total,
        'start': start,
        'end': end,
    })

# Add a separate view for deleting an expense for cleaner URL structure and POST method handling
@require_http_methods(['POST']) # Ensure deletion only happens via POST request for security
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, "Xarajat muvaffaqiyatli o'chirildi!")
    return redirect('app:expense_list')





from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense, Income # Import both models
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# --- Expense Views (oldingi kodlaringiz) ---

def main_view(request):
    return render(request, 'main.html')



@require_http_methods(['GET', 'POST'])
def expense_view(request):
    # Filtrlash parametrlari
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    qs = Expense.objects.all().order_by('-date')
    total = None

    if start and end:
        try:
            s = datetime.fromisoformat(start).date()
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(date__range=[s, e])
            total = qs.aggregate(Sum('amount'))['amount__sum']
        except ValueError:
            messages.error(request, "Sana formati noto'g'ri. Iltimos, YYYY-MM-DD formatida kiriting.")
            total = None
            start = None
            end = None
    
    paginator = Paginator(qs, 10) # Har sahifada 10 ta element
    page = request.GET.get('page')
    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        exp_id = request.POST.get('id')
        name = request.POST.get('name')
        amount_str = request.POST.get('amount')
        date_str = request.POST.get('date')

        if not name or not amount_str or not date_str:
            messages.error(request, "Barcha maydonlar to'ldirilishi shart.")
            return redirect('app:expense_list') 

        try:
            amount = float(amount_str)
            date = datetime.fromisoformat(date_str).date()
        except ValueError:
            messages.error(request, "Miqdor yoki sana formati noto'g'ri. Miqdor raqam, sana YYYY-MM-DD formatida bo'lishi kerak.")
            return redirect('app:expense_list')

        if exp_id:
            exp = get_object_or_404(Expense, pk=int(exp_id))
            exp.name, exp.amount, exp.date = name, amount, date
            exp.save()
            messages.success(request, "Xarajat muvaffaqiyatli yangilandi!")
        else:
            Expense.objects.create(name=name, amount=amount, date=date)
            messages.success(request, "Yangi xarajat muvaffaqiyatli qo'shildi!")
        
        return redirect('app:expense_list')
    
    return render(request, 'expense.html', {
        'expenses': expenses,
        'total': total,
        'start': start,
        'end': end,
    })

@require_http_methods(['POST'])
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, "Xarajat muvaffaqiyatli o'chirildi!")
    return redirect('app:expense_list')

# --- Income Views (Yangi qo'shiladigan qism) ---

@require_http_methods(['GET', 'POST'])
def income_view(request):
    # Filtrlash parametrlari
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # Kirimlar obyektini olish va sanasi bo'yicha tartiblash
    qs = Income.objects.all().order_by('-date')
    total = None

    # Agar boshlanish va tugash sanalari berilgan bo'lsa, filtrlash
    if start and end:
        try:
            s = datetime.fromisoformat(start).date()
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(date__range=[s, e])
            total = qs.aggregate(Sum('amount'))['amount__sum']
        except ValueError:
            messages.error(request, "Sana formati noto'g'ri. Iltimos, YYYY-MM-DD formatida kiriting.")
            total = None
            # Noto'g'ri kiritilgan sanani tozalash
            start = None
            end = None
    
    # Pagination
    paginator = Paginator(qs, 10) # Har sahifada 10 ta element
    page = request.GET.get('page') # URL dan sahifa raqamini olish
    try:
        incomes = paginator.page(page)
    except PageNotAnInteger:
        # Agar sahifa raqami butun son bo'lmasa, birinchi sahifani ko'rsatish
        incomes = paginator.page(1)
    except EmptyPage:
        # Agar sahifa mavjud bo'lmasa, oxirgi sahifani ko'rsatish
        incomes = paginator.page(paginator.num_pages)
    
    # Kirim qo'shish yoki yangilash
    if request.method == 'POST':
        inc_id = request.POST.get('id')
        name = request.POST.get('name')
        amount_str = request.POST.get('amount')
        date_str = request.POST.get('date')

        # Kerakli maydonlarni tekshirish
        if not name or not amount_str or not date_str:
            messages.error(request, "Barcha maydonlar to'ldirilishi shart.")
            return redirect('app:income_list') 

        try:
            amount = float(amount_str) # Miqdorni floatga aylantirish
            date = datetime.fromisoformat(date_str).date()
        except ValueError:
            messages.error(request, "Miqdor yoki sana formati noto'g'ri. Miqdor raqam, sana YYYY-MM-DD formatida bo'lishi kerak.")
            return redirect('app:income_list')

        if inc_id:
            # Mavjud kirimni yangilash
            inc = get_object_or_404(Income, pk=int(inc_id))
            inc.name, inc.amount, inc.date = name, amount, date
            inc.save()
            messages.success(request, "Kirim muvaffaqiyatli yangilandi!")
        else:
            # Yangi kirim yaratish
            Income.objects.create(name=name, amount=amount, date=date)
            messages.success(request, "Yangi kirim muvaffaqiyatli qo'shildi!")
        
        # POST so'rovidan keyin qayta yo'naltirish
        return redirect('app:income_list')
    
    # GET so'rovlari uchun shablonni render qilish
    return render(request, 'income.html', {
        'incomes': incomes, # Endi paginator obyektini yuboramiz
        'total': total,
        'start': start,
        'end': end,
    })

@require_http_methods(['POST'])
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    messages.success(request, "Kirim muvaffaqiyatli o'chirildi!")
    return redirect('app:income_list')