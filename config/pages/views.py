from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa   # pip install xhtml2pdf
from .models import *

# 🧾 List all quotations
def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-id')
    return render(request, 'pages/quotation_list.html', {'quotations': quotations})


# 🧱 Create quotation dynamically
def quotation_create(request):
    templates = QuotationTemplate.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        client = request.POST.get('client')
        template_id = request.POST.get('template')

        if not title:
            messages.error(request, "Title দেওয়া বাধ্যতামূলক।")
            return redirect('quotation_create')

        quotation = Quotation.objects.create(
            title=title,
            client_name=client,
            template_id=template_id
        )

        group_names = request.POST.getlist('group_name[]')
        descriptions = request.POST.getlist('description[]')
        qtys = request.POST.getlist('qty[]')
        units = request.POST.getlist('unit[]')
        prices = request.POST.getlist('unit_price[]')
        totals = request.POST.getlist('total_price[]')

        if not descriptions:
            messages.error(request, "Item data পাওয়া যায়নি।")
            quotation.delete()
            return redirect('quotation_create')

        current_group = None
        grand_total = 0

        for i in range(len(descriptions)):
            desc = descriptions[i].strip()
            grp = group_names[i].strip() if i < len(group_names) else ""
            qty = qtys[i] or ""
            unit = units[i] or ""
            price = float(prices[i]) if prices[i] else 0
            total = float(totals[i]) if totals[i] else 0

            if grp:
                current_group = QuotationGroup.objects.create(
                    quotation=quotation, name=grp
                )

            if desc and current_group:
                QuotationItem.objects.create(
                    group=current_group,
                    description=desc,
                    qty=qty,
                    unit=unit,
                    unit_price=price,
                    total_price=total
                )
                grand_total += total

        quotation.total_amount = grand_total
        quotation.save()
        messages.success(request, "Quotation সফলভাবে তৈরি হয়েছে ✅")
        return redirect('quotation_view', quotation.id)

    return render(request, 'pages/quotation_create.html', {'templates': templates})


# 🔍 View single quotation (details page)
def quotation_view(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    groups = quotation.groups.prefetch_related('items').all()
    return render(request, 'pages/quotation_view.html', {
        'quotation': quotation,
        'groups': groups
    })


# 🔄 Load template items dynamically (AJAX)
def load_template_items(request, template_id):
    items = QuotationTemplateItem.objects.filter(template_id=template_id)
    grouped = {}

    for i in items:
        grouped.setdefault(i.group_name or "Main Part", []).append({
            'description': i.description,
            'qty': i.qty or '',
            'unit': i.unit or '',
            'unit_price': float(i.unit_price or 0)
        })

    return JsonResponse({'groups': grouped})


# 🧾 Generate PDF (A4 size printable format)
def quotation_pdf(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    groups = quotation.groups.prefetch_related('items').all()

    html = render_to_string('pages/quotation_pdf.html', {
        'quotation': quotation,
        'groups': groups
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Quotation_{quotation.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
