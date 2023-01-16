from django.urls import path
from .views import *



app_name = "invoices"

urlpatterns = [
    path("", InvoiceListView.as_view(), name="main"),
    path("new/", InvoiceFormView.as_view(), name="create"),
    # path('<pk>/', SimpleView.as_view(), name="detail"),
    path('<pk>/update/', InvoiceUpdateView.as_view(), name="update"),
    path('<pk>/closed/', CloseInvoiceView.as_view(), name="closed"),
    path('<pk>/', AddPositionsFormView.as_view(), name="detail"),
    path('<pk>/delete/<int:position_pk>/', InvoicePositionDeleteView.as_view(), name="delete"),
    path('<pk>/pdf/', invoice_pdf_view, name="pdf")
]
