# Django core imports
from django.urls import reverse
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging
logger = logging.getLogger('custom') 

# Class-based views
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView
)

# Third-party packages
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Local app imports
from .models import Invoice
from .tables import InvoiceTable

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import InvoiceSerializer
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
"""
def invoice_detail_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    template = get_template('invoice_pdf.html')
    html_content = template.render({'invoice': invoice})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{pk}.pdf"'

    HTML(string=html_content).write_pdf(response)
    return response
"""
def invoice_detail_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    template = get_template('invoice_pdf.html')
    html_content = template.render({'invoice': invoice})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{pk}.pdf"'

    # PDF oluşturmak için BytesIO kullanıyoruz
    result = BytesIO()
    pdf_status = pisa.CreatePDF(src=html_content, dest=result)

    if not pdf_status.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse("PDF oluşturulamadı", status=500)

class InvoiceListView(APIView):
    """
    API view for listing invoices.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)


class InvoiceDetailView(APIView):
    """
    API view for retrieving the details of an invoice.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)


class InvoiceCreateView(APIView):
    """
    API view for creating a new invoice.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.user.username} tarafından {invoice.id} numaralı fatura eklendi.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceUpdateView(APIView):
    """
    API view for updating an existing invoice.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def put(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDeleteView(APIView):
    """
    API view for deleting an invoice.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def delete(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        print("log satırına geldik")
        logger.info(f"{request.user.username} tarafından {invoice.id} numaralı fatura silindi.")
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
