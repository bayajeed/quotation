from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Quotation, QuotationTemplate, QuotationGroup, QuotationItem,
    Item, ItemGroup, Unit
)
from .serializers import QuotationTemplateSerializer, QuotationSerializer
from .forms import (
    QuotationForm, ItemForm, ItemGroupForm, UnitForm
)
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .utils import process_groups

@method_decorator(login_required, name='dispatch')
class QuotationListView(ListView):
    model = Quotation
    template_name = 'pages/quotation_list.html'
    context_object_name = 'quotations'

@method_decorator(login_required, name='dispatch')
class QuotationDetailView(DetailView):
    model = Quotation
    template_name = 'pages/quotation_view.html'
    context_object_name = 'quotation'

@method_decorator(login_required, name='dispatch')
class QuotationReportView(DetailView):
    model = Quotation
    template_name = 'pages/quotation_report.html'
    context_object_name = 'quotation'

@method_decorator(login_required, name='dispatch')
class QuotationCreateView(View):
    def get(self, request):
        form = QuotationForm()
        templates = QuotationTemplate.objects.all()
        units = Unit.objects.all()
        return render(request, 'pages/quotation_create.html', {'form': form, 'templates': templates, 'units': units})

    def post(self, request):
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save()
            process_groups(request, quotation)
            return redirect('quotation_view', pk=quotation.pk)
        templates = QuotationTemplate.objects.all()
        units = Unit.objects.all()
        return render(request, 'pages/quotation_create.html', {'form': form, 'templates': templates, 'units': units})

@method_decorator(login_required, name='dispatch')
class QuotationUpdateView(View):
    def get(self, request, pk):
        quotation = get_object_or_404(Quotation, pk=pk)
        form = QuotationForm(instance=quotation)
        templates = QuotationTemplate.objects.all()
        units = Unit.objects.all()
        quotation_json = json.dumps(QuotationSerializer(quotation).data)
        return render(request, 'pages/quotation_create.html', {'form': form, 'quotation': quotation, 'templates': templates, 'units': units, 'quotation_json': quotation_json})

    def post(self, request, pk):
        quotation = get_object_or_404(Quotation, pk=pk)
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            quotation = form.save()
            process_groups(request, quotation)
            return redirect('quotation_view', pk=quotation.pk)
        templates = QuotationTemplate.objects.all()
        units = Unit.objects.all()
        return render(request, 'pages/quotation_create.html', {'form': form, 'quotation': quotation, 'templates': templates, 'units': units})

@method_decorator(login_required, name='dispatch')
class QuotationDeleteView(DeleteView):
    model = Quotation
    template_name = 'pages/quotation_delete.html'
    success_url = reverse_lazy('quotation_list')

@method_decorator(login_required, name='dispatch')
class QuotationTemplateDetailAPIView(APIView):
    def get(self, request, pk):
        template = get_object_or_404(QuotationTemplate, pk=pk)
        serializer = QuotationTemplateSerializer(template)
        return Response(serializer.data)

# Item Views
@method_decorator(login_required, name='dispatch')
class ItemListView(ListView):
    model = Item
    template_name = 'pages/item_list.html'

@method_decorator(login_required, name='dispatch')
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'pages/item_form.html'
    success_url = reverse_lazy('item_list')

@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'pages/item_form.html'
    success_url = reverse_lazy('item_list')

@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'pages/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')

# ItemGroup Views
@method_decorator(login_required, name='dispatch')
class ItemGroupListView(ListView):
    model = ItemGroup
    template_name = 'pages/itemgroup_list.html'

@method_decorator(login_required, name='dispatch')
class ItemGroupCreateView(CreateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'pages/itemgroup_form.html'
    success_url = reverse_lazy('itemgroup_list')

@method_decorator(login_required, name='dispatch')
class ItemGroupUpdateView(UpdateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'pages/itemgroup_form.html'
    success_url = reverse_lazy('itemgroup_list')

@method_decorator(login_required, name='dispatch')
class ItemGroupDeleteView(DeleteView):
    model = ItemGroup
    template_name = 'pages/itemgroup_confirm_delete.html'
    success_url = reverse_lazy('itemgroup_list')

# Unit Views
@method_decorator(login_required, name='dispatch')
class UnitListView(ListView):
    model = Unit
    template_name = 'pages/unit_list.html'

@method_decorator(login_required, name='dispatch')
class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'pages/unit_form.html'
    success_url = reverse_lazy('unit_list')

@method_decorator(login_required, name='dispatch')
class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'pages/unit_form.html'
    success_url = reverse_lazy('unit_list')

@method_decorator(login_required, name='dispatch')
class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'pages/unit_confirm_delete.html'
    success_url = reverse_lazy('unit_list')

