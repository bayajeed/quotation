from rest_framework import serializers
from .models import Quotation, QuotationPart, QuotationItem

class QuotationItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = QuotationItem
        fields = ['id','serial_no','description','qty','unit','unit_price','total_price']
        read_only_fields = ['total_price']


class QuotationPartSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True)

    class Meta:
        model = QuotationPart
        fields = ['id','name','order','items']
        read_only_fields = ['order']


class QuotationSerializer(serializers.ModelSerializer):
    parts = QuotationPartSerializer(many=True)

    class Meta:
        model = Quotation
        fields = ['id','project_name','client_name','notes','created_at','parts']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        parts_data = validated_data.pop('parts', [])
        quotation = Quotation.objects.create(**validated_data)
        for idx, part_data in enumerate(parts_data):
            items_data = part_data.pop('items', [])
            part = QuotationPart.objects.create(quotation=quotation, order=idx, **part_data)
            for jdx, item_data in enumerate(items_data):
                QuotationItem.objects.create(part=part, serial_no=item_data.get('serial_no', jdx+1), **item_data)
        return quotation

    def update(self, instance, validated_data):
        parts_data = validated_data.pop('parts', [])
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()

        # Simplest: delete existing parts/items and recreate from payload
        instance.parts.all().delete()
        for idx, part_data in enumerate(parts_data):
            items_data = part_data.pop('items', [])
            part = QuotationPart.objects.create(quotation=instance, order=idx, **part_data)
            for jdx, item_data in enumerate(items_data):
                QuotationItem.objects.create(part=part, serial_no=item_data.get('serial_no', jdx+1), **item_data)
        return instance
