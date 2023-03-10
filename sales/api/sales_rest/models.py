from email.policy import default
from django.db import models


# Create your models here.


class AutomobileVO(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    has_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"VIN:{self.vin}"


class SalesPerson(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SaleRecord(models.Model):
    automobile = models.ForeignKey(
        AutomobileVO,
        related_name="sales_record",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    sales_person = models.ForeignKey(
        SalesPerson,
        related_name="sales_record",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    customer = models.ForeignKey(
        Customer,
        related_name="sales_record",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer} {self.automobile} {self.sales_person} {self.price}"
