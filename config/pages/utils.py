
from .models import QuotationGroup, QuotationItem, Item, ItemGroup, Unit

def process_groups(request, quotation):
    groups_data = {}
    for key, value in request.POST.items():
        if key.startswith('groups-'):
            parts = key.split('-')
            group_index = int(parts[1])
            field_type = parts[2]

            if group_index not in groups_data:
                groups_data[group_index] = {'items': {}}

            if field_type == 'name':
                groups_data[group_index]['name'] = value
            elif field_type == 'items':
                item_index = int(parts[3])
                item_field = parts[4]
                if item_index not in groups_data[group_index]['items']:
                    groups_data[group_index]['items'][item_index] = {}
                groups_data[group_index]['items'][item_index][item_field] = value
    
    quotation.groups.all().delete()
    for index, data in groups_data.items():
        group = QuotationGroup.objects.create(quotation=quotation, name=data['name'])
        item_group, _ = ItemGroup.objects.get_or_create(name=data['name'])

        for item_index, item_data in data['items'].items():
            unit, _ = Unit.objects.get_or_create(name=item_data.get('unit', ''))
            item, _ = Item.objects.get_or_create(
                name=item_data.get('description', ''),
                group=item_group,
                unit=unit,
                defaults={'unit_price': float(item_data.get('unit_price', 0))}
            )
            item.unit_price = float(item_data.get('unit_price', 0))
            item.save()

            QuotationItem.objects.create(
                group=group,
                item=item,
                qty=float(item_data.get('qty', 1)),
                unit_price=float(item_data.get('unit_price', 0))
            )
