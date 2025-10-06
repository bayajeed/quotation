from django.db import models

class QuotationTemplate(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuotationTemplateItem(models.Model):
    template = models.ForeignKey(QuotationTemplate, on_delete=models.CASCADE, related_name='items')
    group_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    qty = models.FloatField(default=1)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.FloatField(default=0)

    def total_price(self):
        return self.qty * self.unit_price

    def __str__(self):
        return f"{self.description}"


class Quotation(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    template = models.ForeignKey(QuotationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price for group in self.groups.all() for item in group.items.all())

    def __str__(self):
        return f"{self.title} - {self.client_name}"


class QuotationGroup(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuotationItem(models.Model):
    group = models.ForeignKey(QuotationGroup, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    qty = models.FloatField(default=1)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
