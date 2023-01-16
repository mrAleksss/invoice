from django.shortcuts import render, get_object_or_404
from .models import Invoice, Profile
from django.views.generic import ListView, FormView, DetailView, UpdateView, RedirectView, DeleteView
from profiles.models import Profile
from .forms import InvoiceForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from positions.forms import PositionForm
from positions.models import Position
from .mixins import InvoiceClosedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template

# Create your views here.
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 3
    template_name = 'invoices/main.html'# template_name by default invoice_list for model name
    context_object_name = 'qs'# object_list by defoult
    def get_queryset(self):
        # profile = Profile.objects.get(user=self.request.user)
        profile = get_object_or_404(Profile, user=self.request.user)
        # qs = Invoice.objects.filter(profile=profile).order_by('-created')
        # return qs
        return super().get_queryset().filter(profile=profile).order_by('-created')
    
    
class InvoiceFormView(LoginRequiredMixin, FormView):
    template_name = 'invoices/create.html'
    form_class = InvoiceForm
    # success_url = reverse_lazy("invoices:main")
    i_instance = None
    
    
    def form_valid(self, form):
        # add profile to forms
        profile = Profile.objects.get(user=self.request.user)
        instance = form.save(commit=False)
        instance.profile = profile
        form.save()
        self.i_instance = instance
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('invoices:detail', kwargs={'pk':self.i_instance.pk})
    
    
# class SimpleView(TemplateView):
#     template_name = "invoices/simple.html"

# class SimpleView(DetailView):
#     template_name = "invoices/simple.html"
#     model = Invoice
    
    
class AddPositionsFormView(LoginRequiredMixin, FormView):
    template_name = "invoices/detail.html"
    form_class = PositionForm
    
    def get_success_url(self):
        return self.request.path
    
    def form_valid(self, form):
        invoice_pk = self.kwargs.get('pk')
        invoice_obj = Invoice.objects.get(pk=invoice_pk)
        instance = form.save(commit=False)
        instance.invoice = invoice_obj
        form.save()
        messages.info(self.request, f"successfully added {instance.title}")
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_obj = Invoice.objects.get(pk=self.kwargs.get('pk'))
        qs = invoice_obj.positions
        context['obj'] = invoice_obj
        context['qs'] = qs
        
        return context
    
    
    
class InvoiceUpdateView(LoginRequiredMixin, InvoiceClosedMixin, UpdateView):
    template_name = "invoices/update.html"
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy("invoices:main")
    
    def form_valid(self, form):
        instance = form.save()
        messages.info(self.request, f"Successfully updated invoice - {instance.number}")
        return super().form_valid(form)
    
    
class CloseInvoiceView(LoginRequiredMixin, RedirectView):
    pattern_name = "invoices:detail"
    
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Invoice.objects.get(pk=pk)
        obj.closed = True
        obj.save()
        
        return super().get_redirect_url(*args, **kwargs)
    
    
class InvoicePositionDeleteView(LoginRequiredMixin, InvoiceClosedMixin, DeleteView):
    model = Position
    template_name = "invoices/confirm_delete.html"
    
    # path <pk>/delete/<position_pk>
    def get_object(self):
        pk = self.kwargs.get('position_pk')
        obj = Position.objects.get(pk=pk)
        return obj
    
    def get_success_url(self):
        messages.info(self.request, f"successfully deleted position {self.object.title}")
        return reverse('invoices:detail', kwargs={'pk':self.object.invoice.id})
    
@login_required
def invoice_pdf_view(request, **kwargs):
    
    pk = kwargs.get('pk')
    obj = Invoice.objects.get(pk=pk)
    
    logo_result = finders.find('img/logo.png')
    font_result = finders.find('fonts/Lato-Regular.ttf')
    # show search location result
    searched_locations = finders.searched_locations
    print(searched_locations)
    
    template_path = 'invoices/pdf.html'
    context = {
        'object': obj,
        'static': {
            'font': font_result,
            'logo': logo_result,
        },
    }
    # Create a django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    # find the template and render it
    template = get_template(template_path)
    html = template.render(context)
    
    # create pdf
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=response, encoding='utf-8')
    
    # if case of error
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    return response
 
 
        