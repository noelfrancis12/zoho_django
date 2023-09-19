from django.db import models
from django.contrib.auth.models import User

class company_details(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    contact_number = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    company_email = models.CharField(max_length=255,null=True,blank=True)
    business_name = models.CharField(max_length=255,null=True,blank=True)
    company_type = models.CharField(max_length=255,null=True,blank=True)
    industry_type = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/patient')




class Sales(models.Model):
    Account_type=models.TextField(max_length=255)
    Account_name=models.TextField(max_length=255)
    Acount_code=models.TextField(max_length=255)
    Account_desc=models.TextField(max_length=255)
    def __str__(self):
        return self.Account_name
    


class Purchase(models.Model):
    ACC_TYPE_CHOICES = (
        ('1', 'EXPENSE'),
        ('2', 'Cost of Goods Sold'),
        ('3', 'Fixed Asset'),
    )
    Account_type=models.CharField(max_length=255,choices=ACC_TYPE_CHOICES)
    Account_name=models.TextField(max_length=255)
    Acount_code=models.TextField(max_length=255)
    Account_desc=models.TextField(max_length=255)
    def __str__(self):
        return self.Account_name




class Unit(models.Model):
    unit=models.TextField(max_length=255)

    def __str__(self):
        return self.unit


    
    
    
class AddItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    type=models.TextField(max_length=255)
    Name=models.TextField(max_length=255)
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    hsn=models.IntegerField(null=True,blank=True)
    sales=models.ForeignKey(Sales,on_delete=models.CASCADE)

    purchase=models.ForeignKey(Purchase,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    s_desc=models.TextField(max_length=255)
    p_desc=models.TextField(max_length=255)
    creat=models.CharField(max_length=255)
    s_price=models.CharField(max_length=255)
    p_price=models.TextField(max_length=255)
    satus=models.TextField(default='active')
    interstate=models.CharField(max_length=255,default='')
    intrastate=models.CharField(max_length=255,default='')
    tax=models.TextField(max_length=255,null=True)
    invacc=models.TextField(max_length=255,null=True)
    stock=models.IntegerField(blank=True,null=True,)
    rate=models.IntegerField(blank=True,null=True,)
    status_stock=models.TextField(default='active')


class History(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    date=models.DateTimeField(auto_now=True)
    message=models.CharField(max_length=255)
    p=models.ForeignKey(AddItem,on_delete=models.CASCADE)


class vendor_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    salutation=models.CharField(max_length=25)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    company_name=models.CharField(max_length=150)
    vendor_display_name=models.CharField(max_length=150)
    vendor_email=models.CharField(max_length=250)
    vendor_wphone=models.CharField(max_length=50)
    vendor_mphone=models.CharField(max_length=50)
    skype_number=models.CharField(max_length=50)
    designation=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    website=models.CharField(max_length=250)
    gst_treatment=models.CharField(max_length=100)
    gst_number=models.CharField(max_length=50,null=True)
    pan_number=models.CharField(max_length=50,null=True)
    source_supply=models.CharField(max_length=100)
    currency=models.CharField(max_length=50)
    opening_bal=models.CharField(max_length=100)
    opening_bal_type=models.CharField(max_length=100,null=True,blank=True)
    payment_terms=models.CharField(max_length=100)
    battention=models.CharField(max_length=100,default='')
    bcountry=models.CharField(max_length=100,default='')
    baddress=models.CharField(max_length=300,default='')
    bcity=models.CharField(max_length=100,default='')
    bstate=models.CharField(max_length=100,default='')
    bzip=models.CharField(max_length=100,default='')
    bphone=models.CharField(max_length=100,default='')
    bfax=models.CharField(max_length=100,default='')
    sattention=models.CharField(max_length=100,default='')
    scountry=models.CharField(max_length=100,default='')
    saddress=models.CharField(max_length=300,default='')
    scity=models.CharField(max_length=100,default='')
    sstate=models.CharField(max_length=100,default='')
    szip=models.CharField(max_length=100,default='')
    sphone=models.CharField(max_length=100,default='')
    sfax=models.CharField(max_length=100,default='')
    status=models.CharField(max_length=100,null=True,blank=True)

class comments_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    comment=models.TextField(max_length=500)

class mail_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    mail_from=models.TextField(max_length=300)
    mail_to=models.TextField(max_length=300)
    subject=models.TextField(max_length=250)
    content=models.TextField(max_length=900)
    mail_date=models.DateTimeField(auto_now_add=True)

class doc_upload_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    title=models.TextField(max_length=200)
    document=models.FileField(upload_to='doc/')
    
    
    
class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    Fname=models.CharField(max_length=100,null=True,blank=True)
    Lname=models.CharField(max_length=100,null=True,blank=True)
    customerName= models.CharField(max_length=100,null=True,blank=True)
    customerType= models.CharField(max_length=100,null=True,blank=True)
    companyName= models.CharField(max_length=100,null=True,blank=True)
    customerEmail= models.CharField(max_length=100,null=True,blank=True)
    customerWorkPhone= models.CharField(max_length=100,null=True,blank=True)
    customerMobile= models.CharField(max_length=100,null=True,blank=True)
    skype=models.CharField(max_length=100,null=True,blank=True)
    designation=models.CharField(max_length=100,null=True,blank=True)
    department=models.CharField(max_length=100,null=True,blank=True)
    website=models.CharField(max_length=100,null=True,blank=True)
    GSTTreatment=models.CharField(max_length=100,null=True,blank=True)
    GSTIN=models.CharField(max_length=100,null=True,blank=True)
    pan_no=models.CharField(max_length=100,null=True,blank=True)
    placeofsupply=models.CharField(max_length=100,null=True,blank=True)
    Taxpreference=models.CharField(max_length=100,null=True,blank=True)
    currency=models.CharField(max_length=100,null=True,blank=True)
    OpeningBalance= models.IntegerField(null=True,blank=True)
    PaymentTerms=models.CharField(max_length=100,null=True,blank=True)
    PriceList=models.CharField(max_length=100,null=True,blank=True)

    PortalLanguage=models.CharField(max_length=100,null=True,blank=True)
    Facebook=models.CharField(max_length=100,null=True,blank=True)
    Twitter=models.CharField(max_length=100,null=True,blank=True)
    Attention=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    Address1=models.CharField(max_length=100,null=True,blank=True)
    Address2=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.CharField(max_length=100,null=True,blank=True)
    phone1=models.CharField(max_length=100,null=True,blank=True)
    fax=models.CharField(max_length=100,null=True,blank=True)
    remark=models.CharField(max_length=100,null=True,blank=True)

class customer_contact_person_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Customr=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    CPsalutation=models.CharField(max_length=100,null=True,blank=True)
    Firstname=models.CharField(max_length=100,null=True,blank=True)
    Lastname=models.CharField(max_length=100,null=True,blank=True)
    CPemail=models.CharField(max_length=100,null=True,blank=True)
    CPphone=models.CharField(max_length=100,null=True,blank=True)
    CPmobile=models.CharField(max_length=100,null=True,blank=True)
    CPskype=models.CharField(max_length=100,null=True,blank=True)
    CPdesignation=models.CharField(max_length=100,null=True,blank=True)
    CPdepartment=models.CharField(max_length=100,null=True,blank=True)

class RetainerInvoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    customer_name=models.ForeignKey(customer,on_delete=models.CASCADE)
    retainer_invoice_number=models.CharField(max_length=255)
    refrences=models.CharField(max_length=255)
    retainer_invoice_date=models.DateField()
    total_amount=models.CharField(max_length=100)
    customer_notes=models.TextField()
    terms_and_conditions=models.TextField()
    is_draft=models.BooleanField(default=True)
    is_sent=models.BooleanField(default=False)

class Retaineritems(models.Model):
    retainer=models.ForeignKey(RetainerInvoice, on_delete=models.CASCADE)
    description=models.TextField()
    amount=models.CharField(max_length=100)
            
class Estimates(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    estimate_no = models.CharField(max_length=100,null=True,blank=True)
    reference = models.CharField(max_length=100,null=True,blank=True)
    estimate_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    tax_amount = models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    adjustment = models.FloatField(null=True,blank=True)
    total = models.FloatField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    customer_notes = models.CharField(max_length=250,null=True,blank=True)
    terms_conditions = models.CharField(max_length=250,null=True,blank=True)
    attachment = models.ImageField(upload_to="image/", null=True)   

class EstimateItems(models.Model):
    estimate = models.ForeignKey(Estimates,on_delete=models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    tax_percentage = models.IntegerField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)

class payment(models.Model):
    term=models.TextField(max_length=255)
    days=models.TextField(max_length=255)
    
class payment_terms(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Terms=models.CharField(max_length=100,null=True,blank=True)
    Days=models.IntegerField(null=True,blank=True)    

class invoice(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    invoice_no=models.TextField(max_length=255)
    terms=models.ForeignKey(payment_terms,on_delete=models.CASCADE)
    order_no=models.IntegerField()
    inv_date=models.DateField()
    due_date=models.DateField()
    igst=models.TextField(max_length=255)
    cgst=models.TextField(max_length=255)
    sgst=models.TextField(max_length=255)
    t_tax=models.FloatField()
    subtotal=models.FloatField()
    grandtotal=models.FloatField()
    cxnote=models.TextField(max_length=255)
    file=models.ImageField(upload_to='documents')
    terms_condition=models.TextField(max_length=255)
    status=models.TextField(max_length=255)
    
    def __str__(self) :
        return self.invoice_no
    
class invoice_item(models.Model):
    product=models.TextField(max_length=255)
    quantity=models.IntegerField()
    hsn=models.TextField(max_length=255)
    tax=models.IntegerField()
    total=models.FloatField()
    desc=models.TextField(max_length=255)
    rate=models.TextField(max_length=255)
    inv=models.ForeignKey(invoice,on_delete=models.CASCADE)


class Pricelist(models.Model):
    itemtable=models.ForeignKey(AddItem,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    types=models.CharField(max_length=255)
    tax=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    mark=models.CharField(max_length=255)
    percentage=models.IntegerField()
    roundoff=models.CharField(max_length=255)
    currency=models.CharField(max_length=255)
    status= models.TextField(default='active')
    
class Sample_table(models.Model):
    item_name=models.CharField(max_length=255)
    price=models.IntegerField()
    cust_rate=models.FloatField()
    pl=models.ForeignKey(Pricelist,on_delete=models.CASCADE)
    
    
class contact_person_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    vendor=models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    salutation=models.CharField(max_length=25)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=200)
    work_phone=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    skype_number=models.CharField(max_length=50)
    designation=models.CharField(max_length=50)
    department=models.CharField(max_length=50)

class remarks_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    vendor=models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    remarks=models.CharField(max_length=500)


class banking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=220,default='', null=True, blank=True)
    alias = models.CharField(max_length=220,default='', null=True, blank=True)
    acc_type = models.CharField(max_length=220,default='', null=True, blank=True)
    ac_holder = models.CharField(max_length=220,default='', null=True, blank=True)
    ac_no = models.CharField(max_length=220,default='', null=True, blank=True)
    ifsc = models.CharField(max_length=220,default='', null=True, blank=True)
    swift_code = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_name = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_branch = models.CharField(max_length=220,default='', null=True, blank=True)
    chq_book = models.CharField(max_length=220,default='', null=True, blank=True)
    chq_print = models.CharField(max_length=220,default='', null=True, blank=True)
    chq_config = models.CharField(max_length=220,default='', null=True, blank=True)
    mail_name = models.CharField(max_length=220,default='', null=True, blank=True)
    mail_addr = models.CharField(max_length=220,default='', null=True, blank=True)
    mail_country = models.CharField(max_length=220,default='', null=True, blank=True)
    mail_state = models.CharField(max_length=220,default='', null=True, blank=True)
    mail_pin = models.CharField(max_length=220,default='', null=True, blank=True)
    bd_bnk_det = models.CharField(max_length=220,default='', null=True, blank=True)
    bd_pan_no = models.CharField(max_length=220,default='', null=True, blank=True)
    bd_reg_typ = models.CharField(max_length=220,default='', null=True, blank=True)
    bd_gst_no = models.CharField(max_length=220,default='', null=True, blank=True)
    bd_gst_det = models.CharField(max_length=220,default='', null=True, blank=True)
    opening_bal =models.CharField(max_length=220,default='', null=True, blank=True)
    opening_blnc_type = models.CharField(max_length=220,default='', null=True, blank=True)

class bank(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    acc_type = models.CharField(max_length=220,default='', null=True, blank=True)
    bank_name = models.CharField(max_length=220,default='', null=True, blank=True)
    
class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    profile_name = models.CharField(max_length=255)
    repeat_every = models.CharField(max_length=50)
    start_date = models.DateField()
    ends_on = models.CharField(max_length=255,null=True)
    expense_account = models.CharField(max_length=255)
    expense_type = models.CharField(max_length=50)
    goods_label = models.CharField(max_length=255, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    paidthrough = models.CharField(max_length=50)
    vendor = models.ForeignKey(vendor_table, on_delete=models.CASCADE)
    gst = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    tax = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    customername = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True, null=True)
    activation_tag = models.CharField(max_length=255,default='')
    title = models.CharField(max_length=255,default='')
    document = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.profile_name

class Account(models.Model):
    accountType = models.CharField(max_length=255)
    accountName = models.CharField(max_length=255)
    accountCode = models.CharField(max_length=255)
    description = models.TextField() 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
class SalesOrder(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    sales_no=models.CharField(max_length=255,null=True,blank=True)
    reference=models.CharField(max_length=255,null=True,blank=True)
    sales_date=models.DateField(max_length=255,null=True,blank=True)
    ship_date=models.DateField(max_length=255,null=True,blank=True)
    sos=models.TextField(null=True,blank=True)
    sh_charge=models.CharField(null=True,blank=True,max_length=255)
    igst=models.TextField(max_length=255,null=True,blank=True)
    cgst=models.TextField(max_length=255,null=True,blank=True)
    sgst=models.TextField(max_length=255,null=True,blank=True)
    t_tax=models.FloatField(null=True,blank=True)
    subtotal=models.FloatField(null=True,blank=True)
    grandtotal=models.FloatField(null=True,blank=True)
    cxnote=models.TextField(max_length=255,null=True,blank=True)
    file=models.ImageField(upload_to='documents',null=True,blank=True)
    terms_condition=models.TextField(max_length=255,null=True,blank=True)
    status=models.TextField(max_length=255,null=True,blank=True)
    terms=models.ForeignKey(payment_terms,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) :
        return self.invoice_no
    

    
class sales_item(models.Model):
    product=models.TextField(max_length=255,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    hsn=models.TextField(max_length=255,null=True,blank=True)
    tax=models.IntegerField(null=True,blank=True)
    total=models.FloatField(null=True,blank=True)
    desc=models.TextField(max_length=255,null=True,blank=True)
    rate=models.TextField(max_length=255,null=True,blank=True)
    sale=models.ForeignKey(SalesOrder,on_delete=models.CASCADE,null=True,blank=True)
    
class DeliveryChellan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    customer_mailid = models.CharField(max_length=100,null=True,blank=True)
    chellan_no = models.CharField(max_length=100,null=True,blank=True)
    reference = models.CharField(max_length=100,null=True,blank=True)
    chellan_date = models.DateField(null=True)
    chellan_type = models.CharField(max_length=100,null=True,blank=True)    
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    tax_amount = models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    adjustment = models.FloatField(null=True,blank=True)
    total = models.FloatField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    customer_notes = models.CharField(max_length=250,null=True,blank=True)
    terms_conditions = models.CharField(max_length=250,null=True,blank=True)
    attachment = models.ImageField(upload_to="image/", null=True)  

class ChallanItems(models.Model):
    chellan = models.ForeignKey(DeliveryChellan,on_delete=models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    tax_percentage = models.IntegerField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    
    
class recurring_invoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cust_name=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    items=models.ForeignKey(AddItem,on_delete=models.CASCADE,null=True)
    cname=models.CharField(max_length=255)
    cemail=models.CharField(max_length=255,null=True,blank=True)
    cadrs=models.CharField(max_length=255,null=True,blank=True)
    p_supply=models.CharField(max_length=255)
    entry_type=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    order_num=models.CharField(max_length=255)
    every=models.CharField(max_length=255)
    start=models.DateField()
    end=models.DateField()
    terms=models.CharField(max_length=255)
    cust_note=models.TextField()
    conditions=models.TextField()
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    tax_amount = models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    adjustment = models.FloatField(null=True,blank=True)
    total = models.FloatField(null=True,blank=True)

class recur_itemtable(models.Model):
    
    ri=models.ForeignKey(recurring_invoice,on_delete=models.CASCADE,null=True)
    iname=models.CharField(max_length=255)
    quantity=models.FloatField(null=True,blank=True)
    rate=models.FloatField(null=True,blank=True)
    discount=models.FloatField(null=True,blank=True)
    tax=models.FloatField(null=True,blank=True)
    amt=models.FloatField(null=True,blank=True)

class payments_recur(models.Model):
    Terms=models.CharField(max_length=100,null=True,blank=True)
    Days=models.IntegerField(null=True,blank=True)

class recurring_bills(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    profile_name = models.CharField(max_length=100,null=True,blank=True)
    source_supply = models.CharField(max_length=100,null=True,blank=True)
    vendor_name = models.CharField(max_length=100,null=True,blank=True)
    vendor_gst_number = models.CharField(max_length=100,null=True,blank=True) #haripriya add
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    repeat_every = models.CharField(max_length=100,null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    payment_terms = models.CharField(max_length=100,null=True,blank=True)
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    tax_amount =  models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    adjustment = models.FloatField(null=True,blank=True)
    grand_total = models.FloatField(null=True,blank=True)
    note = models.CharField(max_length=255,null=True,blank=True)
    document=models.FileField(upload_to='doc/recurring_bills',null=True,blank=True)
    comments = models.CharField(max_length=255,null=True,blank=True)
    

class recurring_bills_items (models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    recur_bills = models.ForeignKey(recurring_bills,on_delete=models.CASCADE,null=True,blank=True)
    item = models.CharField(max_length=100,null=True,blank=True)
    account = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate=models.FloatField(null=True,blank=True)
    tax = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    
    
class Comment(models.Model):
    profile_name = models.CharField(max_length=255)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)

    def _str_(self):
        return self.comment
        

class repeat_every(models.Model):
    Terms=models.CharField(max_length=100,null=True,blank=True)
    
    
class payment_item(models.Model):
    vendor = models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    reference = models.TextField(max_length=255,null=True,blank=True)
    payment = models.TextField(max_length=255,null=True,blank=True) 
    date = models.DateField(max_length=255,null=True,blank=True)
    cash = models.TextField(max_length=255,null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    email = models.EmailField(max_length=255,null=True)
    balance = models.IntegerField(null=True,blank=True)
    current_balance = models.IntegerField(null=True,blank=True)
    
    
class Purchase_Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    
    vendor_name = models.CharField(max_length=100,null=True,blank=True)
    vendor_mail = models.CharField(max_length=100,null=True,blank=True)
    vendor_gst_traet = models.CharField(max_length=100,null=True,blank=True)
    vendor_gst_no = models.CharField(max_length=100,null=True,blank=True)
    

    Org_name = models.CharField(max_length=100,null=True,blank=True)
    Org_address = models.CharField(max_length=100,null=True,blank=True)
    Org_gst = models.CharField(max_length=100,null=True,blank=True)
    Org_street = models.CharField(max_length=100,null=True,blank=True)
    Org_state = models.CharField(max_length=100,null=True,blank=True)
    Org_city = models.CharField(max_length=100,null=True,blank=True)
    typ=   models.CharField(max_length=100,null=True,blank=True)
    Org_mail=models.CharField(max_length=100,null=True,blank=True)    ###### #add the fields to medel


    customer_name = models.CharField(max_length=100,null=True,blank=True)
    customer_mail = models.CharField(max_length=100,null=True,blank=True)
    customer_address = models.CharField(max_length=100,null=True,blank=True)
    customer_street = models.CharField(max_length=100,null=True,blank=True)
    customer_state = models.CharField(max_length=100,null=True,blank=True)
    customer_city = models.CharField(max_length=100,null=True,blank=True)


    Pur_no = models.CharField(max_length=100,null=True,blank=True)

    source_supply = models.CharField(max_length=100,null=True,blank=True)

    ref = models.CharField(max_length=100,null=True,blank=True)
    Ord_date=models.DateField(null=True,blank=True)
    exp_date=models.DateField(null=True,blank=True)
    payment_terms = models.CharField(max_length=100,null=True,blank=True)
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    tax_amount =  models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    grand_total = models.FloatField(null=True,blank=True)
    note = models.CharField(max_length=255,null=True,blank=True)
    document=models.FileField(upload_to='doc/purchase_order',null=True,blank=True)
    comments = models.CharField(max_length=255,null=True,blank=True)
    term=models.CharField(max_length=255,null=True,blank=True)
    status=models.CharField(max_length=255,default='Draft')

class Purchase_Order_items (models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    PO = models.ForeignKey(Purchase_Order,on_delete=models.CASCADE,null=True,blank=True)
    item = models.CharField(max_length=100,null=True,blank=True)
    account = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate=models.FloatField(null=True,blank=True)
    tax = models.CharField(max_length=100,blank=True,null=True)    ########## #replace the model 
    discount = models.FloatField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    
    
class payment_made_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    vendor = models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    reference = models.TextField(max_length=255,null=True,blank=True)
    payment = models.TextField(max_length=255,null=True,blank=True) 
    date = models.DateField(max_length=255,null=True,blank=True)
    cash = models.ForeignKey(banking,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(null=True,blank=True)
    email = models.EmailField(max_length=255,null=True)
    balance = models.IntegerField(null=True,blank=True)
    current_balance = models.IntegerField(null=True,blank=True)
    gst = models.TextField(max_length=255,null=True,blank=True)            
    
    
class Chart_of_Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    account_type = models.CharField(max_length=255,null=True,blank=True)
    account_name = models.CharField(max_length=255,null=True,blank=True)
    credit_no = models.CharField(max_length=255,null=True,blank=True)
    sub_account = models.CharField(max_length=255,null=True,blank=True)
    parent_account = models.CharField(max_length=255,null=True,blank=True)
    bank_account_no = models.CharField(max_length=255,null=True,blank=True)
    currency = models.CharField(max_length=255,null=True,blank=True)
    account_code = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    watchlist = models.CharField(max_length=255,null=True,blank=True)
    attachment=models.ImageField(upload_to="image/", null=True) 
    create_status=models.CharField(max_length=255,null=True,blank=True) 
    status = models.CharField(max_length=255,null=True,blank=True)

class Chart_of_Account_Upload(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    account=models.ForeignKey(Chart_of_Account,on_delete=models.CASCADE,null=True,blank=True)
    account_type=models.CharField(max_length=255,null=True,blank=True)
    account_name=models.CharField(max_length=255,null=True,blank=True)
    title=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    document=models.FileField(upload_to='docs/')
    
    
class project1(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    name=models.CharField(max_length=255,null=True,blank=True)
    desc=models.CharField(max_length=255,null=True,blank=True)
    c_name=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    billing=models.CharField(max_length=255,null=True,blank=True)
    rateperhour=models.CharField(max_length=255,null=True,blank=True)
    budget=models.CharField(max_length=255,null=True,blank=True)
    active = models.BooleanField(default = True)
    comment=models.CharField(max_length=255,null=True,blank=True)
    
    
class task(models.Model):
    proj=models.ForeignKey(project1,on_delete=models.CASCADE,null=True,blank=True)
    c_name=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    taskname=models.CharField(max_length=255,null=True,blank=True) 
    taskdes=models.CharField(max_length=255,null=True,blank=True)
    taskrph= models.CharField(max_length=255, null=True,blank=True) 
    BILLABLE_CHOICES = [
        ('Billed', 'Billed'),
        ('Not Billed', 'Not Billed'),
    ]
    billable = models.CharField(max_length=255,choices=BILLABLE_CHOICES, default='Not Billed',null=True,blank=True)
    

class usercreate(models.Model):
    projnn=models.ForeignKey(project1,on_delete=models.CASCADE,null=True,blank=True)
    userss=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    usernamezz=models.CharField(max_length=255, null=True,blank=True)
    emailzz=models.CharField(max_length=255, null=True,blank=True)
    
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.CharField(max_length=255,default='Active')

    def __str__(self):
        return self.name
        
        
class Comments_item(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    item=models.ForeignKey(AddItem,on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField(max_length=255,null=True,blank=True)
    # def __str__(self):
    #     return f"Comment by {self.user.username} on {self.item}"
    
    
class method(models.Model):
    option=models.TextField(max_length=255) 
    
    def __str__(self):
        return self.option
    
    
class payment_made(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    vendor = models.ForeignKey(vendor_table,on_delete=models.CASCADE,null=True)
    reference = models.TextField(max_length=255,null=True,blank=True)
    payment = models.ForeignKey(method, on_delete=models.CASCADE, null=True)  # Changed this line
    date = models.DateField(max_length=255,null=True,blank=True)
    cash = models.CharField(max_length=255,null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    email = models.EmailField(max_length=255,null=True)
    balance = models.IntegerField(null=True,blank=True)
    current_balance = models.IntegerField(null=True,blank=True)
    gst = models.TextField(max_length=255,null=True,blank=True)    
    
    
class Payroll(models.Model):
    title = models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True)
    alias = models.CharField(max_length=100)
    image=models.ImageField(upload_to="image/", null=True)
    joindate=models.DateField()
    salary_type = models.CharField(max_length=100, default='Fixed')
    salary = models.IntegerField(null=True,blank=True)
    emp_number = models.CharField(max_length=100,null=True)
    designation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob=models.DateField()
    blood = models.CharField(max_length=10)
    parent = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    permanent_address = models.CharField(max_length=250,null=True)
    Phone = models.BigIntegerField()
    emergency_phone = models.BigIntegerField(null=True ,blank=True,default=1)
    email = models.EmailField(max_length=255,null=True)
    ITN = models.IntegerField(null=True)
    Aadhar = models.CharField(max_length=250,default='')
    UAN = models.IntegerField(null=True)
    PFN = models.IntegerField(null=True)
    PRAN = models.IntegerField(null=True)
    status=models.CharField(max_length=200,default='Active')
    isTDS=models.CharField(max_length=200,null=True)
    TDS = models.IntegerField(null=True,default=0)
    
    
class Bankdetails(models.Model):
    acc_no = models.BigIntegerField()  
    IFSC = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=100)
    payroll=models.ForeignKey(Payroll,on_delete=models.CASCADE,default='')
    
    
class Commentmodel(models.Model):
    comment=models.CharField(max_length=300)
    payroll=models.ForeignKey(Payroll,on_delete=models.CASCADE)
    
    
###############expense
class AccountE(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    account_type = models.CharField(max_length=255,null=True,blank=True)
    account_name = models.CharField(max_length=255,null=True,blank=True)
    credit_no = models.CharField(max_length=255,null=True,blank=True)
    sub_account = models.CharField(max_length=255,null=True,blank=True)
    parent_account = models.CharField(max_length=255,null=True,blank=True)
    bank_account_no = models.CharField(max_length=255,null=True,blank=True)
    currency = models.CharField(max_length=255,null=True,blank=True)
    account_code = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    watchlist = models.CharField(max_length=255,null=True,blank=True)
    attachment=models.ImageField(upload_to="image/", null=True) 
    create_status=models.CharField(max_length=255,null=True,blank=True) 
    status = models.CharField(max_length=255,null=True,blank=True)     
    
    
class addcustomerE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name= models.CharField(max_length=100,null=True,blank=True)
    customerType= models.CharField(max_length=100,null=True,blank=True)
    companyName= models.CharField(max_length=100,null=True,blank=True)
    customerEmail= models.CharField(max_length=100,null=True,blank=True)
    customerWorkPhone= models.CharField(max_length=100,null=True,blank=True)
    customerMobile= models.CharField(max_length=100,null=True,blank=True)
    skype=models.CharField(max_length=100,null=True,blank=True)
    designation=models.CharField(max_length=100,null=True,blank=True)
    department=models.CharField(max_length=100,null=True,blank=True)
    website=models.CharField(max_length=100,null=True,blank=True)
    GSTTreatment=models.CharField(max_length=100,null=True,blank=True)
    placeofsupply=models.CharField(max_length=100,null=True,blank=True)
    Taxpreference=models.CharField(max_length=100,null=True,blank=True)
    currency=models.CharField(max_length=100,null=True,blank=True)
    OpeningBalance=models.CharField(max_length=100,default='',null=True,blank=True)
    PaymentTerms=models.CharField(max_length=100,null=True,blank=True)
    PriceList=models.CharField(max_length=100,null=True,blank=True)

    PortalLanguage=models.CharField(max_length=100,null=True,blank=True)
    Facebook=models.CharField(max_length=100,null=True,blank=True)
    Twitter=models.CharField(max_length=100,null=True,blank=True)
    Attention=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    Address1=models.CharField(max_length=100,null=True,blank=True)
    Address2=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.CharField(max_length=100,null=True,blank=True)
    phone1=models.CharField(max_length=100,null=True,blank=True)
    fax=models.CharField(max_length=100,null=True,blank=True)

    CPsalutation=models.CharField(max_length=100,null=True,blank=True)
    Firstname=models.CharField(max_length=100,null=True,blank=True)
    Lastname=models.CharField(max_length=100,null=True,blank=True)
    CPemail=models.CharField(max_length=100,null=True,blank=True)
    CPphone=models.CharField(max_length=100,null=True,blank=True)
    CPmobile=models.CharField(max_length=100,null=True,blank=True)
    CPskype=models.CharField(max_length=100,null=True,blank=True)
    CPdesignation=models.CharField(max_length=100,null=True,blank=True)
    CPdepartment=models.CharField(max_length=100,null=True,blank=True)
    
    
class vendor_tableE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salutation=models.CharField(max_length=25,null=True,blank=True)
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    company_name=models.CharField(max_length=150,null=True,blank=True)
    vendor_display_name=models.CharField(max_length=150,default='',null=True,blank=True)
    vendor_email=models.CharField(max_length=250,default='',null=True,blank=True)
    vendor_wphone=models.CharField(max_length=50,default='',null=True,blank=True)
    vendor_mphone=models.CharField(max_length=50,default='',null=True,blank=True)
    skype_number=models.CharField(max_length=50,default='',null=True,blank=True)
    designation=models.CharField(max_length=50,default='',null=True,blank=True)
    department=models.CharField(max_length=50,default='',null=True,blank=True)
    website=models.CharField(max_length=250,default='',null=True,blank=True)
    gst_treatment=models.CharField(max_length=100,default='',null=True,blank=True)
    gst_number=models.CharField(max_length=50,default='',null=True,blank=True)
    pan_number=models.CharField(max_length=50,default='',null=True,blank=True)
    source_supply=models.CharField(max_length=100,default='',null=True,blank=True)
    currency=models.CharField(max_length=50,default='',null=True,blank=True)
    opening_bal=models.CharField(max_length=100,default='',null=True,blank=True)
    payment_terms=models.CharField(max_length=100,default='',null=True,blank=True)
    battention=models.CharField(max_length=100,default='',null=True,blank=True)
    bcountry=models.CharField(max_length=100,default='',null=True,blank=True)
    baddress=models.CharField(max_length=300,default='',null=True,blank=True)
    bcity=models.CharField(max_length=100,default='',null=True,blank=True)
    bstate=models.CharField(max_length=100,default='',null=True,blank=True)
    bzip=models.CharField(max_length=100,default='',null=True,blank=True)
    bphone=models.CharField(max_length=100,default='',null=True,blank=True)
    bfax=models.CharField(max_length=100,default='',null=True,blank=True)
    sattention=models.CharField(max_length=100,default='',null=True,blank=True)
    scountry=models.CharField(max_length=100,default='',null=True,blank=True)
    saddress=models.CharField(max_length=300,default='',null=True,blank=True)
    scity=models.CharField(max_length=100,default='',null=True,blank=True)
    sstate=models.CharField(max_length=100,default='',null=True,blank=True)
    szip=models.CharField(max_length=100,default='',null=True,blank=True)
    sphone=models.CharField(max_length=100,default='',null=True,blank=True)
    sfax=models.CharField(max_length=100,default='',null=True,blank=True)
    
    
class ExpenseE(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    expense_account=models.CharField(max_length=100,default="",null=True, blank=True)
    # expense_account=models.ForeignKey(AccountE,on_delete=models.CASCADE)
    amount=models.TextField(max_length=255,null=True, blank=True)
    currency=models.TextField(max_length=255,null=True, blank=True)
    expense_type=models.TextField(max_length=255,null=True, blank=True)
    paid=models.TextField(max_length=255,null=True, blank=True)
    vendor= models.ForeignKey(vendor_table, on_delete=models.CASCADE,null=True, blank=True)
    notes=models.TextField(max_length=255,null=True, blank=True)
    hsn_code=models.TextField(max_length=255,null=True, blank=True)
    gst_treatment =models.TextField(max_length=255,null=True, blank=True)
    gstin=models.TextField(max_length=255,null=True, blank=True)
    destination_of_supply=models.TextField(max_length=255,null=True, blank=True)
    reverse_charge=models.TextField(max_length=255,null=True, blank=True)
    tax=models.TextField(max_length=255,null=True, blank=True)
    invoice=models.TextField(max_length=255,null=True, blank=True)
    # vendor=models.CharField(max_length=100,default='')
    # customer_name= models.CharField(max_length=100,default='')
    customer_name = models.ForeignKey(customer, on_delete=models.CASCADE,null=True, blank=True)
    reporting_tags=models.TextField(max_length=255,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    sac=models.TextField(max_length=255,null=True, blank=True)
    taxamt=models.TextField(max_length=255,null=True, blank=True)
    image = models.FileField(upload_to='expense_image/', blank=True, null=True)
    
    
class AttachE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
    expense = models.ForeignKey(ExpenseE, on_delete=models.CASCADE, null=True)
    attachment= models.FileField(upload_to='attachment/', blank=True, null=True)
    
    
class Payrollfiles(models.Model):
    attachment=models.FileField(upload_to='doc/',null=True)
    payroll=models.ForeignKey(Payroll,on_delete=models.CASCADE)
    
    
class usernamez(models.Model):
    projn=models.ForeignKey(project1,on_delete=models.CASCADE,null=True,blank=True)
    users=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    usernamez=models.CharField(max_length=255, null=True,blank=True)
    emailz=models.CharField(max_length=255, null=True,blank=True)
    
    
    
class estimate_comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    estimate=models.ForeignKey(Estimates,on_delete=models.CASCADE,null=True,blank=True)
    comments=models.CharField(max_length=500,null=True,blank=True)
    
    
    
class Vendor_Credits(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    company_name=models.CharField(max_length=150)
    vendor_email=models.CharField(max_length=250)
    gst_treatment=models.CharField(max_length=100)
    source_supply=models.CharField(max_length=100)
    baddress=models.CharField(max_length=300,default='')
    credit_note = models.CharField(max_length=100, null=True, blank=True)
    order_no = models.CharField(max_length=100, null=True, blank=True)
    adjustment = models.CharField(max_length=100, null=True, blank=True)
    vendor_date = models.DateField()
    
    igst=models.TextField(max_length=255)
    cgst=models.TextField(max_length=255)
    sgst=models.TextField(max_length=255)
    t_tax=models.FloatField()
    subtotal=models.FloatField()
    grandtotal=models.FloatField()
    cxnote=models.TextField(max_length=255)
    file=models.ImageField(upload_to='documents')
    # terms_condition=models.TextField(max_length=255)
    status=models.TextField(max_length=255)
    
    
class Vendor_invoice_item(models.Model):
    product=models.TextField(max_length=255)
    quantity=models.IntegerField()
    hsn=models.TextField(max_length=255)
    tax=models.IntegerField()
    total=models.FloatField()
    discount=models.TextField(max_length=255)
    rate=models.TextField(max_length=255)
    inv = models.ForeignKey(Vendor_Credits, on_delete=models.CASCADE)
    
    
# Vendor Credits

class Vendor_Credits_Bills(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    vendor_name = models.CharField(max_length=100,null=True,blank=True)
    source_supply = models.CharField(max_length=100,null=True,blank=True)
    gst_number=models.CharField(max_length=150, null=True, blank=True)
    vendor_email=models.CharField(max_length=250)
    gst_treatment=models.CharField(max_length=100) 
    credit_note = models.CharField(max_length=100, null=True, blank=True)
    order_no = models.CharField(max_length=100, null=True, blank=True)
    vendor_date = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    tax_amount =  models.FloatField(null=True,blank=True)
    adjustment = models.FloatField(null=True,blank=True)
    grand_total = models.FloatField(null=True,blank=True)
    note = models.CharField(max_length=255,null=True,blank=True)
    document=models.FileField(upload_to='doc/Vendor_Credits_Bills',null=True,blank=True)
    comments = models.CharField(max_length=255,null=True,blank=True)
    
    
class Vendor_Credits_Bills_items_bills (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company_details,on_delete=models.CASCADE,null=True,blank=True)
    recur_bills = models.ForeignKey(Vendor_Credits_Bills,on_delete=models.CASCADE,null=True,blank=True)
    item = models.CharField(max_length=100,null=True,blank=True)
    account = models.CharField(max_length=100,null=True,blank=True)
    hsn = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate=models.FloatField(null=True,blank=True)
    tax = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    
class Credits_comments_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(Vendor_Credits_Bills,on_delete=models.CASCADE,null=True)
    comment=models.TextField(max_length=500)
    
    
class Credits_mail_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(Vendor_Credits_Bills,on_delete=models.CASCADE,null=True)
    mail_from=models.TextField(max_length=300)
    mail_to=models.TextField(max_length=300)
    subject=models.TextField(max_length=250)
    content=models.TextField(max_length=900)
    mail_date=models.DateTimeField(auto_now_add=True)
    
    
class Credits_doc_upload_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    vendor=models.ForeignKey(Vendor_Credits_Bills,on_delete=models.CASCADE,null=True)
    title=models.TextField(max_length=200)
    document=models.FileField(upload_to='doc/')
    
    
#-------------------------------------------------sumayya--------purchase bills------------------------------------------
class PurchaseBills(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    customer_email = models.CharField(max_length=100,null=True,blank=True)
    place_of_supply = models.CharField(max_length=100,null=True,blank=True)
    vendor_name = models.CharField(max_length=100,null=True,blank=True)
    vendor_email = models.CharField(max_length=100,null=True,blank=True)
    vendor_gst_no = models.CharField(max_length=100,null=True,blank=True)
    source_of_supply = models.CharField(max_length=100,null=True,blank=True)
    bill_no = models.CharField(max_length=100,null=True,blank=True)
    order_number = models.CharField(max_length=100,null=True,blank=True)
    bill_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    payment_terms = models.CharField(max_length=100,null=True,blank=True)
    sub_total = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    tax_amount = models.FloatField(null=True,blank=True)
    shipping_charge = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    total = models.FloatField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    attachment = models.ImageField(upload_to="image/", null=True)  
    comments = models.CharField(max_length=100,null=True,blank=True)
    
    
class PurchaseBillItems(models.Model):
    purchase_bill = models.ForeignKey(PurchaseBills,on_delete=models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=100,null=True,blank=True)
    account = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    tax_percentage = models.IntegerField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    
    
class payment_termsE(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Terms=models.CharField(max_length=100,null=True,blank=True)
    Days=models.IntegerField(null=True,blank=True)    
    
class customer_mail_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    customr=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    mail_from=models.TextField(max_length=300)
    mail_to=models.TextField(max_length=300)
    subject=models.TextField(max_length=250)
    content=models.TextField(max_length=900)
    mail_date=models.DateTimeField(auto_now_add=True) 
    
    
class customer_doc_upload_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    customr=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    title=models.TextField(max_length=200)
    document=models.FileField(upload_to='doc/')
    
    
class customer_comments_table(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default='')
    customr=models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    comment=models.TextField(max_length=500) 
    
    
##Reshna-banking
class Bankcreation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=220,default='', null=True, blank=True)
    branch = models.CharField(max_length=220,default='', null=True, blank=True)
    ac_no = models.CharField(max_length=220,default='', null=True, blank=True)
    ifsc = models.CharField(max_length=220,default='', null=True, blank=True)
    opn_bal =models.FloatField(null=True, blank=True)
    bal_type=models.CharField(max_length=220,default='', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    document=models.FileField(upload_to='bank/',null=True,blank=True)
    status= models.TextField(default='Active')
    
    
class transactions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bank=models.ForeignKey(Bankcreation, on_delete=models.CASCADE,null=True, blank=True)
    fromB=models.CharField(max_length=220,default='', null=True, blank=True)
    toB=models.CharField(max_length=220,default='', null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description=models.CharField(max_length=220,default='', null=True, blank=True)
    type=models.CharField(max_length=220,default='', null=True, blank=True)
    adjtype=models.CharField(max_length=220,default='', null=True, blank=True)
    adjacname=models.CharField(max_length=220,default='', null=True, blank=True)
    
class Transportation(models.Model):
    method = models.CharField(max_length=100)

    def __str__(self):
        return self.method 

class EWayBill(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cust=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    doc = models.CharField(max_length=50,null=True)
    transsub = models.CharField(max_length=50,null=True)
    customerzz = models.CharField(max_length=100,null=True)
    cemail=models.EmailField(max_length=255,null=True)
    cgst_trt_inp = models.CharField(max_length=100,null=True)
    cgstin_inp = models.CharField(max_length=100,null=True)
    invoiceno = models.CharField(max_length=50,null=True)
    date = models.DateField()
    trans = models.CharField(max_length=100,null=True)
    adda = models.TextField(max_length=255,null=True)
    addb = models.TextField(max_length=255,null=True)
    srcofsupply = models.CharField(max_length=100,null=True)
    transportation = models.CharField(max_length=100,null=True)
    km = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    vno = models.CharField(max_length=50,null=True) 
    sub_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    adj = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    note = models.TextField(max_length=255,null=True)
    comment = models.CharField(max_length=255,null=True,blank=True)
    
    
class EWayBillItem(models.Model):
    eway_bill = models.ForeignKey(EWayBill, on_delete=models.CASCADE)
    item = models.CharField(max_length=100,null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)     