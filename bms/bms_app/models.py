from django.db import models

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

class Items(models.Model):
    item_name = models.CharField(max_length=255)

    class Meta:
        db_table = "items"

    def __str__(self):
        return self.item_name
    
class Remarks(models.Model):
    remark = models.CharField(max_length=255)

    class Meta:
        db_table = "remarks"

    def __str__(self):
        return self.remark
    
class Tax(models.Model):
    tax_percentage = models.IntegerField()
    default_tax = models.IntegerField(default=5)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "tax"

    def __str__(self):
        return f"{self.tax_percentage}% - {self.description}"

class Party(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    person = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    gst = models.CharField(max_length=20, null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "party"

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    gst = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_account_no = models.CharField(max_length=20, null=True, blank=True)
    bank_branch = models.CharField(max_length=20, null=True, blank=True)
    bank_ifsc = models.CharField(max_length=20, null=True, blank=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    cst_no = models.CharField(max_length=20, null=True, blank=True)
    invoice_head = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True,default='active')

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class FinancialYear(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    from_date = models.CharField(max_length=20, null=True, blank=True)
    to_date = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True,default='active')

    class Meta:
        db_table = "financial_year"

    def __str__(self):
        return f"{self.company.name}: {self.from_date} to {self.to_date}"
    
class GSTDetails(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    gst = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "gst_details"

    def __str__(self):
        return f"{self.company.name}: {self.gst}"
    
class CompanyPartInvoiceDetails(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "company_party_invoice_details"

    def __str__(self):
        return f"{self.company.name}: {self.party.name}"