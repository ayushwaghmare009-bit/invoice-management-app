from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import invoice
from django.shortcuts import render
from invoice_app.models import invoice
from  .forms import invoiceForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Sum, Count,Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

@login_required(login_url='login')
def generate_invoice_pdf(request, pk):
    inv = get_object_or_404(invoice, pk=pk)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{inv.invoice_number}.pdf"'

    # Create the PDF object, using the ReportLab canvas library
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw Corporate Header
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, height - 50, "INVOICE MANAGEMENT SYSTEM")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, "Official Digital Statement")

    # Draw a line separator
    p.setLineWidth(1)
    p.line(50, height - 85, width - 50, height - 85)

    # Invoice Metadata
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, f"Invoice #: {inv.invoice_number}")
    p.drawString(50, height - 145, f"Customer Name: {inv.customer_name}")
    p.drawString(50, height - 170, f"Date Created: {inv.date_created.strftime('%B %d, %Y')}")
    
    status_text = "Paid" if inv.is_paid else "Unpaid"
    p.drawString(50, height - 195, f"Payment Status: {status_text}")

    # Amount Box / Total
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 250, f"Total Amount Due: ₹{inv.amount}")

    # Footer note
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, height - 320, "Thank you for your business! This is a computer-generated invoice.")

    # Close and save the PDF object
    p.showPage()
    p.save()
    
    return response




def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically logs the user in after registration
            return redirect('invoices')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def invoices_list_view(request):
    # Get search and filter parameters from the URL
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    all_invoices = invoice.objects.all().order_by('-date_created')

    # Apply search filter (by customer name or invoice number)
    if query:
        all_invoices = all_invoices.filter(
            Q(customer_name__icontains=query) | Q(invoice_number__icontains=query)
        )

    # Apply payment status filter
    if status_filter == 'paid':
        all_invoices = all_invoices.filter(is_paid=True)
    elif status_filter == 'unpaid':
        all_invoices = all_invoices.filter(is_paid=False)

    # Calculate metrics based on the full dataset (or filtered dataset)
    total_revenue = all_invoices.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
    paid_count = all_invoices.filter(is_paid=True).count()
    unpaid_count = all_invoices.filter(is_paid=False).count()

    context = {
        'all_invoices': all_invoices,
        'total_revenue': total_revenue,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
    }
    return render(request, 'invoice_list.html', context)


@login_required(login_url='login')
def add_invoice(request):
    form = invoiceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice successfully created!")
            return redirect('invoices')
    return render(request, 'add_invoice.html', {'form': form})
    
@login_required(login_url='login')
def edit_invoice(request, pk):
    inv = get_object_or_404(invoice, pk=pk)
    if request.method == 'POST':
        form = invoiceForm(request.POST, instance=inv)
        if form.is_valid():
            form.save()
            return redirect('invoices')
    else:
        form = invoiceForm(instance=inv)
    return render(request, 'edit_invoice.html', {'form': form})



@login_required(login_url='login')
def create_invoice(request):
    invoice.objects.create(
        customer_name='ayush waghmare',
        invoice_number="INV-1000",
        amount=15000.00,
        is_paid=False
    )
    return render(request,'E:\new_django\mysite\invoice_app\templates\invoice_list.html',{})

@login_required(login_url='login')
def show_one_invoice(request):
    incoice=invoice.objects.get(invoice_number='INV-1000')

    data={
        'invoice':invoice
    }
    return render(request,'mysite\invoice_app\templates\invoice_detail.html')

@login_required(login_url='login')
def show_unpaid_invoices(request):
    unpaid_invoices=invoice.objects.filter(is_paid=False)
    data={
        'unpaid_invoices':unpaid_invoices 
    }
    return render(request,'E:\new_django\mysite\invoice_app\templates\invoice_list.html',data)

@login_required(login_url='login')
def mark_as_paid(request):
    invoice.objects.filter(invoice_number='INV-100').update(is_paid=True)
    all_invoices=invoice.objects.filter(is_paid=False)
    data={
        'all_invoices':all_invoices
    }
    return render(request,'E:\new_django\mysite\invoice_app\templates\invoice_list.html',data)


class HomePageView(TemplateView):
    template_name='home.html'

class InvoicesListView(TemplateView):
    model=invoice
    template_name='invoice_list.html'
    context_object_name='all_invoice'

@login_required(login_url='login')
def cust_name_view(request):
    invoices=[
        {'id':1,'name':'rahul','amount':5000},
        {'id':2,'name':'udit','amount':8000},
        {'id':3,'name':'karan','amount':4747},
    ]
    return render(request,'customer.html',{'invoices':invoices})

@login_required(login_url='login')
def delete_invoice(request, pk):
    inv = get_object_or_404(invoice, pk=pk)
    if request.method == 'POST':
        inv.delete()
        messages.success(request, "Invoice deleted successfully.")
        return redirect('invoices')
    return render(request, 'delete_invoice.html', {'invoice': inv})
# Create your views here.
