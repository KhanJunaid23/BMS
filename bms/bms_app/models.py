from django.db import models

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]


class Items(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=255)

    class Meta:
        db_table = "items"

    def __str__(self):
        return self.item_name


class Remarks(models.Model):
    remark_id = models.BigAutoField(primary_key=True)
    remark = models.CharField(max_length=255)

    class Meta:
        db_table = "remarks"

    def __str__(self):
        return self.remark


class Tax(models.Model):
    tax_id = models.BigAutoField(primary_key=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    default_tax = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "tax"

    def __str__(self):
        return f"{self.tax_percentage}% - {self.description or 'No Description'}"


class Party(models.Model):
    party_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    gst = models.CharField(max_length=20, null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "party"

    def __str__(self):
        return self.name


class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    gst = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_account_no = models.CharField(max_length=20, null=True, blank=True)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    bank_ifsc = models.CharField(max_length=20, null=True, blank=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    cst_no = models.CharField(max_length=20, null=True, blank=True)
    invoice_head = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name


class FinancialYear(models.Model):
    financial_year_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="financial_years")
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = "financial_year"

    def __str__(self):
        return f"{self.company.name}: {self.from_date} to {self.to_date}"


class GSTDetails(models.Model):
    gst_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="gst_details")
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name="gst_details")
    gst = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "gst_details"

    def __str__(self):
        return f"{self.company.name}: {self.gst}"


class CompanyPartyInvoiceDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="party_invoice_details")
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name="party_invoice_details")
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="company_invoice_details")
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "company_party_invoice_details"

    def __str__(self):
        return f"{self.company.name}: {self.party.name}"


class Transactions(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    bill_no = models.CharField(max_length=100, null=True, blank=True)
    bill_date = models.DateField(null=True, blank=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="transactions_as_party")
    party_bill_no = models.CharField(max_length=100, null=True, blank=True)
    seller_party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="transactions_as_seller_party")
    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    brokerage_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    brokerage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    brokerage_gst = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name="transactions")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    remark = models.ForeignKey(Remarks, on_delete=models.CASCADE, related_name="transactions")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="transactions")
    company_financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name="transactions")

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.party.name if self.party else 'Unknown'}"
