from django.db import models

class ItemGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.FloatField(default=0)

    class Meta:
        unique_together = ('group', 'name')

    def __str__(self):
        if self.group:
            return f"{self.name} ({self.group.name})"
        return self.name

class QuotationTemplate(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuotationTemplateItem(models.Model):
    template = models.ForeignKey(QuotationTemplate, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField(default=1)
    unit_price = models.FloatField(null=True, blank=True)

    def total_price(self):
        price = self.unit_price if self.unit_price is not None else self.item.unit_price
        return self.qty * price

    def __str__(self):
        return f"{self.item.name}"


class Quotation(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    template = models.ForeignKey(QuotationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(group.subtotal() for group in self.groups.all())

    def __str__(self):
        return f"{self.title} - {self.client_name}"


class QuotationGroup(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)

    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return self.name


class QuotationItem(models.Model):
    group = models.ForeignKey(QuotationGroup, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField(default=1)
    unit_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name