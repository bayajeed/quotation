from .models import QuotationGroup, QuotationItem, Item, ItemGroup, Unit

def process_groups(request, quotation):
    groups_data = {}
    for key, value in request.POST.items():
        if not key.startswith('groups-'):
            continue

        parts = key.split('-')
        try:
            if len(parts) < 3:
                continue

            group_index = int(parts[1])
            field_type = parts[2]

            if group_index not in groups_data:
                groups_data[group_index] = {'items': {}}

            if field_type == 'name' and len(parts) == 3:
                groups_data[group_index]['name'] = value
            elif field_type == 'items' and len(parts) == 5:
                item_index = int(parts[3])
                item_field = parts[4]
                if item_index not in groups_data[group_index]['items']:
                    groups_data[group_index]['items'][item_index] = {}
                groups_data[group_index]['items'][item_index][item_field] = value
        except (ValueError, IndexError):
            # Safely ignore any key that doesn't match the expected pattern
            continue

    # Clear existing groups to rebuild them
    quotation.groups.all().delete()
    
    for index, data in sorted(groups_data.items()):
        group_name = data.get('name', '').strip()
        if not group_name:
            continue # Don't create a group without a name

        group = QuotationGroup.objects.create(quotation=quotation, name=group_name)
        item_group, _ = ItemGroup.objects.get_or_create(name=group_name)

        for item_index, item_data in sorted(data.get('items', {}).items()):
            description = item_data.get('description', '').strip()
            if not description:
                continue # Skip empty item rows

            try:
                qty = float(item_data.get('qty') or '1')
            except ValueError:
                qty = 1.0

            try:
                unit_price = float(item_data.get('unit_price') or '0')
            except ValueError:
                unit_price = 0.0

            unit, _ = Unit.objects.get_or_create(name=item_data.get('unit', ''))
            
            try:
                item = Item.objects.get(name=description, group=item_group)
                created = False
            except Item.DoesNotExist:
                item = Item.objects.create(
                    name=description,
                    group=item_group,
                    unit=unit,
                    unit_price=unit_price
                )
                created = True
            except Item.MultipleObjectsReturned:
                # This indicates a data integrity issue but we'll proceed by picking one.
                item = Item.objects.filter(name=description, group=item_group).first()
                created = False

            if not created and (item.unit != unit or item.unit_price != unit_price):
                item.unit = unit
                item.unit_price = unit_price
                item.save()

            QuotationItem.objects.create(
                group=group,
                item=item,
                qty=qty,
                unit_price=unit_price
            )
