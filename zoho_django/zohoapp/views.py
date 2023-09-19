from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.utils.text import capfirst
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views import View
from .forms import EmailForm
from django.http import JsonResponse
from datetime import datetime,date, timedelta
from xhtml2pdf import pisa
from django.template.loader import get_template
from bs4 import BeautifulSoup
import io
import os
import json
from django.template import Context, Template
import tempfile
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import FileResponse
from django.urls import reverse
from django.db.models import Sum
from itertools import groupby


def index(request):

    return render(request,'landpage.html')

def register(request):
    if request.method=='POST':

        first_name=capfirst(request.POST['fname'])
        last_name=capfirst(request.POST['lname'])
        username=request.POST['uname']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email1']
        phone = request.POST['phone']

      
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                return redirect('register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                
                user.save()
                u = User.objects.get(id = user.id)

                company_details(contact_number = phone, user = u).save()
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('register')   
        return redirect('register')

    return render(request,'register.html',{'msg' : messages})

def login(request):
        
    if request.method == 'POST':
        
        email_or_username = request.POST['emailorusername']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=email_or_username, password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            # .........................................................
            user=request.user        
            account_info = [{"user": user, "account_type": "Accounts Payable","account_name":"Accounts Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This is an account of all the money which you owe to others like a pending bill payment to a vendor,etc.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Accounts Receivable","account_name":"Accounts Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The money that customers owe you becomes the accounts receivable. A good example of this is a payment expected from an invoice sent to your customer.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Advertising and Marketing","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Your expenses on promotional, marketing and advertising activities like banners, web-adds, trade shows, etc. are recorded in advertising and marketing account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Advance Tax","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any tax which is paid in advance is recorded into the advance tax account. This advance tax payment could be a quarterly, half yearly or yearly payment","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Automobile Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Transportation related expenses like fuel charges and maintenance charges for automobiles, are included to the automobile expense account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Bad Debt","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any amount which is lost and is unrecoverable is recorded into the bad debt account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Bank Fees and Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Any bank fees levied is recorded into the bank fees and charges account. A bank account maintenance fee, transaction charges, a late payment fee are some examples.","watchlist":"","create_status":"default","status":"active"},
            
            {"user": user, "account_type": "Expense","account_name":"Consultant Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Charges for availing the services of a consultant is recorded as a consultant expenses. The fees paid to a soft skills consultant to impart personality development training for your employees is a good example.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Cost of Goods Sold","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account which tracks the value of the goods sold.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Credit Card Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Service fees for transactions , balance transfer fees, annual credit fees and other charges levied on a credit card are recorded into the credit card account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Depreciation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any depreciation in value of your assets can be captured as a depreciation expense.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Depreciation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any depreciation in value of your assets can be captured as a depreciation expense.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Income","account_name":"Discount","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any reduction on your selling price as a discount can be recorded into the discount account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Drawings","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The money withdrawn from a business by its owner can be tracked with this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Employee Advance","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Money paid out to an employee in advance can be tracked here till it's repaid or shown to be spent for company purposes","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Employee Reimbursements","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account can be used to track the reimbursements that are due to be paid out to employees.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Expense","account_name":"Exchange Gain or Loss","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Changing the conversion rate can result in a gain or a loss. You can record this into the exchange gain or loss account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Fixed Asset","account_name":"Furniture and Equipment","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Purchases of furniture and equipment for your office that can be used for a long period of time usually exceeding one year can be tracked with this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"General Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A general category of account where you can record any income which cannot be recorded into any other category","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Interest Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A percentage of your balances and deposits are given as interest to you by your banks and financial institutions. This interest is recorded into the interest income account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Stock","account_name":"Inventory Asset","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An account which tracks the value of goods in your inventory.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"IT and Internet Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Money spent on your IT infrastructure and usage like internet connection, purchasing computer equipment etc is recorded as an IT and Computer Expense","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Janitorial Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"All your janitorial and cleaning expenses are recorded into the janitorial expenses account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Late Fee Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any late fee income is recorded into the late fee income account. The late fee is levied when the payment for an invoice is not received by the due date","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Lodging","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any expense related to putting up at motels etc while on business travel can be entered here.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Meals and Entertainment","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Expenses on food and entertainment are recorded into this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Office Supplies","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"All expenses on purchasing office supplies like stationery are recorded into the office supplies account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"Opening Balance Adjustments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account will hold the difference in the debits and credits entered during the opening balance.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Opening Balance Offset","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This is an account where you can record the balance from your previous years earning or the amount set aside for some activities. It is like a buffer account for your funds.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Other Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Miscellaneous charges like adjustments made to the invoice can be recorded in this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Other Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Any minor expense on activities unrelated to primary business operations is recorded under the other expense account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Owner's Equity","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The owners rights to the assets of a company can be quantified in the owner's equity account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Cash","account_name":"Petty Cash","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"It is a small amount of cash that is used to pay your minor or casual expenses rather than writing a check.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Postage","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Your expenses on ground mails, shipping and air mails can be recorded under the postage account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Prepaid Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An asset account that reports amounts paid in advance while purchasing goods or services from a vendor.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Printing and Stationery","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Expenses incurred by the organization towards printing and stationery.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Rent Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The rent paid for your office or any space related to your business can be recorded as a rental expense.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Repairs and Maintenance","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The costs involved in maintenance and repair of assets is recorded under this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Retained Earnings","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The earnings of your company which are not distributed among the share holders is accounted as retained earnings.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Salaries and Employee Wages","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Salaries for your employees and the wages paid to workers are recorded under the salaries and wages account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Sales","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" The income from the sales in your business is recorded under the sales account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Shipping Charge","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Shipping charges made to the invoice will be recorded in this account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Liability","account_name":"Tag Adjustments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" This adjustment account tracks the transfers between different reporting tags.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Tax Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The amount of money which you owe to your tax authority is recorded under the tax payable account. This amount is a sum of your outstanding in taxes and the tax charged on sales.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Telephone Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The expenses on your telephone, mobile and fax usage are accounted as telephone expenses.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Travel Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Expenses on business travels like hotel bookings, flight charges, etc. are recorded as travel expenses.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Uncategorized","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account can be used to temporarily track expenses that are yet to be identified and classified into a particular category.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Cash","account_name":"Undeposited Funds","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Record funds received by your company yet to be deposited in a bank as undeposited funds and group them as a current asset in your balance sheet.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Unearned Revenue","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A liability account that reports amounts received in advance of providing goods or services. When the goods or services are provided, this account balance is decreased and a revenue account is increased.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Capital Stock","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" An equity account that tracks the capital introduced when a business is operated through a company or corporation.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Long Term Liability","account_name":"Construction Loans","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount you repay for construction loans.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Contract Assets","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An asset account to track the amount that you receive from your customers while you're yet to complete rendering the services.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Depreciation And Amortisation","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that is used to track the depreciation of tangible assets and intangible assets, which is amortization.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Distributions","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account that tracks the payment of stock, cash or physical products to its shareholders.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Dividends Paid","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account to track the dividends paid when a corporation declares dividend on its common stock.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"GST Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output CGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output IGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output SGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Equity","account_name":"Investments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account used to track the amount that you invest.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Job Costing","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the costs that you incur in performing a job or a task.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Labor","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount that you pay as labor.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Materials","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount you use in purchasing materials.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Merchandise","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on purchasing merchandise.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Long Term Liability","account_name":"Mortgages","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amounts you pay for the mortgage loan.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Raw Materials And Consumables","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on purchasing raw materials and consumables.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Reverse Charge Tax Input but not due","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The amount of tax payable for your reverse charge purchases can be tracked here.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Sales to Customers (Cash)","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Subcontractor","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" An expense account to track the amount that you pay subcontractors who provide service to you.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Assets","account_name":"GST TCS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"GST TDS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Assets","account_name":"Input Tax Credits","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input CGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input IGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input SGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"TDS Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"TDS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Transportation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on transporting goods or providing services.","watchlist":"","create_status":"default","status":"active"},




            ]
            print(account_info[0])
            print(account_info[1])

            for account in account_info:
                print(account)
                if not Chart_of_Account.objects.filter(account_name=account['account_name']).exists():
                    new_account = Chart_of_Account(user=account['user'],account_name=account['account_name'],account_type=account['account_type'],credit_no=account['credit_no'],sub_account=account['sub_account'],parent_account=account['parent_account'],bank_account_no=account['bank_account_no'],currency=account['currency'],account_code=account['account_code'],description=account['description'],watchlist=account['watchlist'],create_status=account['create_status'],status=account['status'])
                    new_account.save()

            

            return redirect('dashboard')
           
        else:
            return redirect('/')
        

    return render(request, 'register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def forgotpassword(request):
     return render(request,'setpassword.html')

def setnewpassword(request):

    if request.method=='POST':
        email_or_username = request.POST['emailorusername']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:

            c = User.objects.filter(Q(username = email_or_username)|Q(email = email_or_username)).first()
            c.set_password(password)
            c.save()

        return redirect('register' )
        
    else:
        return render(request, 'setpassword.html')

@login_required(login_url='login')
def base(request):
   
       
    if not Unit.objects.filter(unit='BOX').exists():
            Unit(unit='BOX').save()
    if not Unit.objects.filter(unit='UNIT').exists():
            Unit(unit='UNIT').save()
    if not Unit.objects.filter(unit='LITRE').exists():
            Unit(unit='LITRE').save()
    if not Unit.objects.filter(unit='DOZEN').exists():
            Unit(unit='DOZEN').save()
    if not Unit.objects.filter(unit='DOZEN').exists():
            Unit(unit='DOZEN').save()
    if not Unit.objects.filter(unit='GRAMS').exists():
            Unit(unit='GRAMS').save()
    if not Unit.objects.filter(unit='KILOGRAMS').exists():
            Unit(unit='KILOGRAMS').save()
    if not Unit.objects.filter(unit='METERS').exists():
            Unit(unit='METERS').save()
    if not Unit.objects.filter(unit='TABLETS').exists():
            Unit(unit='TABLETS').save()
    if not Unit.objects.filter(unit='PIECES').exists():
            Unit(unit='PIECES').save()
    if not Unit.objects.filter(unit='PAIRS').exists():
            Unit(unit='PAIRS').save()

    if not Sales.objects.filter(Account_name='General Income').exists():
            Sales(Account_type='INCOME',Account_name='General Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Intrest Income').exists():
            Sales(Account_type='INCOME',Account_name='Intrest Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Late fee Income').exists():
            Sales(Account_type='INCOME',Account_name='Late fee Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Discount Income').exists():
            Sales(Account_type='INCOME',Account_name='Discount Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Other Charges').exists():
            Sales(Account_type='INCOME',Account_name='Other Charges',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Shipping Charge').exists():
            Sales(Account_type='INCOME',Account_name='Shipping Charge',Account_desc='salesincome').save()
    


   
    if not  Purchase.objects.filter(Account_name='Advertising & Markting').exists():        
        Purchase(Account_type='EXPENCES',Account_name='Advertising & Markting',Account_desc='Advertsing Exp').save()
    
    if not Purchase.objects.filter(Account_name='Debit Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Debit Charge',Account_desc='Debited Exp').save()
    if not Purchase.objects.filter(Account_name='Labour Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Labour Charge',Account_desc='Labour Exp').save()
    if not Purchase.objects.filter(Account_name='Raw Meterials').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw Meterials',Account_desc='Raw Meterials Exp').save()
    if not Purchase.objects.filter(Account_name='Automobile Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Automobile Expense',Account_desc='Automobile Expense').save()
    if not Purchase.objects.filter(Account_name='Bad Debt').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bad Debt',Account_desc='Bad Debt').save()
    if not Purchase.objects.filter(Account_name='Bank Fees and Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bank Fees and Charges',Account_desc='Bank Fees and Charges').save()
    if not Purchase.objects.filter(Account_name='Consultant Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Consultant Expense',Account_desc='Consultant Expense').save()
    if not Purchase.objects.filter(Account_name='Credit card Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Credit card Charges',Account_desc='Credit card Charges').save()
    if not Purchase.objects.filter(Account_name='Depreciation Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation Charges',Account_desc='Depreciation Charges').save()
    if not Purchase.objects.filter(Account_name='IT and Internet Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='IT and Internet Expense',Account_desc='IT and Internet Expense').save()
    if not Purchase.objects.filter(Account_name='Janitorial Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Janitorial Expense',Account_desc='Janitorial Expense').save()
    if not Purchase.objects.filter(Account_name='Lodging').exists():
            Purchase(Account_type='EXPENCES',Account_name='Lodging',Account_desc='Lodging').save()
    if not Purchase.objects.filter(Account_name='Meals and Entertinment').exists():
            Purchase(Account_type='EXPENCES',Account_name='Meals and Entertinment',Account_desc='Meals and Entertinment').save()
    if not Purchase.objects.filter(Account_name='Office Supplies').exists():
            Purchase(Account_type='EXPENCES',Account_name='Office Supplies',Account_desc='Office Supplies').save()
    if not Purchase.objects.filter(Account_name='Other Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Other Expenses',Account_desc='Other Expenses').save()
            
    if not Purchase.objects.filter(Account_name='Postage').exists():
            Purchase(Account_type='EXPENCES',Account_name='Postage',Account_desc='Postage').save()
    if not Purchase.objects.filter(Account_name='Printing and sationary').exists():
            Purchase(Account_type='EXPENCES',Account_name='Printing and sationary',Account_desc='Printing and sationary').save()
    if not Purchase.objects.filter(Account_name='Rent Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Rent Expenses',Account_desc='Rent Expenses').save()
    if not Purchase.objects.filter(Account_name='Repair and maintenance').exists():
            Purchase(Account_type='EXPENCES',Account_name='Repair and maintenance',Account_desc='Repair and maintenance').save()
    if not Purchase.objects.filter(Account_name='Salaries and Employee wages').exists():
            Purchase(Account_type='EXPENCES',Account_name='Salaries and Employee wages',Account_desc='Salaries and Employee wages').save()
    if not Purchase.objects.filter(Account_name='Telephonic Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Telephonic Expenses',Account_desc='Telephonic Expenses').save()
    if not Purchase.objects.filter(Account_name='Travel Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Travel Expenses',Account_desc='Travel Expenses').save()
    if not Purchase.objects.filter(Account_name='Uncategorized').exists():
            Purchase(Account_type='EXPENCES',Account_name='Uncategorized',Account_desc='Uncategorized').save()
    if not Purchase.objects.filter(Account_name='Contract Assets').exists():
            Purchase(Account_type='EXPENCES',Account_name='Contract Assets',Account_desc='Contract Assets').save()
    if not Purchase.objects.filter(Account_name='Depreciation and Amoritisation').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation and Amoritisation',Account_desc='Depreciation and Amoritisation').save()
    if not Purchase.objects.filter(Account_name='Merchandise').exists():
            Purchase(Account_type='EXPENCES',Account_name='Merchandise',Account_desc='Merchandise').save()
    if not Purchase.objects.filter(Account_name='Raw material and Consumables').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw material and Consumables',Account_desc='Raw material and Consumables').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Cost Of Goods Sold').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Cost Of Goods Sold',Account_desc='Cost Of Goods Sold').save()
    if not Purchase.objects.filter(Account_name='Job Costing').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Job Costing',Account_desc='Job Costing').save()
    if not Purchase.objects.filter(Account_name='Labour').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Labour',Account_desc='Labour').save()
    if not Purchase.objects.filter(Account_name='Materials').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Materials',Account_desc='Materials').save()
    if not Purchase.objects.filter(Account_name='Subcontractor').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Subcontractor',Account_desc='Subcontractor').save()
    if not Purchase.objects.filter(Account_name='Furniture and Equipment').exists():
            Purchase(Account_type='Fixed Asset',Account_name='Furniture and Equipment',Account_desc='Furniture and Equipment').save()
    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'loginhome.html',context)


@login_required(login_url='login')
def view_profile(request):

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'profile.html',context)

@login_required(login_url='login')
def edit_profile(request,pk):

    company = company_details.objects.get(id = pk)
    user1 = User.objects.get(id = company.user_id)

    if request.method == "POST":

        user1.first_name = capfirst(request.POST.get('f_name'))
        user1.last_name  = capfirst(request.POST.get('l_name'))
        user1.email = request.POST.get('email')
        company.contact_number = request.POST.get('cnum')
        company.address = capfirst(request.POST.get('ards'))
        company.company_name = request.POST.get('comp_name')
        company.company_email = request.POST.get('comp_email')
        company.city = request.POST.get('city')
        company.state = request.POST.get('state')
        company.country = request.POST.get('country')
        company.pincode = request.POST.get('pinc')
        company.gst_num = request.POST.get('gst')
        company.pan_num = request.POST.get('pan')
        company.business_name = request.POST.get('bname')
        company.company_type = request.POST.get('comp_type')
        if len(request.FILES)!=0 :
            company.profile_pic = request.FILES.get('file')

        company.save()
        user1.save()
        return redirect('view_profile')

    context = {
        'company' : company,
        'user1' : user1,
    }
    
    return render(request,'edit_profile.html',context)

@login_required(login_url='login')
def itemview(request):
    company = company_details.objects.get(user = request.user)
    viewitem=AddItem.objects.all()
    return render(request,'item_view.html',{'view':viewitem,'company':company})


@login_required(login_url='login')
def additem(request):
    company=company_details.objects.get(user=request.user)
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem.html',{'unit':unit,'sale':sale,'purchase':purchase,'company':company,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

@login_required(login_url='login')
def add_account(request):
    if request.method=='POST':
        Account_type  =request.POST.get('acc_type')
        if Account_type is not None:
            Account_name =request.POST['acc_name']
            Account_desc =request.POST['acc_desc']
        
            acc=Purchase(Account_type=Account_type,Account_name=Account_name,Account_desc=Account_desc)
            acc.save() 
            account_id=acc.id 
                           
            return JsonResponse({"Account_type":Account_type,"Account_name":Account_name,"Account_desc":Account_desc,'account_id':account_id})
        
    return render(request,'additem.html')


@login_required(login_url='login')
def add(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
           
            
            if radio =='taxable':
                print('tax section')
                
    
                
                inter=request.POST['inter']
                print(inter)
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                hsn=request.POST['hsn']
                status=request.POST.get('status')
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                tax=request.POST.get('radio')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                invacc=request.POST.get('invacc')
                stock=request.POST.get('openstock')
                rate=request.POST.get('inventoryaccntperunit')
                status_stock=request.POST.get('satus',0)
               
           
                
                
                ad_item=AddItem(type=type,
                                Name=name,
                                p_desc=p_desc,
                                s_desc=s_desc,
                                s_price=sel_price,
                                p_price=cost_price,
                                tax=tax,
                                hsn=hsn,
                                unit=unit,
                                sales=sel,
                                purchase=cost,
                                satus=status,
                                user=user,
                                creat=history,
                                interstate=inter,
                                intrastate=intra,
                                invacc=invacc,
                                stock=stock,
                                rate=rate,
                                status_stock=status_stock
                                
                                )
                ad_item.save()
                
            else:
                print('nontaxsection')
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                hsn=request.POST['hsn']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                tax=request.POST.get('radio')
                status=request.POST.get('status')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                stock = request.POST['openstock']
                invacc=request.POST.get('invacc')
                rate=request.POST.get('inventoryaccntperunit')
                status_stock=request.POST.get('satus',0)
               
               
                ad_item=AddItem(type=type,
                                Name=name,
                                hsn=hsn,
                                p_desc=p_desc,
                                s_desc=s_desc,
                                s_price=sel_price,
                                p_price=cost_price,
                                unit=unit,
                                sales=sel,
                                tax=tax,
                                purchase=cost,
                                satus = status,
                                user=user,
                                creat=history,
                                interstate='none',
                                intrastate='none',
                                invacc=invacc,
                                stock=stock,
                                rate=rate,
                                status_stock=status_stock
                              
                            
                               
                                )
                
                ad_item.save()
           
           
            return redirect("itemview")
    return render(request,'additem.html')


@login_required(login_url='login')
def edititem(request,id):
    item=AddItem.objects.all
    pedit=AddItem.objects.get(id=id)
    p=Purchase.objects.all()
    s=Sales.objects.all()
    u=Unit.objects.all()
    company=company_details.objects.get(user=request.user)
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))
    

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    return render(request,'edititem.html',{"account":account,"account_type":account_type,'e':pedit,'p':p,'s':s,'u':u,"accounts":accounts,"account_types":account_types,'item':item, "company":company})




@login_required(login_url='login')
def edit_db(request,id):
        if request.method=='POST':
            edit=AddItem.objects.get(id=id)
            edit.type=request.POST.get('type')
            edit.Name=request.POST['name']
            unit=request.POST.get('unit')
            edit.s_price=request.POST['sel_price']
            sel_acc=request.POST['sel_acc']
            edit.s_desc=request.POST['sel_desc']
            edit.p_price=request.POST['cost_price']
            cost_acc=request.POST['cost_acc']        
            edit.p_desc=request.POST['cost_desc']
            edit.hsn=request.POST['hsn']
            edit.stock=request.POST['openstock']
            edit.satus=request.POST.get('status')
            edit.invacc=request.POST.get('invacc')
            edit.rate=request.POST['inventoryaccntperunit']
            edit.status_stock=request.POST.get('satus')
            edit.unit=Unit.objects.get(id=unit)
            edit.sales=Sales.objects.get(id=sel_acc)
            edit.purchase=Purchase.objects.get(id=cost_acc)
            

            edit.save()
            
            return redirect('detail', id=edit.id)


        return render(request,'edititem.html')




@login_required(login_url='login')
def detail(request,id):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    items=AddItem.objects.all()
    product=AddItem.objects.get(id=id)
    history=History.objects.filter(p_id=product.id)
    comments = Comments_item.objects.filter(item=id).order_by('-id')
    print(product.id)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    context={
       "allproduct":items,
       "product":product,
       "history":history,
       'company':  company, 
       "comments":comments,
       'stock': stock,
    }
    
    return render(request,'demo.html',context)


@login_required(login_url='login')
def Action(request,id):
    user=request.user.id
    user=User.objects.get(id=user)
    viewitem=AddItem.objects.all()
    event=AddItem.objects.get(id=id)
    

    print(user)
    if request.method=='POST':
        action=request.POST['action']
        event.satus=action
        event.save()
        if action == 'active':
            History(user=user,message="Item marked as Active ",p=event).save()
        else:
            History(user=user,message="Item marked as inActive",p=event).save()
    return render(request,'item_view.html',{'view':viewitem})

@login_required(login_url='login')
def cleer(request,id):
    dl=AddItem.objects.get(id=id)
    dl.delete()
    return redirect('itemview')


@login_required(login_url='login')
def add_unit(request):
    if request.method == 'POST':
        unit_name = request.POST['unit_name']
        unit = Unit(unit=unit_name)  
        unit.save()  
        unit_id = unit.id  
        return JsonResponse({"unit_name": unit_name, "unit_id": unit_id})
    return render(request, "additem.html")



@login_required(login_url='login')
def add_sales(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem')
    return render(request,'additem.html')


@login_required(login_url='login')
def vendor(request):
    company=company_details.objects.get(user=request.user)
    return render(request,'create_vendor.html',{'company':company})


@login_required(login_url='login')
def add_vendor(request):
    if request.method=="POST":
        vendor_data=vendor_table()
        vendor_data.salutation=request.POST['salutation']
        vendor_data.first_name=request.POST['first_name']
        vendor_data.last_name=request.POST['last_name']
        vendor_data.company_name=request.POST['company_name']
        vendor_data.vendor_display_name=request.POST['v_display_name']
        vendor_data.vendor_email=request.POST['vendor_email']
        vendor_data.vendor_wphone=request.POST['w_phone']
        vendor_data.vendor_mphone=request.POST['m_phone']
        vendor_data.skype_number=request.POST['skype_number']
        vendor_data.designation=request.POST['designation']
        vendor_data.department=request.POST['department']
        vendor_data.website=request.POST['website']
        vendor_data.gst_treatment=request.POST['gst']

        x=request.POST['gst']
        if x=="Unregistered Business-not Registered under GST":
            vendor_data.pan_number=request.POST['pan_number']
            vendor_data.gst_number="null"
        else:
            vendor_data.gst_number=request.POST['gst_number']
            vendor_data.pan_number=request.POST['pan_number']

        vendor_data.source_supply=request.POST['source_supply']
        vendor_data.currency=request.POST['currency']
        vendor_data.opening_bal_type = request.POST['op_type']
        vendor_data.opening_bal=request.POST['opening_bal']
        vendor_data.payment_terms=request.POST['payment_terms']

        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vendor_data.user=udata
        vendor_data.battention=request.POST['battention']
        vendor_data.bcountry=request.POST['bcountry']
        vendor_data.baddress=request.POST['baddress']
        vendor_data.bcity=request.POST['bcity']
        vendor_data.bstate=request.POST['bstate']
        vendor_data.bzip=request.POST['bzip']
        vendor_data.bphone=request.POST['bphone']
        vendor_data.bfax=request.POST['bfax']

        vendor_data.sattention=request.POST['sattention']
        vendor_data.scountry=request.POST['scountry']
        vendor_data.saddress=request.POST['saddress']
        vendor_data.scity=request.POST['scity']
        vendor_data.sstate=request.POST['sstate']
        vendor_data.szip=request.POST['szip']
        vendor_data.sphone=request.POST['sphone']
        vendor_data.sfax=request.POST['sfax']
        vendor_data.status='Active'
        vendor_data.save()
# .......................................................adding to remaks table.....................
        vdata=vendor_table.objects.get(id=vendor_data.id)
        vendor=vdata
        rdata=remarks_table()
        rdata.remarks=request.POST['remark']
        rdata.user=udata
        rdata.vendor=vdata
        rdata.save()


#  ...........................adding multiple rows of table to model  ........................................................       
        salutation =request.POST.getlist('salutation[]')
        first_name =request.POST.getlist('first_name[]')
        last_name =request.POST.getlist('last_name[]')
        email =request.POST.getlist('email[]')
        work_phone =request.POST.getlist('wphone[]')
        mobile =request.POST.getlist('mobile[]')
        skype_number =request.POST.getlist('skype[]')
        designation =request.POST.getlist('designation[]')
        department =request.POST.getlist('department[]') 
        vdata=vendor_table.objects.get(id=vendor_data.id)
        vendor=vdata

        print(first_name)
        if first_name :
            if len(salutation)==len(first_name)==len(last_name)==len(email)==len(work_phone)==len(mobile)==len(skype_number)==len(designation)==len(department):
                mapped2=zip(salutation,first_name,last_name,email,work_phone,mobile,skype_number,designation,department)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = contact_person_table.objects.get_or_create(salutation=ele[0],first_name=ele[1],last_name=ele[2],email=ele[3],
                            work_phone=ele[4],mobile=ele[5],skype_number=ele[6],designation=ele[7],department=ele[8],user=udata,vendor=vendor)
            
        
                 
        return redirect('recurringhome')


        

def sample(request):
    print("hello")
    return redirect('base')

def view_vendor_list(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata)
    return render(request,'vendor_list.html',{'data':data,'company':company})

def view_vendor_details(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=vendor_table.objects.filter(user=udata)
    vdata2=vendor_table.objects.get(id=pk)
    mdata=mail_table.objects.filter(vendor=vdata2)
    ddata=doc_upload_table.objects.filter(user=udata,vendor=vdata2)
    cmt_data=comments_table.objects.filter(user=udata,vendor=vdata2)
    contact_persons = contact_person_table.objects.filter(user=udata,vendor=vdata2)

    fname = vdata2.first_name
    lname = vdata2.last_name
    fullname = fname + ' ' + lname
    v_email = vdata2.vendor_email
    name_and_id = fullname +' '+ str(vdata2.id) 
    id_and_name = str(vdata2.id) +' '+ fullname  

    print(fname)
    print(lname)
    print(fullname)
    print(v_email)
    print(name_and_id)

    expence = ExpenseE.objects.filter(user = udata,vendor_id = pk)
    recurring_expense = Expense.objects.filter(user = udata,vendor_id = pk)
    purchase_ordr = Purchase_Order.objects.filter(user = udata,vendor_name = name_and_id)
    paymnt_made = payment_made.objects.filter(user = udata,vendor_id = pk)
    purchase_bill = PurchaseBills.objects.filter(user = udata,vendor_name = fullname,vendor_email = v_email)
    recurring_bill = recurring_bills.objects.filter(user = udata,vendor_name = id_and_name)

    context = {
        'company':company,
        'vdata':vdata1,
        'vdata2':vdata2,
        'mdata':mdata,
        'ddata':ddata,
        'cmt_data':cmt_data,
        'contact_persons':contact_persons,
        'expence':expence,
        'recurring_expense':recurring_expense,
        'purchase_ordr':purchase_ordr,
        'paymnt_made':paymnt_made,
        'purchase_bill':purchase_bill,
        'recurring_bill':recurring_bill,

    }

    return render(request,'vendor_details.html',context)

def add_comment(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        Expense.objects.create(expense=expense, comment=comment_text)

    return redirect('show_recurring', expense_id=expense_id)

def sendmail(request):
    if request.method=='POST':
       subject=request.POST['subject']
       messag=request.POST['messag']
       sendto=request.POST['sendto']
       send_mail(subject,messag,settings.EMAIL_HOST_USER,
                 [sendto],fail_silently=False)
       return redirect('view_customr')



def edit_vendor(request,pk):
    company=company_details.objects.get(user=request.user)
    vdata=vendor_table.objects.get(id=pk)
    if remarks_table.objects.filter(vendor=vdata).exists() or contact_person_table.objects.filter(vendor=vdata).exists():
        if remarks_table.objects.filter(vendor=vdata).exists() and contact_person_table.objects.filter(vendor=vdata).exists():
            rdata=remarks_table.objects.get(vendor=vdata)
            pdata=contact_person_table.objects.filter(vendor=vdata)
            return render(request,'edit_vendor.html',{'vdata':vdata,'rdata':rdata,'pdata':pdata})
        else:
            if remarks_table.objects.filter(vendor=vdata).exists():
                rdata=remarks_table.objects.get(vendor=vdata)
                return render(request,'edit_vendor.html',{'vdata':vdata,'rdata':rdata})
            if contact_person_table.objects.filter(vendor=vdata).exists():
                pdata=contact_person_table.objects.filter(vendor=vdata)
                return render(request,'edit_vendor.html',{'vdata':vdata,'pdata':pdata})      
        
    else:
        return render(request,'edit_vendor.html',{'vdata':vdata,"company":company})


def edit_vendor_details(request,pk):
    if request.method=='POST':
        vdata=vendor_table.objects.get(id=pk)
        vdata.salutation=request.POST['salutation']
        vdata.first_name=request.POST['first_name']
        vdata.last_name=request.POST['last_name']
        vdata.company_name=request.POST['company_name']
        vdata.vendor_display_name=request.POST['v_display_name']
        vdata.vendor_email=request.POST['vendor_email']
        vdata.vendor_wphone=request.POST['w_phone']
        vdata.vendor_mphone=request.POST['m_phone']
        vdata.skype_number=request.POST['skype_number']
        vdata.designation=request.POST['designation']
        vdata.department=request.POST['department']
        vdata.website=request.POST['website']
        vdata.gst_treatment=request.POST['gst']
        if vdata.gst_treatment=="Unregistered Business-not Registered under GST":
            vdata.pan_number=request.POST['pan_number']
            vdata.gst_number="null"
        else:
            vdata.gst_number=request.POST['gst_number']
            vdata.pan_number=request.POST['pan_number']

        vdata.source_supply=request.POST['source_supply']
        vdata.currency=request.POST['currency']
        vdata.opening_bal=request.POST['opening_bal']
        vdata.payment_terms=request.POST['payment_terms']

        vdata.battention=request.POST['battention']
        vdata.bcountry=request.POST['bcountry']
        vdata.baddress=request.POST['baddress']
        vdata.bcity=request.POST['bcity']
        vdata.bstate=request.POST['bstate']
        vdata.bzip=request.POST['bzip']
        vdata.bphone=request.POST['bphone']
        vdata.bfax=request.POST['bfax']

        vdata.sattention=request.POST['sattention']
        vdata.scountry=request.POST['scountry']
        vdata.saddress=request.POST['saddress']
        vdata.scity=request.POST['scity']
        vdata.sstate=request.POST['sstate']
        vdata.szip=request.POST['szip']
        vdata.sphone=request.POST['sphone']
        vdata.sfax=request.POST['sfax']

        vdata.save()
             # .................................edit remarks_table ..........................
        vendor=vdata
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        if remarks_table.objects.filter(vendor=vdata).exists():
            rdata=remarks_table.objects.get(vendor=vdata)
            rdata.remarks=request.POST['remark']
            rdata.save()
        else:
            rdata=remarks_table()
            rdata.remarks=request.POST["remark"]
            rdata.vendor=vendor
            rdata.user=udata
            rdata.save()

            # .......................contact_person_table................ deleting existing entries and inserting  ...............

        pdata=contact_person_table.objects.filter(vendor=vdata)
        salutation =request.POST.getlist('salutation[]')
        first_name =request.POST.getlist('first_name[]')
        last_name =request.POST.getlist('last_name[]')
        email =request.POST.getlist('email[]')
        work_phone =request.POST.getlist('wphone[]')
        mobile =request.POST.getlist('mobile[]')
        skype_number =request.POST.getlist('skype[]')
        designation =request.POST.getlist('designation[]')
        department =request.POST.getlist('department[]') 

        vdata=vendor_table.objects.get(id=vdata.id)
        vendor=vdata
        user_id=request.user.id
        udata=User.objects.get(id=user_id)

        # .....  deleting existing rows......
        pdata.delete()
        if len(salutation)==len(first_name)==len(last_name)==len(email)==len(work_phone)==len(mobile)==len(skype_number)==len(designation)==len(department):
            mapped2=zip(salutation,first_name,last_name,email,work_phone,mobile,skype_number,designation,department)
            mapped2=list(mapped2)
            print(mapped2)
            for ele in mapped2:
                created = contact_person_table.objects.get_or_create(salutation=ele[0],first_name=ele[1],last_name=ele[2],email=ele[3],
                         work_phone=ele[4],mobile=ele[5],skype_number=ele[6],designation=ele[7],department=ele[8],user=udata,vendor=vendor)
        



        return redirect("view_vendor_list")

def upload_document(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata=vendor_table.objects.get(id=pk)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=doc_upload_table(user=udata,vendor=vdata,title=title,document=document)
        doc_data.save()
        return redirect("view_vendor_list")

def download_doc(request,pk):
    document=get_object_or_404(doc_upload_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def cancel_vendor(request):
    return redirect("vendor")

def delete_vendor(request,pk):
    if comments_table.objects.filter(vendor=pk).exists():
        user2=comments_table.objects.filter(vendor=pk)
        user2.delete()
    if mail_table.objects.filter(vendor=pk).exists():
        user3=mail_table.objects.filter(vendor=pk)
        user3.delete()
    if doc_upload_table.objects.filter(vendor=pk).exists():
        user4=doc_upload_table.objects.filter(vendor=pk)
        user4.delete()
    if contact_person_table.objects.filter(vendor=pk).exists():
        user5=contact_person_table.objects.filter(vendor=pk)
        user5.delete()
    if remarks_table.objects.filter(vendor=pk).exists():
        user6=remarks_table.objects.filter(vendor=pk)
        user6.delete()
    
    user1=vendor_table.objects.get(id=pk)
    user1.delete()
    return redirect("view_vendor_list")
    
    

# view functions for retainer invoice

@login_required(login_url='login')
def add_customer(request):
    sb=payment_terms.objects.all()
    return render(request,'customer.html',{'sb':sb})


@login_required(login_url='login')
def retainer_invoice(request):
    company=company_details.objects.get(user=request.user)
    invoices=RetainerInvoice.objects.all()
    context={'invoices':invoices,'company':company}
    return render(request,'retainer_invoice.html',context)


@login_required(login_url='login')
def add_invoice(request):
    company=company_details.objects.get(user_id=request.user)
    customer1=customer.objects.all()   
    context={'customer1':customer1,'company':company}    
    return render(request,'add_invoice.html',context)

@login_required(login_url='login')
def create_invoice_draft(request):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    
    if request.method=='POST':
        select=request.POST['select']
        customer_name=customer.objects.get(id=select)
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
    
        retainer_invoice=RetainerInvoice(
            customer_name=customer_name,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,total_amount=total_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions,user=user1,)
    
        retainer_invoice.save()
        

        description = request.POST.getlist('description[]')
        amount =request.POST.getlist('amount[]')
        if len(description)==len(amount):
            mapped = zip(description,amount)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.get_or_create(description=ele[0],amount=ele[1], retainer=retainer_invoice)
        else:
            pass

        return redirect('retainer_invoice')



            
        

         
@login_required(login_url='login')
def create_invoice_send(request):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    if request.method=='POST':
        select=request.POST['select']
        customer_name=customer.objects.get(id=select)
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
        retainer_invoice=RetainerInvoice(
        customer_name=customer_name,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,total_amount=total_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions,is_draft=False,user=user1)
        retainer_invoice.save()

        description = request.POST.getlist('description[]')
        amount = request.POST.getlist('amount[]')
        if len(description)==len(amount):
            mapped = zip(description,amount)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.get_or_create(description=ele[0],amount=ele[1], retainer=retainer_invoice)
        else:
            pass
        return redirect('invoice_view',pk=retainer_invoice.id)



@login_required(login_url='login')
def invoice_view(request,pk):
    company=company_details.objects.get(user_id=request.user)
    invoices=RetainerInvoice.objects.all()
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)

    context={'invoices':invoices,'invoice':invoice,'item':item,"company":company}
    return render(request,'invoice_view.html',context)


@login_required(login_url='login')
def retainer_template(request,pk):
    invoice=RetainerInvoice.objects.get(id=pk)
    return render(request,'template.html',{'invoice':invoice})

@login_required(login_url='login')
def retainer_edit_page(request,pk):
    company=company_details.objects.get(user_id=request.user)
    invoice=RetainerInvoice.objects.get(id=pk)
    customer1=customer.objects.all()
    items=Retaineritems.objects.filter(retainer=pk)
    context={'invoice':invoice, 'customer1':customer1,'items':items,'company':company}
    return render(request,'retainer_invoice_edit.html', context)



@login_required(login_url='login')
def retainer_update(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)

    if request.method=='POST':
        retainer_invoice=RetainerInvoice.objects.get(id=pk)
        select=request.POST['select']
        retainer_invoice.customer_name=customer.objects.get(id=select)
        retainer_invoice.retainer_invoice_number=request.POST['retainer-invoice-number']
        retainer_invoice.refrences=request.POST['references']
        retainer_invoice.retainer_invoice_date=request.POST['invoicedate']
        retainer_invoice.total_amount=request.POST.get('total')
        retainer_invoice.customer_notes=request.POST['customer_notes']
        retainer_invoice.terms_and_conditions=request.POST['terms']
    
        retainer_invoice.save()
        
        descriptions=request.POST.getlist('description[]')
        amounts=request.POST.getlist('amount[]')
        # if len(descriptions)==len(amounts):
        #     mapped = zip(descriptions,amounts)
        #     mapped=list(mapped)
        #     for ele in mapped:
        #         created=Retaineritems.objects.filter(retainer=retainer_invoice).update(description=ele[0])
        # else:
        #     pass
        for i in range(len(descriptions)):
            description=descriptions[i]
            amount=amounts[i]
            obj,created=Retaineritems.objects.update_or_create(retainer=retainer_invoice,description=description,defaults={'amount':amount})
            obj.save()





        return redirect('retainer_invoice')

@login_required(login_url='login')
def mail_send(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    retainer_invoice=RetainerInvoice.objects.get(id=pk)
    customer_email=retainer_invoice.customer_name.customerEmail
    
    if request.method=='POST':
        comments=request.POST.getlist('mailcomments')
        files=request.FILES.getlist('files')
        email_to=customer_email
        subject='Retainer Invoice'
        message1=f'Please keep the attached\nretainer invoice for future use.\n\ncomments:\n'
        message2='' 

        for comment in comments:
            message2 += comment + '\n'

        messages=message1+message2    


        email=EmailMessage(
            subject=subject,
            body=messages,
            to=[email_to]
        )
        
        for file in files:
            email.attach(file.name, file.read(), file.content_type)

        email.send() 
         
       
        retainer_invoice.is_draft=False
        retainer_invoice.is_sent=True
        retainer_invoice.save()  
        return redirect('retainer_invoice')
    
    return redirect('retainer_invoice')

@login_required(login_url='login')
def retaineritem_delete(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    item = get_object_or_404(Retaineritems, id=pk)
    item.delete()
    return redirect('retainer_edit_page' ,pk=item.retainer.id)
    
@login_required(login_url='login')
def retainer_delete(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    items=Retaineritems.objects.filter(retainer=pk)
    items.delete()
    retainer=RetainerInvoice.objects.get(id=pk)
    retainer.delete()
    return redirect('retainer_invoice')
        
            
def allestimates(request):
    user = request.user
    estimates = Estimates.objects.filter(user=user).order_by('-id')
    company = company_details.objects.get(user=user)
    context = {
        'estimates': estimates,
        'company': company,
    }
    # for i in estimates:
    #     print(i)

    return render(request, 'all_estimates.html', context)





def newestimate(request):
    user = request.user
    # print(user_id)
    
    company = company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    # item=AddItem.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    payments = payment_terms.objects.filter(user = request.user)
    estimates_count = Estimates.objects.count()
    next_count = estimates_count+1
    context = {'company': company,
               'items': items,
               'customers': customers,
               'count': next_count,
               'units':unit,
               'sales':sales,
               'purchase':purchase,
               'payments':payments,
               }

    return render(request,'new_estimate.html',context)


def itemdata_est(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    print(id)
    print(cust)
    item = AddItem.objects.get(Name=id, user=user)
    rate = item.p_price
    place = company.state
    gst = item.intrastate
    igst = item.interstate
    place_of_supply = customer.objects.get(
        customerName=cust, user=user).placeofsupply
    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'pos': place_of_supply, 'gst': gst, 'igst': igst})
    return redirect('/')


def createestimate(request):
    print('hi1')
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name=cust_name2.customerName
        customer_id=request.POST['customer_id']
        customer_id1=customer.objects.get(id=customer_id)
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        if x == y:

          item = request.POST.getlist('item[]')
          quantity = request.POST.getlist('quantity[]')
          rate = request.POST.getlist('rate[]')
          discount = request.POST.getlist('discount[]')
          tax = request.POST.getlist('tax[]')
          amount = request.POST.getlist('amount[]')
        
        else:
          itemm = request.POST.getlist('itemm[]')
          quantityy = request.POST.getlist('quantityy[]')
          ratee = request.POST.getlist('ratee[]')
          discountt = request.POST.getlist('discountt[]')
          taxx = request.POST.getlist('taxx[]')
          amountt = request.POST.getlist('amountt[]')
        

        cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        adjustment = request.POST['adjustment_charge']
        total = request.POST['total']
        tearms_conditions = request.POST['terms_conditions']
        attachment = request.FILES.get('file')
        status = 'Draft'
        

        estimate = Estimates(user=user,customer=customer_id1,customer_name=cust_name, estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        estimate.save()

        if x == y:

           if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
             mapped = zip(item, quantity, rate, discount, tax, amount)
             mapped = list(mapped)
             for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
        else:
            if len(itemm) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
             mapped = zip(itemm, quantityy, ratee, discountt, taxx, amountt )
             mapped = list(mapped)
             for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

    return redirect('newestimate')


def create_and_send_estimate(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    print("hello")
    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name=cust_name2.customerName
        customer_id=request.POST['customer_id']
        customer_id1=customer.objects.get(id=customer_id)
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        if x == y:

            item = request.POST.getlist('item[]')
            quantity1 = request.POST.getlist('quantity[]')
            quantity = [float(x) for x in quantity1]
            rate1 = request.POST.getlist('rate[]')
            rate = [float(x) for x in rate1]
            discount1 = request.POST.getlist('discount[]')
            discount = [float(x) for x in discount1]
            tax1 = request.POST.getlist('tax[]')
            tax = [float(x) for x in tax1]
            amount1 = request.POST.getlist('amount[]')
            amount = [float(x) for x in amount1]
        else:
            itemm = request.POST.getlist('itemm[]')
            quantityy1 = request.POST.getlist('quantityy[]')
            quantityy = [float(x) for x in quantityy1]
            ratee1 = request.POST.getlist('ratee[]')
            ratee = [float(x) for x in ratee1]
            discountt1 = request.POST.getlist('discountt[]')
            discountt = [float(x) for x in discountt1]
            taxx1 = request.POST.getlist('taxx[]')
            taxx = [float(x) for x in taxx1]
            amountt1 = request.POST.getlist('amountt[]')
            amountt = [float(x) for x in amountt1]
        

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST.get('igst'))
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['terms_conditions']
        attachment = request.FILES.get('file')
        status = 'Sent'
        tot_in_string = str(total)
        estimate = Estimates(user=user,customer=customer_id1,customer_name=cust_name, estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        estimate.save()

        if x == y:
            if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
              mapped = zip(item, quantity, rate, discount, tax, amount)
              mapped = list(mapped)
              for element in mapped:
                    created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
        
        else:
            if len(itemm) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
              mapped = zip(itemm, quantityy, ratee, discountt, taxx, amountt)
              mapped = list(mapped)
              for element in mapped:
                    created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

        cust_email = customer.objects.get(
            user=user, customerName=cust_name).customerEmail
        print(cust_email)
        subject = 'Estimate'
        message = 'Dear Customer,\n Your Estimate has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('newestimate')

def estimateslip(request, est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user)
    estimate = Estimates.objects.get(id=est_id)
    
    items = EstimateItems.objects.filter(estimate=estimate)
    est_comments=estimate_comments.objects.filter(estimate=estimate.id,user=user)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
        'est_comments':est_comments,
    }
    return render(request, 'estimate_slip.html', context)




def editestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    comp=company.state
    customers = customer.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    estimate = Estimates.objects.get(id=est_id)
    cust=estimate.customer.placeofsupply
    cust_id=estimate.customer.id
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()

    est_items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'estimate': estimate,
        'customers': customers,
        'items': items,
        'est_items': est_items,
        'comp':comp,
        'cust':cust,
        'cust_id':cust_id,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
    }
    return render(request,'edit_estimate.html', context)

def updateestimate(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        estimate = Estimates.objects.get(id=pk)
        estimate.user = user
        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name=cust_name2.customerName
        estimate.customer_name=cust_name
        custr=request.POST['customer_id']
        customer_id=customer.objects.get(id=custr)
        estimate.customer=customer_id
        estimate.estimate_no = request.POST['estimate_number']
        estimate.reference = request.POST['reference']
        estimate.estimate_date = request.POST['estimate_date']
        estimate.expiry_date = request.POST['expiry_date']

        estimate.customer_notes = request.POST['customer_note']
        estimate.sub_total = float(request.POST['subtotal'])
        estimate.igst = float(request.POST['igst'])
        estimate.sgst = float(request.POST['sgst'])
        estimate.cgst = float(request.POST['cgst'])
        estimate.tax_amount = float(request.POST['total_taxamount'])
        estimate.shipping_charge = float(request.POST['shipping_charge'])
        estimate.adjustment = float(request.POST['adjustment_charge'])
        estimate.total = float(request.POST['total'])
        estimate.terms_conditions = request.POST['terms_conditions']
        estimate.status = 'Draft'

        old=estimate.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            estimate.attachment = old
        else:
            estimate.attachment = new

        estimate.save()

        if x == y:
          item = request.POST.getlist('item[]')
          quantity1 = request.POST.getlist('quantity[]')
          quantity = [float(x) for x in quantity1]
          rate1 = request.POST.getlist('rate[]')
          rate = [float(x) for x in rate1]
          discount1 = request.POST.getlist('discount[]')
          discount = [float(x) for x in discount1]
          tax1 = request.POST.getlist('tax[]')
          tax = [float(x) for x in tax1]
          amount1 = request.POST.getlist('amount[]')
          amount = [float(x) for x in amount1]
        else:
          itemm = request.POST.getlist('itemm[]')
          quantityy1 = request.POST.getlist('quantityy[]')
          quantityy = [float(x) for x in quantityy1]
          ratee1 = request.POST.getlist('ratee[]')
          ratee = [float(x) for x in ratee1]
          discountt1 = request.POST.getlist('discountt[]')
          discountt = [float(x) for x in discountt1]
          taxx1 = request.POST.getlist('taxx[]')
          taxx = [float(x) for x in taxx1]
          amountt1 = request.POST.getlist('amountt[]')
          amountt = [float(x) for x in amountt1]

        objects_to_delete = EstimateItems.objects.filter(estimate_id=estimate.id)
        objects_to_delete.delete()

        if x == y:
           if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
              mapped = zip(item, quantity, rate, discount, tax, amount)
              mapped = list(mapped)
              for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
        else:
           if len(itemm) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
              mapped = zip(itemm, quantityy, ratee, discountt, taxx, amountt)
              mapped = list(mapped)
              for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

    return redirect('allestimates')

def converttoinvoice(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    cust = customer.objects.get(customerName=estimate.customer_name,user=user)
    invoice_count = invoice.objects.count()
    next_no = invoice_count+1 
    inv = invoice(customer=cust,invoice_no=next_no,terms='null',order_no=estimate.estimate_no,
                      inv_date=estimate.estimate_date,due_date=estimate.expiry_date,igst=estimate.igst,cgst=estimate.cgst,
                      sgst=estimate.sgst,t_tax=estimate.tax_amount,subtotal=estimate.sub_total,grandtotal=estimate.total,
                      cxnote=estimate.customer_notes,file=estimate.attachment,terms_condition=estimate.terms_conditions,
                      status=estimate.status)
    inv.save()
    inv = invoice.objects.get(invoice_no=next_no,customer=cust)
    for item in items:
        items = invoice_item(product=item.item_name,quantity=item.quantity,hsn='null',tax=item.tax_percentage,
                             total=item.amount,desc=item.discount,rate=item.rate,inv=inv)
        items.save()
    return redirect('allestimates')

class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'newmail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})



def add_customer_for_estimate(request):
    sb=payment_terms.objects.all()
    return render(request,'customer_est.html',{'sb':sb})
    
def entr_custmr_for_estimate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST['email']            
            wphone=request.POST['fname']
            mobile=request.POST.get('lname')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("newestimate")
        return redirect("newestimate")
    
def payment_term_for_estimate(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_for_estimate")

    
@login_required(login_url='login')
def payment_term(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer")

@login_required(login_url='login')
def invoiceview(request):
    company=company_details.objects.get(user=request.user)
    invoicev=invoice.objects.all()
    
    if not payment_terms.objects.filter(Terms='net 15').exists(): 
       payment_terms(Terms='net 15',Days=15).save()
    if not payment_terms.objects.filter(Terms='due end of month').exists():
        payment_terms(Terms='due end of month',Days=60).save()
    elif not  payment_terms.objects.filter(Terms='net 30').exists():
        payment_terms(Terms='net 30',Days=30).save() 
    
    
    context={
        'invoice':invoicev,
        'company':company
        
    }
    return render(request,'invoiceview.html',context)

@login_required(login_url='login')
def detailedview(request,id):
    inv_dat=invoice.objects.all()
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'comp':company,
        'invoice':inv_master,
        "company":company,
        
                    }
    return render(request,'invoice_det.html',context)



@login_required(login_url='login')

def dele(request,pk):
    d=invoice.objects.get(id=pk)
    d.delete()
    return redirect('invoiceview')

@login_required(login_url='login')

def addinvoice(request):
    c=customer.objects.all()
    p=AddItem.objects.all()
    i=invoice.objects.all()
    pay=payment.objects.all()
    if not payment.objects.filter(term='net 15').exists(): 
       payment(term='net 15',days=15).save()
    if not payment.objects.filter(term='due end of month').exists():
        payment(term='due end of month',days=60).save()
    elif not  payment.objects.filter(term='net 30').exists():
        payment(term='net 30',days=30).save() 
    


    
            
            
            
            
    context={
        'c':c,
        'p':p,
        'i':i,
        'pay':pay,
        
    }
       
    return render(request,'createinvoice.html',context)


@login_required(login_url='login')

def add_prod(request):
    company=company_details.objects.get(user=request.user)
    c=customer.objects.all()
    p=AddItem.objects.all()
    i=invoice.objects.all()
    pay=payment_terms.objects.all()
    if not payment_terms.objects.filter(Terms='net 15').exists(): 
       payment_terms(Terms='net 15',Days=15).save()
    if not payment_terms.objects.filter(Terms='due end of month').exists():
        payment_terms(Terms='due end of month',Days=60).save()
    elif not  payment_terms.objects.filter(Terms='net 30').exists():
        payment_terms(Terms='net 30',Days=30).save() 
    
    
   
    if request.user.is_authenticated:
        if request.method=='POST':
            c=request.POST['cx_name']
            cus=customer.objects.get(customerName=c) 
            print(cus.id)  
            custo=cus.id
            invoice_no=request.POST['inv_no']
            terms=request.POST['term']
            term=payment_terms.objects.get(id=terms)
            order_no=request.POST['ord_no']
            inv_date=request.POST['inv_date']
            due_date=request.POST['due_date']
        
            
            cxnote=request.POST['customer_note']
            subtotal=request.POST['subtotal']
            igst=request.POST['igst']
            cgst=request.POST['cgst']
            sgst=request.POST['sgst']
            totaltax=request.POST['totaltax']
            t_total=request.POST['t_total']
            if request.FILES.get('file') is not None:
                file=request.FILES['file']
            else:
                file="/static/images/alt.jpg"
            tc=request.POST['ter_cond']

            status=request.POST['sd']
            if status=='draft':
                print(status)   
            else:
                print(status)  
        
            product=request.POST.getlist('item[]')
            hsn=request.POST.getlist('hsn[]')
            quantity=request.POST.getlist('quantity[]')
            rate=request.POST.getlist('rate[]')
            desc=request.POST.getlist('desc[]')
            tax=request.POST.getlist('tax[]')
            total=request.POST.getlist('amount[]')
            term=payment_terms.objects.get(id=term.id)

            inv=invoice(customer_id=custo,invoice_no=invoice_no,terms=term,order_no=order_no,inv_date=inv_date,due_date=due_date,
                        cxnote=cxnote,subtotal=subtotal,igst=igst,cgst=cgst,sgst=sgst,t_tax=totaltax,
                        grandtotal=t_total,status=status,terms_condition=tc,file=file)
            inv.save()
            inv_id=invoice.objects.get(id=inv.id)
            if len(product)==len(hsn)==len(quantity)==len(desc)==len(tax)==len(total)==len(rate):

                mapped = zip(product,hsn,quantity,desc,tax,total,rate)
                mapped = list(mapped)
                for element in mapped:
                    created = invoice_item.objects.get_or_create(inv=inv_id,product=element[0],hsn=element[1],
                                        quantity=element[2],desc=element[3],tax=element[4],total=element[5],rate=element[6])
                    
                return redirect('invoiceview')
    context={
            'c':c,
            'p':p,
            'i':i,
            'pay':pay,
            'company':company,
    }       
    return render(request,'createinvoice.html',context)


@login_required(login_url='login')

def add_payment(request):
    if request.method=='POST':
            terms=request.POST.get()
    return redirect('add_prod')


@login_required(login_url='login')

def add_cx(request):
    if request.user.is_authenticated:
        if request.method=='POST':
                user=request.user.id
                user=User.objects.get(id=user)
                print(user)
                name=request.POST.get('name')
                email=request.POST.get('email')
                pos=request.POST.get('position')
                state=request.POST.get('state')
                com_name=request.POST.get('company')
                customer(customerName=name,customerEmail=email,placeofsupply=pos,state=state,companyName=com_name,user_id=user.id).save()
        return redirect('add_prod')




@login_required(login_url='login')

def edited_prod(request,id):
    print(id)
    company = company_details.objects.get(user = request.user)
    c = customer.objects.all()
    p = AddItem.objects.all()
    invoiceitem = invoice_item.objects.filter(inv_id=id)
    invoic = invoice.objects.get(id=id)
    pay=payment_terms.objects.all()
  
    if request.method == 'POST':
        u=request.user.id
        c=request.POST['cx_name']
        
        cust=customer.objects.get(customerName=c) 
        invoic.customer=cust
        term=request.POST['term']
        
        
        invoic.terms = payment_terms.objects.get(id=term)
        invoic.inv_date = request.POST['inv_date']
        invoic.due_date = request.POST['due_date']
        invoic.cxnote = request.POST['customer_note']
        invoic.subtotal = request.POST['subtotal']
        invoic.igst = request.POST['igst']
        invoic.cgst = request.POST['cgst']
        invoic.sgst = request.POST['sgst']
        invoic.t_tax = request.POST['totaltax']
        invoic.grandtotal = request.POST['t_total']

        if request.FILES.get('file') is not None:
            invoic.file = request.FILES['file']
        else:
            invoic.file = "/static/images/alt.jpg"

            invoic.terms_condition = request.POST.get('ter_cond')
        
        status=request.POST['sd']
        if status=='draft':
            invoic.status=status      
        else:
            invoic.status=status   
         
        invoic.save()
        
        print("/////////////////////////////////////////////////////////")
        product=request.POST.getlist('item[]')
        hsn=request.POST.getlist('hsn[]')
        quantity=request.POST.getlist('quantity[]')
        rate=request.POST.getlist('rate[]')
        desc=request.POST.getlist('desc[]')
        tax=request.POST.getlist('tax[]')
        total=request.POST.getlist('amount[]')
        obj_dele=invoice_item.objects.filter(inv_id=invoic.id)
        obj_dele.delete()
       
        if len(product)==len(hsn)==len(quantity)==len(desc)==len(tax)==len(total)==len(rate):

            mapped = zip(product,hsn,quantity,desc,tax,total,rate)
            mapped = list(mapped)
            for element in mapped:
                created = invoice_item.objects.get_or_create(inv=invoic,product=element[0],hsn=element[1],
                                    quantity=element[2],desc=element[3],tax=element[4],total=element[5],rate=element[6])
                
            return redirect('detailedview',id)
                    
    context = {
            'c': c,
            'p': p,
            'inv': invoiceitem,
            'i': invoic,
            'pay':pay,
            "company":company,
        }             
        
    return render(request, 'invoiceedit.html', context)





@login_required(login_url='login')

def edited(request,id):
    c=customer.objects.all()
    p=AddItem.objects.all()
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    inv=invoice.objects.get(id=id)
    context={
        'c':c,
        'p':p,
        'inv':invoiceitem,
        'inv':inv,
        
    }
    
    return render(request,'editinvoice.html')



@login_required(login_url='login')

def itemdata(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
   
        
    item = AddItem.objects.get(Name=id)
    cus=customer.objects.get(id=cust)
    rate = item.s_price
    place=company.state
    gst = item.intrastate
    igst = item.interstate
    desc=item.s_desc
    print(place)
    mail=cus.customerEmail
    
    place_of_supply = customer.objects.get(id=cust).placeofsupply
    print(place_of_supply)
    return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst})
    return redirect('/')
    

def deleteestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    items.delete()
    estimate.delete()
    return redirect('allestimates')
    

@login_required(login_url='login')
def additem_page_est(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_est.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_est(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("newestimate")
    return render(request,'additem_est.html')

@login_required(login_url='login')
def add_unit_est(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_est')
    return redirect("additem_est")
    
#-------------new view functions to add

@login_required(login_url='login')
def add_sales_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_est')
    return redirect("additem_est")

@login_required(login_url='login')
def add_account_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_est")
        
    return redirect("additem_est")
    
def customerdata(request):
    customer_id = request.GET.get('id')
    print(customer_id)
    cust = customer.objects.get(id=customer_id)
    data7 = {'email': cust.customerEmail}
    
    print(data7)
    return JsonResponse(data7)


def add_customer_for_invoice(request):
    pt=payment_terms.objects.all()
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("add_prod")
        return render(request,"createinvoice.html",)
        
        
def payment_term_for_invoice(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_prod")
        
        
def addprice(request):
    company=company_details.objects.get(user=request.user)
    add=AddItem.objects.all()
    return render(request,'addprice_list.html',{'add':add,'company':company})
    
    
def addpl(request):
    print('hi')
    if request.method == "POST":
        

        
        name = request.POST.get('name')
        print(name)
        types = request.POST.get('type')
        print(types)
        taxes=request.POST.get('rate')
        desc = request.POST.get('desc')
        cur = request.POST.get('currency')
        print(cur)
        mark = request.POST.get('mark')
        print(mark)
        perc = request.POST.get('per')
        print(perc)
        rounds = request.POST.get('round')
        print(rounds)
        u = request.user.id
        user = User.objects.get(id=u)
            
        ad_item = Pricelist(
                name=name,
                types=types,
                tax=taxes,
                currency=cur,
                description=desc,
                mark=mark,
                percentage=perc,
                roundoff=rounds,
                user=user,
            )
            
        ad_item.save()
        item_name = request.POST.getlist('iname[]') 
        print(item_name)
        price = request.POST.getlist('iprice[]')
        rate = request.POST.getlist('custom[]') 
        if len(item_name) == len(price) == len(rate):
            mapped2 = zip(item_name, price, rate)
            mapped2 = list(mapped2)
         
            for ele in mapped2:
                created = Sample_table.objects.get_or_create(item_name=ele[0], price=ele[1], cust_rate=ele[2], pl=ad_item)

        return redirect("viewpricelist")
    else:
        # Handle the case when the request method is not POST
        return render(request, 'addprice_list.html')
    # return render(request, 'addprice_list.html')
def createpl(request):
    return render(request,'addprice_list.html')
def active_status(request, id):
    user = request.user.id
    user = User.objects.get(id=user)
    viewitem = Pricelist.objects.all()
    event = Pricelist.objects.get(id=id)
    
    if request.method == 'POST':
        action = request.POST['action']
        event.status = action  # Updated field name to 'status'
        event.save()
    
    return render(request, 'view_price_list.html', {'view': viewitem})

def viewpricelist(request):
    company = company_details.objects.get(user = request.user)
    view=Pricelist.objects.all()                                                                                                                                                                                                                                                                                                                        
    return render(request,'view_price_list.html',{'view':view,'company':company})
    
def viewlist(request,id):
    company = company_details.objects.get(user = request.user)
    items=Pricelist.objects.all()
    product=Pricelist.objects.get(id=id)
    print(product.id)
    
    
    context={
       "allproduct":items,
       "product":product,
       'company':company,
      
    }
    
    return render(request,'list.html',context)

def editlist(request,id):
    company = company_details.objects.get(user = request.user)
    editpl=Pricelist.objects.get(id=id)
    sam=Sample_table.objects.filter(pl=id)
    return render(request,'edit_pricelist.html',{'editpl':editpl,'sam':sam,"company":company})
    
def editpage(request,id):
    if request.method=='POST':
        edit=Pricelist.objects.get(id=id)
        edit.name=request.POST['name']
        edit.description=request.POST['desc']
        edit.mark=request.POST['mark']
        edit.percentage=request.POST['per']
        print(request.POST['per'])
        edit.tax=request.POST['types']
        
        edit.roundoff=request.POST['round']
        print(edit.roundoff)
        item_name = request.POST.getlist('iname[]') 
        print(item_name)
        price = request.POST.getlist('iprice[]')
        rate = request.POST.getlist('custom[]') 
        sam=Sample_table.objects.filter(pl=id).delete()

        if len(item_name) == len(price) == len(rate):
            mapped2 = zip(item_name, price, rate)
            mapped2 = list(mapped2)
         
            for ele in mapped2:
                created = Sample_table.objects.get_or_create(item_name=ele[0], price=ele[1], cust_rate=ele[2],pl=edit)
        edit.save()

        return redirect('viewpricelist')
def delete_item(request,id):
    dl=Pricelist.objects.get(id=id)
    dl.delete()
    return redirect('viewpricelist')


def banking_home(request):
    company = company_details.objects.get(user = request.user)
    viewitem=banking.objects.filter(user=request.user)
    return render(request,'banking.html',{'view':viewitem,"company":company})       
    
def create_banking(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'create_banking.html',{"bank":banks,"company":company})    

def save_banking(request):
    if request.method == "POST":
        a=banking()
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.opening_blnc_type = request.POST.get('opening_blnc_type',None)
        a.user=request.user
        a.opening_bal = request.POST.get('balance',None)
        a.save()
        return redirect("banking_home")
    return redirect("create_banking")

def view_bank(request,id):
    viewitem=banking.objects.filter(user=request.user)
    bnk=banking.objects.get(id=id,user=request.user)
    company = company_details.objects.get(user = request.user)
    context={
        'view':viewitem,
        'bnk':bnk,
        "company":company
    }
    return render(request,"view_bank.html",context)

def banking_edit(request,id):
    bnk=banking.objects.get(id=id,user=request.user)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    company = company_details.objects.get(user = request.user)
    context={
        'bnk':bnk,
        "bank":banks,
        "company":company
    }
    return render(request,"edit_banking.html",context)

def save_edit_bnk(request,id):
    if request.method == "POST":
        a=banking.objects.get(id=id,user=request.user)
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.opening_bal = request.POST.get('balance',None)
        a.opening_blnc_type = request.POST.get('opening_blnc_type',None)
        a.save()
        return redirect("banking_home")
    return redirect("create_banking")

def save_bank(request):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect("create_banking")
    return redirect("create_banking")
def save_banking_edit(request,id):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect("banking_edit", id)
    return redirect("banking_edit", id)
    
def basenav(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    context = {
                'company' : company
            }
    return render(request,'base.html',context)

def banking_delete(request,id):
    bnk=banking.objects.get(id=id)
    bnk.delete()
    return redirect("banking_home")
    
@login_required(login_url='login')
def recurringhome(request):
    company = company_details.objects.get(user = request.user)
    selected_vendor_id = request.GET.get('vendor')
    vendors = vendor_table.objects.filter(user=request.user)
    selected_vendor = vendor_table.objects.filter(id=selected_vendor_id).first()
    gst_number = selected_vendor.gst_number if selected_vendor else ''
    return render(request, 'recurring_home.html', {
        'vendors': vendors,
        'selected_vendor_id': selected_vendor_id,
        'gst_number': gst_number,
        'company':company,
    })




from django.shortcuts import get_object_or_404
from .models import Expense, vendor_table

def add_expense(request):
    user = request.user
    if request.method == 'POST':
        # Retrieve form data
        profile_name = request.POST['profile_name']
        repeat_every = request.POST['repeat_every']
        start_date = request.POST['start_date']
        expense_account = request.POST.get('expense_account', '')
        expense_type = request.POST['expense_type']
        goods_label = request.POST.get('goods_label')
        amount = request.POST['amount']
        currency = request.POST['currency']
        paidthrough = request.POST['paidthrough']
        vendor_id = request.POST['vendor']
        vendor = get_object_or_404(vendor_table, pk=vendor_id)
        gst = request.POST['gst']
        destination = request.POST['destination']
        tax = request.POST['tax']
        notes = request.POST['notes']
        customer_id = request.POST['customername']
        customer_obj = get_object_or_404(customer, pk=customer_id)

        # Handle the ends_on field
        ends_on = request.POST.get('ends_on')
        never_expire = request.POST.get('never_expire') == 'on'

        if never_expire:
            ends_on = "Never expire"

        # Create and save the Expense instance
        expense = Expense(
            user = user,
            profile_name=profile_name,
            repeat_every=repeat_every,
            start_date=start_date,
            ends_on=ends_on,
            expense_account=expense_account,
            expense_type=expense_type,
            goods_label=goods_label,
            amount=amount,
            currency=currency,
            paidthrough=paidthrough,
            vendor=vendor,
            gst=gst,
            destination=destination,
            tax=tax,
            notes=notes,
            customername=customer_obj.customerName,
            activation_tag="active"  # Set the activation_tag to "active"
        )
        expense.save()

        return redirect('recurringbase')
    else:
        vendors = vendor_table.objects.all()
        return render(request, 'add_expense.html', {'vendors': vendors})


@login_required(login_url='login')
def recurringbase(request):
    company=company_details.objects.get(user=request.user)
    expenses = Expense.objects.all()
    return render(request, 'recurring_base.html',{'expenses': expenses,'company':company})

def show_recurring(request, expense_id):
    company=company_details.objects.get(user=request.user)
    expense = get_object_or_404(Expense, id=expense_id)
    expenses = Expense.objects.all()

    search_query = request.GET.get('search_query')
    search_date = request.GET.get('search_date')

    if search_query:
        expenses = expenses.filter(
            Q(profile_name_icontains=search_query) | Q(customername_icontains=search_query)
        )
    
    if search_date:
        expenses = expenses.filter(start_date=search_date)

    if request.method == 'POST':
        comments = request.POST.get('enter_comment_here', '')
        Comment.objects.create(profile_name=expense.profile_name, expense=expense, comment=comments)

    comments = Comment.objects.filter(profile_name=expense.profile_name, expense=expense)

    return render(request, 'show_recurring.html', {'company':company,'expense': expense, 'expenses': expenses, 'comments': comments})




def expense_details(request, pk):
    user = request.user
    expense = ExpenseE.objects.filter(user=user)
    company = company_details.objects.get(user = request.user)
    expense_account=ExpenseE.objects.get(id=pk)
    context = {
        'expenses': expense,
        'expense': expense_account,
        'company':company
    }
    return render(request, 'expenseview.html', context)
    
def edit_expense(request, expense_id):
    company=company_details.objects.get(user=request.user)
    expense = get_object_or_404(Expense, id=expense_id)
    vendors = vendor_table.objects.all()
    customers = customer.objects.all()  # Fetch all customers

    if request.method == 'POST':
        expense.profile_name = request.POST.get('profile_name')
        expense.repeat_every = request.POST.get('repeat_every')
        expense.start_date = request.POST.get('start_date')
        expense.ends_on = request.POST.get('ends_on')
        expense.expense_account = request.POST.get('expense_account')
        expense.expense_type = request.POST.get('expense_type')
        expense.amount = request.POST.get('amount')
        expense.currency = request.POST.get('currency')
        expense.paidthrough = request.POST.get('paidthrough')
        expense.vendor_id = request.POST.get('vendor')
        expense.goods_label = request.POST.get('goods_label')
        expense.gst = request.POST.get('gst')
        expense.destination = request.POST.get('destination')
        expense.tax = request.POST.get('tax')
        expense.notes = request.POST.get('notes')
        customer_id = request.POST.get('customername')  # Get the customer ID from POST data
        customer_obj = get_object_or_404(customer, pk=customer_id)  # Fetch the customer object
        expense.customername = customer_obj.customerName  # Set the customer name in the expense object

        expense.save()
        return redirect('recurringbase')

    else:
        return render(request, 'edit_expense.html', {'expense': expense,'company':company, 'vendors': vendors, 'customers': customers})   
  
        
@login_required(login_url='login')
def newexp(request):
    return render(request,'create_expense.html')

def save_data(request):
    if request.method == 'POST':
        account_type = request.POST.get('accountType')
        account_name = request.POST.get('accountName')
        account_code = request.POST.get('accountCode')
        description = request.POST.get('description')

        account = Account(accountType=account_type, accountName=account_name, accountCode=account_code, description=description)
        account.save()

        return redirect('recurringhome')

    return render(request, 'recurring_home.html')
  
    
from django.http import JsonResponse
from .models import Account

def get_account_names(request):
    account_names = Account.objects.values_list('accountName', flat=True)
    return JsonResponse(list(account_names), safe=False)
    
@login_required(login_url='login')
def profileshow(request,expense_id):
    expenses = Expense.objects.all()
    expense = get_object_or_404(Expense, id=expense_id)

    return render(request, 'show_recurring.html', {'expenses': expenses,'expense':expense})    
    
def entr_custmr(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select = request.POST.get('pterms')
        try:
            pterms = payment_terms.objects.get(id=select)
        except payment_terms.DoesNotExist:
            pterms = None

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("recurringhome")
        return render(request,'recurring_home.html')    
        
from django.http import JsonResponse

def get_customer_names(request):
    customers = customer.objects.all()
    customer_names = [{'id': c.id, 'name': c.customerName} for c in customers]
    return JsonResponse(customer_names, safe=False)  
    
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('recurringbase')


def get_profile_details(request, profile_id):
    expense = get_object_or_404(Expense, id=profile_id)
    vendor = expense.vendor 
    data = {
        'id': expense.id,
        'profile_name': expense.profile_name,
        'repeat_every': expense.repeat_every,
        'start_date': expense.start_date,
        'ends_on': expense.ends_on,
        'expense_account': expense.expense_account,
        'expense_type': expense.expense_type,
        'amount': expense.amount,
        'paidthrough': expense.paidthrough,
        'vendor': vendor.vendor_display_name,  
        'gst': expense.gst,
        'destination': expense.destination,
        'tax': expense.tax,
        'notes': expense.notes,
        'customername': expense.customername,
        'activation_tag': expense.activation_tag
    }
    return JsonResponse(data)
    
    
    
@login_required(login_url='login')
def view_sales_order(request):
    sales=SalesOrder.objects.all()
    user = request.user
    company = company_details.objects.get(user=user)
    return render(request,'view_sales_order.html',{"sale":sales,"company":company})      

    
@login_required(login_url='login')
def create_sales_order(request):
    user = request.user
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    company = company_details.objects.get(user=user)
    cust=customer.objects.all()
    pay=payment_terms.objects.all()
    itm=AddItem.objects.all()
    purchase=Purchase.objects.all()
    
    context={
        "c":cust,
        "pay":pay,
        "itm":itm,
        "company":company,
        "unit":unit, 
        "sales":sales,
        "purchase":purchase,

    }
    return render(request,'create_sales_order.html',context)

    
@login_required(login_url='login')
def add_customer_for_sorder(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            gstin=request.POST.get('gstin')
            panno=request.POST.get('panno')


            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

           
          
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
          
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                               Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,
                                  user=u ,GSTIN=gstin,pan_no=panno)
            ctmr.save()
 
            
            return HttpResponse({"message": "success"})

    
@login_required(login_url='login')        
def payment_term_for_sorder(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("create_sales_order")
        
        




    
@login_required(login_url='login')
def add_sales_order(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            c=request.POST['cx_name']
            cus=customer.objects.get(id=c)   
            custo=cus.id
            sales_no=request.POST['sale_no']
            terms=request.POST['term']
            term=payment_terms.objects.get(id=terms)
            reference=request.POST['ord_no']
            sa_date=request.POST['sa_date']
            sh_date=request.POST['sh_date']
            sos=request.POST['srcofsupply']

            sh_charge=request.POST['shipping_charge']
            
            cxnote=request.POST['customer_note']
            subtotal=request.POST['subtotal']
            igst=request.POST['igst']
            cgst=request.POST['cgst']
            sgst=request.POST['sgst']
            totaltax=request.POST['totaltax']
            t_total=request.POST['t_total']
            if request.FILES.get('file') is not None:
                file=request.FILES['file']
            else:
                file="/static/images/alt.jpg"
            tc=request.POST['ter_cond']

            status="draft"
             
        
            product=request.POST.getlist('item[]')
            hsn=request.POST.getlist('hsn[]')
            quantity=request.POST.getlist('quantity[]')
            rate=request.POST.getlist('rate[]')
            desc=request.POST.getlist('desc[]')
            tax=request.POST.getlist('tax[]')
            total=request.POST.getlist('amount[]')
            term=payment_terms.objects.get(id=term.id)
            
            sales=SalesOrder(customer_id=custo,sales_no=sales_no,terms=term,reference=reference, sales_date=sa_date,ship_date=sh_date,
                        cxnote=cxnote,subtotal=subtotal,igst=igst,cgst=cgst,sgst=sgst,t_tax=totaltax,
                        grandtotal=t_total,status=status,terms_condition=tc,file=file,sos=sos,sh_charge=sh_charge)
            sales.save()
            sale_id=SalesOrder.objects.get(id=sales.id)
          
            if len(product)==len(quantity)==len(tax)==len(total)==len(rate):
            
                mapped = zip(product,quantity,tax,total,rate,desc)
                mapped = list(mapped)
                
                for element in mapped:

                    created =sales_item(sale=sale_id,product=element[0],
                                        quantity=element[1],tax=element[2],total=element[3],rate=element[4],desc=element[5])
                    created.save()
                    print(created)    
                
            return redirect('view_sales_order')          
    
@login_required(login_url='login')
def sales_order_det(request,id):
    sales=SalesOrder.objects.get(id=id)
    saleitem=sales_item.objects.filter(sale_id=id)
    sale_order=SalesOrder.objects.all()
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'sale':sales,
        'saleitem':saleitem,
        'sale_order':sale_order,
        'company':company,
        
        
                    }
    
    return render(request,'sales_order_det.html',context)


    
@login_required(login_url='login')
def delet_sales(request,id):
    d=SalesOrder.objects.get(id=id)
    d.delete()
    return redirect('view_sales_order')
    
    
@login_required(login_url='login')
def edit_sales_order(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    c = customer.objects.all()
    itm = AddItem.objects.all()
    salesitem = sales_item.objects.filter(sale_id=id)
    sales = SalesOrder.objects.get(id=id)
    pay=payment_terms.objects.all()
    

    if request.method == 'POST':
        u=request.user.id
        c=request.POST['cx_name']
        
        cust=customer.objects.get(id=c) 
        sales.customer=cust
        term=request.POST['term']
        
        
        sales.terms = payment_terms.objects.get(id=term)
        sales.sales_date = request.POST['sa_date']
        sales.shipdate=request.POST['sh_date']
        sales.cxnote = request.POST['customer_note']
        sales.igst = request.POST['igst']
        sales.cgst = request.POST['cgst']
        sales.sgst = request.POST['sgst']
        sales.t_tax = request.POST['totaltax']
        sales.grandtotal = request.POST['t_total']
        sales.sos=request.POST['srcofsupply']
        sales.sh_charge=request.POST['shipping_charge']
        if request.FILES.get('file') is not None:
            sales.file = request.FILES['file']
        else:
            sales.file = "/static/images/alt.jpg"

            sales.terms_condition = request.POST.get('ter_cond')
        
       
        
        sales.save()
        
        product=request.POST.getlist('item[]')
        quantity=request.POST.getlist('quantity[]')
        rate=request.POST.getlist('rate[]')
        tax=request.POST.getlist('tax[]')
        total=request.POST.getlist('amount[]')
        desc=request.POST.getlist('desc[]')
        obj_dele=sales_item.objects.filter(sale_id=sales.id)
        obj_dele.delete()
       
        if len(product)==len(quantity)==len(tax)==len(total)==len(rate):

            mapped = zip(product,quantity,tax,total,rate,desc)
            mapped = list(mapped)
        
            for element in mapped:

                created =sales_item(sale=sales,product=element[0],
                                    quantity=element[1],tax=element[2],total=element[3],rate=element[4],desc=element[5])
                created.save()
                    
               
            return redirect('sales_order_det',id)
                
    context={
        "c":c,
        "itm":itm,
        "saleitm":salesitem,
        "sale":sales,
        "pay":pay,
         "company":company

    }
    return render(request,'edit_sale_page.html',context)
    
    
def create_delivery_chellan(request):
    user = request.user
    # print(user_id)
    company = company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    dates=date.today()
    estimates_count = DeliveryChellan.objects.filter(user_id=user.id).count()
    print(estimates_count)
    next_count = estimates_count+1

    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))

    context = {'company': company,
               'items': items,
               'customers': customers,
               'count': next_count,
               'date':dates,
               'unit':unit,
               'sale':sale,
               'purchase':purchase,
                "account":account,
                "account_type":account_type,
                "accounts":accounts,
                "account_types":account_types,

               }

    return render(request, 'create_delivery_chellan.html', context)


def delivery_chellan_home(request):
    company = company_details.objects.get(user = request.user)
    viewitem=DeliveryChellan.objects.filter(user=request.user)
    
    return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
def create_challan_draft(request):
    
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
   
    if request.method == 'POST':
        cust_name = request.POST['customer_name']
        chellan_no = request.POST['chellan_number']
        reference = request.POST['reference']
        chellan_date = request.POST['chellan_date']
        customer_mailid = request.POST['customer_mail']
        chellan_type = request.POST['chellan_type']

        item = request.POST.getlist('item[]')
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
       

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST['igst'])
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = "Draft"
        tot_in_string = str(total)

        challan = DeliveryChellan(user=user, customer_name=cust_name, chellan_no=chellan_no, reference=reference, chellan_date=chellan_date, customer_mailid=customer_mailid,
                              sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt,chellan_type=chellan_type, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        challan.save()

        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = ChallanItems.objects.create(
                    chellan=challan, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

        cust_email = customer.objects.get(
            user=user, customerName=cust_name).customerEmail
        
        # subject = 'Estimate'
        # message = 'Dear Customer,\n Your Estimate has been Saved for a total amount of: ' + tot_in_string
        # recipient = cust_email
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('delivery_chellan_home')

def create_and_send_challan(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    
   
    if request.method == 'POST':
        cust_name = request.POST['customer_name']
        chellan_no = request.POST['chellan_number']
        reference = request.POST['reference']
        chellan_date = request.POST['chellan_date']
        customer_mailid = request.POST['customer_mail']
        chellan_type = request.POST['chellan_type']

        item = request.POST.getlist('item[]')
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
      

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST['igst'])
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Send'
        tot_in_string = str(total)

        challan = DeliveryChellan(user=user, customer_name=cust_name, chellan_no=chellan_no, reference=reference, chellan_date=chellan_date, customer_mailid=customer_mailid,
                              sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt,chellan_type=chellan_type, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        challan.save()

        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = ChallanItems.objects.create(
                    chellan=challan, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

        cust_email = customer.objects.get(
            user=user, customerName=cust_name).customerEmail
      
        subject = 'Delivery Challan'
        message = 'Dear Customer,\n Your Delivery Challan has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('delivery_chellan_home')


def add_customer_for_challan(request):
   
    return render(request,'create_cust_challan.html')
    
def payment_term_challan(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_for_challan")

def entr_custmr_for_challan(request):
    print("sdfdsfsds")
    type=request.GET.get('types')
    txtFullName=request.GET.get('txtFullNames')
    cpname=request.GET.get('cpnames')
    email=request.GET.get('email_ids')
    mobile=request.GET.get('mobiles')
    wbsite=request.GET.get('wbsites')
    gstt=request.GET.get('gstts')
    posply=request.GET.get('posplys')
    tax1=request.GET.get('tax1s')
    crncy=request.GET.get('crncys')
    obal=request.GET.get('obals')
    select=request.GET.get('ptermss')
    pterms=request.GET.get('ptermss')
    plst=request.GET.get('plsts')
    plang=request.GET.get('plangs')
    fbk=request.GET.get('fbks')
    twtr=request.GET.get('twtrs')
    atn=request.GET.get('atns')
    ctry=request.GET.get('ctrys')
    addrs=request.GET.get('addrss')
    addrs1=request.GET.get('addrs1s')
    bct=request.GET.get('bcts')
    bst=request.GET.get('bsts')
    bzip=request.GET.get('bzips')
    bpon=request.GET.get('bpons')
    bfx=request.GET.get('bfxs')
    sal=request.GET.get('sals')
    ftname=request.GET.get('ftnames')
    ltname=request.GET.get('ltnames')
    mail=request.GET.get('mails')
    bworkpn=request.GET.get('bworkpns')
    bmobile=request.GET.get('bmobiles')

    bskype=request.GET.get('bskypes')
    bdesg=request.GET.get('bdesgs')
    bdept=request.GET.get('bdepts')
    u = User.objects.get(id = request.user.id)


    ctmr=customer(customerName=txtFullName,customerType=type,
                companyName=cpname,customerEmail=email,
                    customerMobile=mobile,
                    website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                        currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                        PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                            Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                            city=bct,state=bst,zipcode=bzip,phone1=bpon,
                            fax=bfx,CPsalutation=sal,Firstname=ftname,
                            Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                            CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                CPdepartment=bdept,user=u )
    ctmr.save() 
    print(txtFullName)
    return JsonResponse({"status": " not", 'customer': txtFullName, "plos":posply})
        
@login_required(login_url='login')
def additem_page_challan(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_challan.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_challan(request):
    
    radio=request.GET.get('radios')
    inter=request.GET.get('inters')
    intra=request.GET.get('intras')
    type=request.GET.get('types')
    name=request.GET.get('names')
    unit=request.GET.get('units')
    sel_price=request.GET.get('sel_prices')
    sel_acc=request.GET.get('sel_accs')
    s_desc=request.GET.get('s_descs')
    cost_price=request.GET.get('cost_prices')
    cost_acc=request.GET.get('cost_accs')      
    p_desc=request.GET.get('p_descs')
    u=request.user.id
    us=request.user
    history="Created by" + str(us)
    user=User.objects.get(id=u)
    unit=Unit.objects.get(id=unit)
    sel=Sales.objects.get(id=sel_acc)
    cost=Purchase.objects.get(id=cost_acc)
    ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                    )
    ad_item.save()

    return JsonResponse({"status": " not", 'name': name})

def delivery_challan_view(request, id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user)
    estimate = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=estimate)
    print(items)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'delivery_challan_view.html', context)


# delivery_challan_edit.html

def delivery_challan_edit(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    customers = customer.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    estimate = DeliveryChellan.objects.get(id=id)
   
    
    pls= customer.objects.get(customerName=estimate.customer_name)
    
    est_items = ChallanItems.objects.filter(chellan=estimate)

    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))

    

    context = {
        'company': company,
        'estimate': estimate,
        'customers': customers,
        'items': items,
        'est_items': est_items,
        'unit':unit,
        'sale':sale,
        'purchase':purchase,
        "account":account,
        "account_type":account_type,
        "accounts":accounts,
        "account_types":account_types,
        "pls":pls,
    }
    return render(request, 'delivery_challan_edit.html', context)

def update_challan(request,id):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == "POST":
        estimate = DeliveryChellan.objects.get(id=id)
        
        estimate.customer_name = request.POST['customer_name']
        estimate.chellan_no = request.POST['chellan_number']
        estimate.reference = request.POST['reference']
        estimate.chellan_date = request.POST['challan_date']
        estimate.customer_mailid = request.POST['customer_mail']
        estimate.chellan_type = request.POST['chellan_type']
    

        estimate.customer_notes = request.POST['customer_note']
        estimate.sub_total = float(request.POST['subtotal'])
        estimate.tax_amount = float(request.POST['total_taxamount'])
        estimate.shipping_charge = float(request.POST['shipping_charge'])
        estimate.adjustment = float(request.POST['adjustment_charge'])
        estimate.total = float(request.POST['total'])
        estimate.terms_conditions = request.POST['tearms_conditions']
        estimate.status = 'Draft'

        old=estimate.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            estimate.attachment = old
        else:
            estimate.attachment = new

        estimate.save()

        item = request.POST.getlist('item[]')
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        objects_to_delete = ChallanItems.objects.filter(chellan=id)
        objects_to_delete.delete()

        
        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = ChallanItems.objects.get_or_create(
                    chellan=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
        return redirect('delivery_chellan_home')
    return redirect('delivery_chellan_home')

def get_cust_mail(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
  
    cust = request.GET.get('cust')
    print(cust)


    item = customer.objects.get(customerName=cust, user=user)

    # comp=item.companyName
    # print(comp)
    email = item.customerEmail
    # print(email)

    ads=item.Address1
    # print(site)

    mob=item.customerMobile
    # print(mob)

    cust_id=item.id
    cust_place_supply=item.placeofsupply

    
    return JsonResponse({"status": " not", 'email': email,'ads':ads,'mob':mob,'cust_id':cust_id,'cust_place_supply':cust_place_supply})
    return redirect('/')
    
def add_customer_edit_challan(request):
   
    return render(request,'create_cust_challan_edit.html')



def payment_term_challan_edit(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_edit_challan")

def sv_cust_edit_challan(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
           
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("delivery_chellan_home")
        return redirect("delivery_chellan_home")

@login_required(login_url='login')
def additem_edit_challan(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_challanedit.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_challan_edit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("delivery_chellan_home")
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_account_challan_edit(request):
    print("haii")
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_edit_challan")
        
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_unit_edit_challan(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_edit_challan')
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_sales_edit_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_edit_challan')
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_account_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_page_challan")
        
    return redirect("additem_page_challan")

@login_required(login_url='login')
def add_unit_challan(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_page_challan')
    return redirect("additem_page_challan")

@login_required(login_url='login')
def add_sales_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_page_challan')
    return redirect("additem_page_challan")



def render_challan_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = DeliveryChellan.objects.filter(user=user)
    challan = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=challan)
    print(challan.customer_name) 
    print(challan.customer_mailid)
    customers = customer.objects.get(user=user,customerName=challan.customer_name,customerEmail=challan.customer_mailid)



    print(items)
    

    total = challan.total

    template_path = 'delivery_challan_pdf.html'
    context = {
        'company': company,
        'challn_on':challn_on,
        'challan': challan,
        'items': items,
        'customers':customers
    }
    fname=challan.chellan_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def deletechallan(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = DeliveryChellan.objects.get(id=id,user=user)
    items = ChallanItems.objects.filter(chellan=id)
    items.delete()
    estimate.delete()
    return redirect('delivery_chellan_home')
    
def filter_chellan(request):
    if request.method=='POST':
        flter_drop  =request.POST['flter_drop']
        company = company_details.objects.get(user = request.user)
        if flter_drop == "Draft":
            viewitem=DeliveryChellan.objects.filter(user=request.user, status="Draft") 
        elif flter_drop == "Send":
            viewitem=DeliveryChellan.objects.filter(user=request.user, status="Send")
        else:
            viewitem=DeliveryChellan.objects.filter(user=request.user)
        return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
    return redirect("delivery_chellan_home") 
    
def filter_chellan_type(request):
    if request.method=='POST':
        flter_drop  =request.POST['flter_tp']
        usr_in  =request.POST['usr_in']
        company = company_details.objects.get(user = request.user)
        if flter_drop == "Customer":
            viewitem=DeliveryChellan.objects.filter(user=request.user, customer_name=usr_in) 
        elif flter_drop == "Date":
            fromdate=datetime.strptime(usr_in, "%d-%m-%Y").date()
            print(fromdate)

            viewitem=DeliveryChellan.objects.filter(user=request.user, chellan_date=fromdate)
        elif flter_drop == "Amount":
            viewitem=DeliveryChellan.objects.filter(user=request.user, total=usr_in)
        else:
            viewitem=DeliveryChellan.objects.filter(user=request.user)
        return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
    return redirect("delivery_chellan_home") 
    
    
def itemdata_challan(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    

    

    item = AddItem.objects.get(Name=id, user=user)
    name=item.Name
    rate = item.p_price
    place = company.state

    return JsonResponse({"status": " not", 'place': place, 'rate': rate})
    return redirect('/')
    

def payment_term_for_sales(request):
    
    if request.method == 'POST':
        terms = json.loads(request.POST.get('terms', '[]'))
        days = json.loads(request.POST.get('days', '[]'))
        pay_term=terms[0]
        if len(terms) == len(days):
            for term, day in zip(terms, days):
                
                created = payment_terms.objects.get_or_create(Terms=term, Days=day)
            return JsonResponse({"message": "success","pay_term":pay_term})
        print(pay_term)
    return JsonResponse({"message": "success",})    
    
    
def report_page(request):
    return render(request,'reports.html')

def report_recurring_invoice(request):
    return render(request,'report_recurring_invoice.html')
    
def payment_recur(request):
    if request.method=='POST':
        print('hi')
        terms=request.POST.get('name')
        print(terms)
        day=request.POST.get('days')
        print(day)
        ptr=payments_recur(Terms=terms,Days=day)
        ptr.save()
        response_data={
            "message":"success",
            "terms":terms,
        }
        return JsonResponse(response_data)

def create_recur(request):
    user = request.user
    # print(user_id)
    company = company_details.objects.get(user=user)
    item=AddItem.objects.all()
    cus=customer.objects.all()
    pay=payments_recur.objects.all()
    every=repeat_every.objects.all()
     
    
    return render(request,'samrecurpage.html',{'item':item,'cus':cus,'pay':pay,'company':company,'every':every})

def new_recur(request):
    if request.method=='POST':
        
        custname=request.POST.get('customer')
        cusemail=request.POST.get('mails')
        cusadd=request.POST.get('addr')

        pos=request.POST.get('supply')
        e_type=request.POST.get('type')
        profile=request.POST.get('name')
        onumber=request.POST.get('order')
        repeat=request.POST.get('every')
        sdate=request.POST.get('start')
        edate=request.POST.get('end')
        pay=request.POST.get('terms')
        notes=request.POST.get('customer_note')
        terms=request.POST.get('ter_cond')
        sub=request.POST.get('subtotal')
        i=request.POST.get('igst')
        c=request.POST.get('cgst')
        s=request.POST.get('sgst')
        taxamt=request.POST.get('total_taxamount')
        ship=request.POST.get('shipping_charge')
        adj=request.POST.get('adjustment_charge')
        tot=request.POST.get('total')
       
        recur=recurring_invoice(
            cname=custname,
            cemail=cusemail,
            cadrs=cusadd,
            p_supply=pos,
            entry_type=e_type,
            name=profile,
            order_num=onumber,
            every=repeat,
            start=sdate,
            end=edate,
            terms=pay,
            cust_note=notes,
            conditions=terms,
            sub_total=sub,
            igst=i,
            cgst=c,
            sgst=s,
            tax_amount=taxamt,
            shipping_charge=ship,
            adjustment=adj,
            total=tot,
            user = request.user,

        )
        recur.save()
        items=request.POST.getlist('item[]')
        print(items)
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        print(quantity)
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        print(rate)
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        print(discount)
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        print(tax)
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        print(amount)
        
        if len(items)==len(quantity)==len(rate)==len(discount)==len(tax)==len(amount):
            print('testing')
            print(items)
            print(quantity)
            print(rate)
            print(discount)
            print(tax)
            print(amount)
            mapped1 = zip(items,quantity,rate,discount,tax,amount)
            mapped = list(mapped1)
            for element in mapped:
                created =recur_itemtable.objects.get_or_create(
                    iname=element[0], quantity=element[1], rate=element[2], discount=element[3], tax=element[4],amt=element[5],ri=recur)
        
                
        return redirect('view_recurpage')
    else:
        return render(request,'samrecurpage.html')


def view_recurpage(request):
    recur=recurring_invoice.objects.all()
    company=company_details.objects.get(user_id=request.user.id)

    return render(request,'recurringonvoice.html',{'recur':recur,'company':company})

def viewrecur(request,id):
    cust = customer.objects.filter(user_id=request.user.id)
    company=company_details.objects.get(user_id=request.user.id)
    items=recurring_invoice.objects.all()
    product=recurring_invoice.objects.get(id=id)
    table=recur_itemtable.objects.filter(ri=id)
    print(product.id)
    return render(request,'recur_invoice.html',{'customer':cust,'allproduct':items,'product':product,'itemstable':table,'company':company})


def edit_recur(request,id):
    item=AddItem.objects.all()
    cus=customer.objects.all()
    pay=payments_recur.objects.all()
    every=repeat_every.objects.all()
    editr=recurring_invoice.objects.get(id=id)
    tab=recur_itemtable.objects.filter(ri=id)
    company=company_details.objects.get(user_id=request.user.id)

    return render(request,'edit_recur.html',{'editr':editr,'cus':cus,'tab':tab,'item':item,'pay':pay,'every':every,'company':company})
   

def editrecurpage(request,id):
    if request.method=='POST':
        edit=recurring_invoice.objects.get(id=id)
        edit.cname=request.POST['customer']
        edit.cemail=request.POST['mails']
        edit.cadrs=request.POST['addr']
        edit.p_supply=request.POST['supply']
        edit.entry_type=request.POST['type']
        edit.name=request.POST['name']
        edit.order_num=request.POST['order']
        edit.every=request.POST['every']
        edit.start=request.POST['start']
        edit.end=request.POST['end']
        edit.terms=request.POST['terms']
        edit.cust_note=request.POST['customer_note']
        edit.conditions=request.POST['ter_cond']
        edit.adjustment=request.POST['adjustment_charge']
        edit.shipping_charge=request.POST['shipping_charge']
        edit.sub_total = float(request.POST['subtotal'])
        edit.tax_amount = float(request.POST['total_taxamount'])
        edit.total = float(request.POST['total'])
        edit.cgst = float(request.POST['cgst'])
        edit.sgst = float(request.POST['sgst'])
        edit.igst = float(request.POST['igst'])
        items=request.POST.getlist('item[]')
        # print(items)
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        # print(quantity)
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        # print(rate)
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        # print(discount)
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        print(tax)
        tax2=request.POST.getlist('taxx[]')
        taxx = [float(x) for x in tax2]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        print(amount)
        sam=recur_itemtable.objects.filter(ri=id).delete()
        if len(items)==len(quantity)==len(rate)==len(discount)==len(tax)==len(taxx)==len(amount):
            print(items)
            print(quantity)
            print(rate)
            print(discount)
            print(tax)
            print(amount)
            mapped1 = zip(items,quantity,rate,discount,tax,amount)
            mapped = list(mapped1)
            for element in mapped:
                created =recur_itemtable.objects.get_or_create(
                    iname=element[0], quantity=element[1], rate=element[2], discount=element[3], tax=element[4], amt=element[5],ri=edit)
        edit.save()
        return redirect('view_recurpage')



def del_recur(request,del_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate =recurring_invoice.objects.get(id=del_id)
    items =recur_itemtable.objects.filter(ri=estimate)
    items.delete()
    estimate.delete()
    # d=recurring_invoice.objects.get(id=id)
    # # d1=recur_itemtable.objects.get(id=id)
    # d.delete()
    # # d1.delete()
    return redirect('view_recurpage')


    
def itemdata_recur(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    print(id)
    print(cust)

    item = AddItem.objects.get(Name=id, user=user)

    rate = item.p_price
    place = company.state
    gst = item.intrastate
    igst = item.interstate
    place_of_supply = customer.objects.get(
        customerName=cust, user=user).placeofsupply
    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'pos': place_of_supply, 'gst': gst, 'igst': igst})
    return redirect('/')


    
@login_required(login_url='login')
def recurring_bill(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    context = {
                'company' : company,
                'recur_bill' : recur
            }
    return render(request,'recurring_bills.html',context)

# filter

@login_required(login_url='login')
def recur_custasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['cust_name'])    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_custdesc(request):
    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['cust_name'],reverse=True)    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_vendorasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['vend_name'])    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_vendordesc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

        sorted_recur = sorted(recur, key=lambda r: r['vend_name'],reverse=True)    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_profileasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['profile_name'],reverse=False) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_profiledesc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['profile_name'],reverse=True) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def add_recurring_bills(request):

    company = company_details.objects.get(user = request.user)
    vendor = vendor_table.objects.filter(user = request.user)
    acnt_name = Chart_of_Account.objects.filter(user = request.user)
    acnt_type = Chart_of_Account.objects.filter(user = request.user).values('account_type').distinct()
    cust = customer.objects.filter(user = request.user)
    item = AddItem.objects.filter(user = request.user)
    payments = payment_terms.objects.filter(user = request.user)
    units = Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    sales_type = set(Sales.objects.values_list('Account_type', flat=True))
    purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
    context = {
                'company' : company,
                'vendor' : vendor,
                'account': acnt_name,
                'account_type' : acnt_type,
                'customer' : cust,
                'item' : item,
                'payments' :payments,
                'units' :units,
                'sales' :sales,
                'purchase':purchase,
                'sales_type':sales_type,
                'purchase_type':purchase_type,
            }
    return render(request,'add_recurring_bills.html',context)

@login_required(login_url='login')
def create_recurring_bills(request):

    company = company_details.objects.get(user = request.user)
    # print(request.POST.get('customer').split(" ")[0])
    cust = customer.objects.get(id=request.POST.get('customer').split(" ")[0],user = request.user)

    if request.method == 'POST':
        # vname = request.POST.get('vendor').rsplit(' ', 1)
        # cname = request.POST.get('customer').split(" ")[1:]
        vname  = request.POST.get('vendor')
        cname = request.POST.get('customer')
        # cname = " ".join(cname)
        v_gst_no=request.POST.get('gstin_inp')   # haripriya add
        src_supply = request.POST.get('srcofsupply')
        prof = request.POST['prof_name']
        repeat = request.POST['repeat']
        start = request.POST.get('start_date')
        end = None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        pay_term =request.POST['terms']

        sub_total =request.POST['subtotal']

        sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        igst= None if request.POST.get('igst') == "" else  request.POST.get('igst')
        # print(igst)

        if src_supply == company.state:
            tax1 = sgst + cgst
        else:
            tax1 = igst
           
        # print(tax1)

        shipping_charge=0 if request.POST['addcharge'] == "" else request.POST['addcharge']
        grand_total=request.POST['grand_total']
        note=request.POST.get('note')

        u = User.objects.get(id = request.user.id)

        bills = recurring_bills(vendor_name=vname,profile_name=prof,customer_name = cname,vendor_gst_number=v_gst_no,
                    source_supply=src_supply,repeat_every = repeat,start_date = start,end_date = end,
                    payment_terms =pay_term,sub_total=sub_total,sgst=sgst,cgst=cgst,igst=igst,
                    tax_amount=tax1, shipping_charge = shipping_charge,
                    grand_total=grand_total,note=note,company=company,user = u,  )
        bills.save()

        r_bill = recurring_bills.objects.get(id=bills.id)

        if len(request.FILES) != 0:
            r_bill.document=request.FILES['file'] 
            r_bill.save()

        items = request.POST.getlist("item[]")
        accounts = request.POST.getlist("account[]")
        quantity = request.POST.getlist("qty[]")
        rate = request.POST.getlist("rate[]")
        
        if (" ".join(src_supply.split(" ")[1:])) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = 0 if request.POST.getlist("discount[]") == " " else request.POST.getlist("discount[]")
        amount = request.POST.getlist("amount[]")

        if len(items)==len(accounts)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) and items and accounts and quantity and rate and tax and discount and amount:
                
                mapped=zip(items,accounts,quantity,rate,tax,discount,amount)
                mapped=list(mapped)

                for ele in mapped:

                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                    try:
                        int(ele[1])
                        ac = Chart_of_Account.objects.get(user = request.user,id = ele[1]).account_name
                        
                    except ValueError:
                        
                        ac = ele[1]
                    
                    created = recurring_bills_items.objects.create(item = it,account = ac,quantity=ele[2],rate=ele[3],
                    tax=ele[4],discount = ele[5],amount=ele[6],user = u,company = company, recur_bills = r_bill)

        return redirect('recurring_bill')
    return redirect('recurring_bill')





@login_required(login_url='login')
def edit_recurring_bills(request,id):

    company = company_details.objects.get(user = request.user)
    vendor = vendor_table.objects.filter(user = request.user)
    acnt = Chart_of_Account.objects.filter(user = request.user)
    acnt_type = Chart_of_Account.objects.filter(user = request.user).values('account_type').distinct()
    cust = customer.objects.filter(user = request.user)
    item = AddItem.objects.filter(user = request.user)
    payments = payment_terms.objects.filter(user = request.user)
    units = Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    
    sales_type = set(Sales.objects.values_list('Account_type', flat=True))
    purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
    recur_bills = recurring_bills.objects.get(user = request.user,id=id)
    recur_item = recurring_bills_items.objects.filter(user = request.user,recur_bills = id)   

    c = customer.objects.filter(user = request.user).get(id = recur_bills.customer_name.split(' ')[0])
    v = vendor_table.objects.filter(user = request.user).get(id = recur_bills.vendor_name.split(" ")[0])
    # print(recur_bills.customer_name.split(" ")[2:])
    context = {
        'company' : company,
        'vendor' : vendor,
        'account': acnt,
        'account_type' : acnt_type,
        'customer' : cust,
        'item' : item,
        'payments' :payments,
        'units' :units,
        'sales' :sales,
        'purchase':purchase,
        'sales_type':sales_type,
        'purchase_type':purchase_type,
        'recur_bills': recur_bills,
        'recur_items' : recur_item,
        'cust':c,
        'vend' : v,
        'vend_name' : " ".join(recur_bills.vendor_name.split(" ")[1:]),
        'cust_name' : " ".join(recur_bills.customer_name.split(" ")[2:])
    }

    return render(request,'edit_recurring_bills.html',context)


def change_recurring_bills(request,id):
            
    company = company_details.objects.get(user = request.user)
    # cust = customer.objects.get(customerName=request.POST.get('customer').strip(" "),user = request.user)
    r_bill=recurring_bills.objects.get(user = request.user,id=id)

    if request.method == 'POST':
        
        r_bill.vendor_name = request.POST.get('vendor')
        r_bill.customer_name= request.POST.get('customer')
        r_bill.profile_name = request.POST['prof_name']
        r_bill.source_supply=request.POST['srcofsupply']
        r_bill.repeat_every=request.POST['repeat']
        r_bill.start_date=request.POST['start_date']
        r_bill.end_date=None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        r_bill.payment_terms=request.POST['terms']
        r_bill.note=request.POST['note']
        r_bill.sub_total=None if request.POST.get('subtotal') == "" else  request.POST.get('subtotal')
        r_bill.igst=None if request.POST.get('igst') == "" else  request.POST.get('igst')
        r_bill.cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        r_bill.sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        r_bill.shipping_charge=request.POST['addcharge']
        r_bill.grand_total=request.POST.get('grand_total')

        if len(request.FILES) != 0:
             
            r_bill.document = request.FILES['file']
            

        r_bill.save()          

        items = request.POST.getlist("item[]")
        accounts = request.POST.getlist("account[]")
        quantity = request.POST.getlist("quantity[]")
        rate = request.POST.getlist("rate[]")

        if (" ".join(request.POST['srcofsupply'].split(" ")[1:])) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = 0 if request.POST.getlist("discount[]") == " " else request.POST.getlist("discount[]")
        amount = request.POST.getlist("amount[]")

        if len(items)==len(accounts)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) and items and accounts and quantity and rate and tax and discount and amount:
                
            mapped=zip(items,accounts,quantity,rate,tax,discount,amount)
            mapped=list(mapped)

            
            count = recurring_bills_items.objects.filter(recur_bills=r_bill.id).count()
            
            for ele in mapped:

                if int(len(items))>int(count):

                    pbillss=recurring_bills.objects.get(id=id)
                    company = company_details.objects.get(user = request.user)
                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                    try:
                        int(ele[1])
                        ac = Chart_of_Account.objects.get(user = request.user,id = ele[1]).account_name
                        
                    except ValueError:
                        
                        ac = ele[1]
                    
                    created = recurring_bills_items.objects.get_or_create(item = it,account = ac,quantity=ele[2],rate=ele[3],
                    tax=ele[4],discount = ele[5],amount=ele[6],recur_bills=r_bill.id,company=company,user = request.user)


                else:
                    
                    dbs=recurring_bills_items.objects.get(recur_bills =r_bill.id,item = ele[0],account=ele[1])
                    created = recurring_bills_items.objects.filter(recur_bills =dbs.recur_bills,items = ele[0],account=ele[1]).update(item = ele[0],
                        account = ele[1],quantity=ele[2],rate=ele[3], tax=ele[4],discount=ele[5],amount= ele[6])
 

        return redirect('view_recurring_bills',id)
    return redirect('recurring_bill')


@login_required(login_url='login')
def delete_recurring_bills(request, id):

    company = company_details.objects.get(user = request.user)
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    rbill.delete() 
    billitem.delete() 
     
    return redirect('recurring_bill')


    
@login_required(login_url='login')
def view_recurring_bills(request,id):

    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user)
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)
    
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
            }

    return render(request, 'view_recurring_bills.html',context)


@login_required(login_url='login')
def view_custasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('customer_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName = rbill.customer_name)

    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)


@login_required(login_url='login')
def view_custdesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-customer_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_vendorasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('vendor_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_vendordesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-vendor_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_profileasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('profile_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_profiledesc(request,id):

    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-profile_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName = rbill.customer_name)

    gst_or_igst = "GST" if comp_state == rbill.source_supplysupply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
            }
    return render(request,'view_recurring_bills.html',context)


@login_required(login_url='login')
def get_vendordet(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id, id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr},safe=False)

@login_required(login_url='login')
def get_customerdet(request):
    company= company_details.objects.get(user = request.user)
    name = request.POST.get('name')
    id = request.POST.get('id')
    cust = customer.objects.get(user=company.user_id,id=id)
    email = cust.customerEmail
    cust_id=id
    cust_place_supply=cust.placeofsupply
    gstin = 0
    gsttr = cust.GSTTreatment
    cstate = cust.placeofsupply.split("] ")[1:]
    print(email)
    print(gstin)
    print(id)
    state = 'Not Specified' if cstate == "" else cstate
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin , 'state' : state,'cust_id':cust_id,'cust_place_supply':cust_place_supply},safe=False)

@login_required(login_url='login')
def recurbills_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def vendor_dropdown(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user = user)
    for option in option_objects:
        
        options[option.id] = [option.salutation, option.first_name, option.last_name, option.id]
    return JsonResponse(options)



@login_required(login_url='login')
def recurbills_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def pay_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.Terms,option.Days]

    return JsonResponse(options)


@login_required(login_url='login')
def recurbills_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = [option.unit,option.id]

    return JsonResponse(options)

@login_required(login_url='login')
def recurbills_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        
        type=request.POST.get('type')
        name=request.POST.get('name')
        ut=request.POST.get('unit')
        inter=request.POST.get('inter')
        intra=request.POST.get('intra')
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)

        u  = User.objects.get(id = request.user.id)

        item=AddItem(type=type,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=u ,creat=history,interstate=inter,intrastate=intra,unit = units,sales = sel, purchase = cost)

        item.save()

        return HttpResponse({"message": "success"})
    
    return HttpResponse("Invalid request method.")

        
@login_required(login_url='login')
def item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.filter(user = request.user)
    for option in option_objects:
        options[option.id] = [option.Name,option.id]

    return JsonResponse(options)


@login_required(login_url='login')
def recurbills_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)
        
        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Chart_of_Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.account_name,option.id]

    return JsonResponse(options)


@login_required(login_url='login')
def get_rate(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':
        id=request.POST.get('id')

        item = AddItem.objects.get( id = id, user = user)
         
        rate = 0 if item.s_price == "" else item.s_price

        return JsonResponse({"rate": rate},safe=False)
    
@login_required(login_url='login')
def get_cust_state(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':

        id=request.POST.get('id')
        cust = customer.objects.get(id = id, user = user)
        cstate = cust.placeofsupply.split("] ")[1]
        state = 'Not Specified' if cstate == "" else cstate

        return JsonResponse({"state": state},safe=False)
    
@login_required(login_url='login')
def export_pdf(request, id):
    company = company_details.objects.get(user=request.user)
    bills = recurring_bills.objects.filter(user=request.user)
    rbill = recurring_bills.objects.get(user=request.user, id=id)
    billitem = recurring_bills_items.objects.filter(user=request.user, recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName=" ".join(rbill.customer_name.split(" ")[1:]))

    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"

    tax_total = 0
    for b in billitem:
        tax_total += b.tax

    template_path = 'view_recurring_bills.html'
    context = {
        'company': company,
        'recur_bills': bills,
        'recur_bill': rbill,
        'bill_item': billitem,
        'tax': tax_total,
        "gst_or_igst": gst_or_igst,
        'customer': cust,
    }
     
    fname= rbill.profile_name
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF( html, dest=response)
 
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@login_required(login_url='login')
def recurbill_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        r_bill = recurring_bills.objects.get(user = request.user, id = id)
        r_bill.comments = cmnt
        r_bill.save()

        return HttpResponse({"message": "success"})

@login_required(login_url='login')
def recurbill_add_file(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)
    print(bill)

    if request.method == 'POST':

        bill.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bill.document = request.FILES['file']

        bill.save()
        return redirect('view_recurring_bills',id)
    

@require_POST
def recurbill_email(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)

    if request.method == 'POST':

        recipient =request.POST.get('recipient')
        sender =request.POST.get('sender')
        sub =request.POST.get('subject')
        message =request.POST.get('message')

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'view_recurring_bills.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()
        

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    if template:
        prntonly_content = str(template)

    # print(prntonly_content)
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
        temp_file.write(prntonly_content.encode('utf-8'))

    with open(temp_file.name, 'rb') as attachment_file:
        attachment_content = attachment_file.read()

    email = EmailMessage(
        subject=sub,
        body=message,
        from_email=sender,
        to=[recipient],
    )
    email.attach('Recurring Bill',attachment_content , 'text/html')

    email.send()
     
    return HttpResponse(status=200)
    
    
def get_comments(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    comments = Expense.objects.filter(expense=expense).values_list('comment', flat=True)
    return JsonResponse(list(comments), safe=False)
    

def every_terms(request):
    if request.method=='POST':
        print('hi')
        terms=request.POST.get('name')
        print(terms)
        ptr=repeat_every(Terms=terms)
        ptr.save()
        response_data={
            "message":"success",
            "terms":terms,
        }
        return JsonResponse(response_data)
        
        
def cust_create(request):
    sb=payment_terms.objects.all()
    return render(request,'customer_cr.html',{'sb':sb})
    
def customer_me(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('email')
            wphone=request.POST.get('fname')
            mobile=request.POST.get('lname')
            skname=request.POST.get('skype')
            desg=request.POST.get('des')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("create_recur")
        return redirect("/")
        
        
@login_required(login_url='login')
def recurbills_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def customer_dropdown(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user=user)
    for option in option_objects:
        display_name = option.customerName
        # options[option.id] = [option.id , option.customerName]
        options[option.id] = [display_name, f"{display_name}"]
    return JsonResponse(options)
    
    
def entr_custmrA(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cr_data=customer()
            print('hii')
            print(cr_data)
            type=request.POST.get('type')
            fName=request.POST['fName']
            lName=request.POST['lName']
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('email')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('v_gsttype')
            
            x=request.POST.get('v_gsttype')
            if x=="Unregistered Business-not Registered under GST":
                pan=request.POST.get('pan_number')
                gstin="null"
            else:
                gstin=request.POST.get('v_gstin')
                pan=request.POST.get('pan_number')
           
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            # select=request.POST.get('pterms')
            
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')
            remark=request.POST.get('remark')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,
                          Fname=fName,Lname=lName,
                          customerType=type,
                        companyName=cpname,
                        customerEmail=email,
                        customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,
                         designation=desg,department=dept,
                           website=wbsite
                           ,GSTTreatment=gstt,
                           GSTIN=gstin,pan_no=pan,
                           placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,
                             PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,
                                Facebook=fbk,
                                Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,
                                     remark=remark,user=u )
            ctmr.save() 
 
            #  ...........................adding multiple rows of table to model  ........................................................       
            CPsalutation =request.POST.getlist('sal[]')
            Firstname=request.POST.getlist('ftname[]')
            Lastname =request.POST.getlist('ltname[]')
            CPemail =request.POST.getlist('mail[]')
            CPphone=request.POST.getlist('bworkpn[]')
            CPmobile=request.POST.getlist('bmobile[]')
            CPskype=request.POST.getlist('bskype[]')
            CPdesignation=request.POST.getlist('bdesg[]')
            CPdepartment=request.POST.getlist('bdept[]') 
            
            cdata=customer.objects.get(id=ctmr.id)
            Customr=cdata 
            
            if len(CPsalutation)==len(Firstname)==len(Lastname)==len(CPemail)==len(CPphone)==len(CPmobile)==len(CPskype)==len(CPdesignation)==len(CPdepartment):
                mapped2=zip(CPsalutation,Firstname,Lastname,CPemail,CPphone,CPmobile,CPskype,CPdesignation,CPdepartment)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = customer_contact_person_table.objects.get_or_create(CPsalutation=ele[0],Firstname=ele[1],Lastname=ele[2],CPemail=ele[3],
                            CPphone=ele[4],CPmobile=ele[5],CPskype=ele[6],CPdesignation=ele[7],CPdepartment=ele[8],user=u,Customr=Customr)
            
            return redirect("view_customr")
        return render(request,'view_customer.html')
        
        
def payment_termA(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return HttpResponse( {"message":"success"})
        
        
def dashboard(request):
    company=company_details.objects.get(user=request.user)
    return render(request,'Dashboard.html',{'company':company})
    
    
def delete_customr(request,id):
    if customer_comments_table.objects.filter(customr=id).exists():
        us2=customer_comments_table.objects.filter(customr=id)
        us2.delete()
    if customer_mail_table.objects.filter(customr=id).exists():
        us3=customer_mail_table.objects.filter(customr=id)
        us3.delete()
    if customer_doc_upload_table.objects.filter(customr=id).exists():

        us5=customer_doc_upload_table.objects.filter(customr=id)
        us5.delete()
    if customer_contact_person_table.objects.filter(Customr=id).exists():
        us4=customer_contact_person_table.objects.filter(Customr=id)
        us4.delete()
    cs=customer.objects.get(id=id)
    cs.delete()
    return redirect('view_customr')
    
def view_customr(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.all()
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_customr_sname(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.order_by('customerName')
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_customr_scpname(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.order_by('companyName')
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_one_customer(request,id):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.all()
    cu=customer.objects.get(id=id)
    em=customer_mail_table.objects.all()
    return render(request,'view_one_customer.html',{'vc':vc,'cu':cu,"company":company,'em':em})
    
def editcustomer(request,id):
    company=company_details.objects.get(user=request.user)
    cu=customer.objects.get(id=id)
    pt=payment_terms.objects.all()
    prc=Pricelist.objects.all()
    if customer_contact_person_table.objects.filter(Customr=cu).exists():
        pdata=customer_contact_person_table.objects.filter(Customr=cu)
        return render(request,'edit_customer.html',{'cu':cu,'pt':pt,'prc':prc,'pdata':pdata})      

    else:
        return render(request,'edit_customer.html',{'cu':cu,'pt':pt,'prc':prc,'company':company})
    
    
def editEnter_customer(request,id):
        if request.method=='POST':
            edit=customer.objects.get(id=id)
            edit.customerType=request.POST['type']
            edit.Fname=request.POST['first_name']
            edit.Lname=request.POST['last_name']
            edit.customerName=request.POST['txtFullName']
            edit.companyName=request.POST['cpname']

            edit.customerEmail=request.POST['email']
            edit.customerWorkPhone=request.POST['wphone']
            edit.customerMobile=request.POST['mobile']
            edit.skype=request.POST['skname']
            edit.designation=request.POST['desg']
            edit.department=request.POST['dept']
            edit.website=request.POST['wbsite']
            edit.GSTTreatment=request.POST['gst']
            if edit.GSTTreatment=="Unregistered Business-not Registered under GST":
                edit.pan_no=request.POST['pan_number']
                edit.GSTIN=request.POST['gst_number']
            else:
                edit.GSTIN=request.POST['gst_number']
                edit.pan_no=request.POST['pan_number']
            
            edit.placeofsupply=request.POST['posply']
            edit.Taxpreference=request.POST['tax1']
            
            edit.PaymentTerms=request.POST['pterms']
            
            edit.PriceList=request.POST['plst']
            edit.PortalLanguage=request.POST['plang']
            edit.Facebook=request.POST['fbk']
            edit.Twitter=request.POST['twtr']
            edit.Attention=request.POST['atn']
            edit.country=request.POST['ctry']

            edit.Address1=request.POST['addrs']
            edit.Address2=request.POST['addrs1']
            edit.city=request.POST['bct']
            edit.state=request.POST['bst']
            edit.zipcode=request.POST['bzip']
            edit.phone1=request.POST['bpon']
            edit.fax=request.POST['bfx']
            edit.remark=request.POST['remark']
            
           
            edit.save()

            
            # .......................contact_person_table................ deleting existing entries and inserting  ...............

            pdata=customer_contact_person_table.objects.filter(Customr=edit)
            CPsalutation =request.POST.getlist('sal[]')
            Firstname =request.POST.getlist('ftname[]')
            Lastname =request.POST.getlist('ltname[]')
            CPemail =request.POST.getlist('mail[]')
            CPphone =request.POST.getlist('bworkpn[]')
            CPmobile =request.POST.getlist('bmobile[]')
            CPskype =request.POST.getlist('bskype[]')
            CPdesignation =request.POST.getlist('bdesg[]')
            CPdepartment =request.POST.getlist('bdept[]') 

            cdata=customer.objects.get(id=edit.id)
            Customr=cdata 
            
            user_id=request.user.id
            u=User.objects.get(id=user_id)

            # .....  deleting existing rows......
            pdata.delete()
            if len(CPsalutation)==len(Firstname)==len(Lastname)==len(CPemail)==len(CPphone)==len(CPmobile)==len(CPskype)==len(CPdesignation)==len(CPdepartment):
                mapped2=zip(CPsalutation,Firstname,Lastname,CPemail,CPphone,CPmobile,CPskype,CPdesignation,CPdepartment)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = customer_contact_person_table.objects.get_or_create(CPsalutation=ele[0],Firstname=ele[1],Lastname=ele[2],CPemail=ele[3],
                            CPphone=ele[4],CPmobile=ele[5],CPskype=ele[6],CPdesignation=ele[7],CPdepartment=ele[8],user=u,Customr=Customr)
            

            return redirect('view_customr')

        return render(request,'view_customer.html')
        
def add_email_customer(request,id):
    cu=customer.objects.get(id=id)
    return render(request,'emailcustomer.html',{'cu':cu})
    
    
def paymentmethod(request):
    company=company_details.objects.get(user=request.user)
    paymnt = payment_made.objects.all()
    vendor = vendor_table.objects.all()
    banks = banking.objects.all()
    option = method.objects.all()
    context = {'paymnt':paymnt,'vendor':vendor,'banks':banks,'option':option,'company':company}
    return render (request,'payment_method.html',context)

def paymentadd_method(request):
    company=company_details.objects.get(user=request.user)
    vendors = vendor_table.objects.all()
    bank =  banking.objects.all()
    option = method.objects.all()
    context = {'vendors':vendors,'bank':bank,'option':option,'company':company}
    return render(request,'payment_method_add.html',context)

def payment_add_details(request):
    if request.method == 'POST':
        select = request.POST['select']
        vendor = vendor_table.objects.get(id=select)
        payment_method = request.POST['payment_method']
        option = method.objects.get(id=payment_method)
        reference = request.POST['reference']
        date = request.POST['date']
        paid_through = request.POST['paid_through']
        amount = request.POST['amount']
        email = request.POST['email']
        balance = request.POST['balance']
        gst_treatment = request.POST['gst']
        difference = request.POST['difference']
        
        # Determine whether it's "In-Hand Cash" or a bank name
        if paid_through == 'cash':
            cash_value = 'In-Hand Cash'
        else:
            bank_name = request.POST.get('bank_name_select', '')  # Adjust name if needed
            cash_value = bank_name
       
        data = payment_made(
            reference=reference,
            payment=option,
            date=date,
            cash=cash_value,
            amount=amount,
            vendor=vendor,
            email=email,
            balance=balance,
            current_balance=difference,
            gst=gst_treatment
        )
        data.save()
        return redirect('paymentmethod')


    
def payment_details_view(request, pk):
    company=company_details.objects.get(user=request.user)
    payment = get_object_or_404(payment_made, id=pk)
    vendors = vendor_table.objects.all()
    # Retrieve the queryset of payment_made_items objects you want to display in the template
    # For example, if you want to display all payment_made_items objects, you can do:
    payment_items = payment_made.objects.all()
    bank = banking.objects.all()  
    option = method.objects.all()
    return render(request, 'payment_details.html', {'payment': payment,'company':company, 'vendors': vendors, 'payment_items': payment_items,'bank':bank,'option':option})



def payment_edit(request):
    company=company_details.objects.get(user=request.user)
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(payment_made,id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    return render(request,'payment_details_edit.html',{'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company})


def payment_edit_view(request,pk):
    if request.method == 'POST':
        payment = payment_made.objects.get(id=pk)
        payments = request.POST.get('payment')
        option = method.objects.get(id=payments)
        payment.payment = option
        payment.reference = request.POST.get('reference')
        select = request.POST.get('select')
        vendor = vendor_table.objects.get(id=select)
        payment.vendor = vendor
        paid_through = request.POST['paid_through']
        
        print(f'paid_through: {paid_through}')  # Debugging output
        if paid_through == 'In-Hand Cash':
            cash_value = 'In-Hand Cash'
        else:
            bank_name = request.POST.get('bank_name_select', '')  # Debugging output
            cash_value = bank_name
        print(f'cash_value: {cash_value}')  # Debugging output
        payment.cash = cash_value

        payment.date = request.POST.get('date')
        payment.email = request.POST.get('email')
        payment.amount = request.POST.get('ammount')
        payment.balance = request.POST.get('balance')
        payment.current_balance = request.POST.get('current_balance')
        payment.gst = request.POST.get('gst')
        payment.save()
        return redirect('paymentmethod')
    return render(request, 'payment_details_edit.html',{'payment': payment})
    
def purchase_order(request):
    company=company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    context={
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'company':company,
        
    }
        
    return render(request,'create_purchase_order.html',context)



def purchaseView(request):
    purchase_table=Purchase_Order.objects.all()
    purchase_order_table=Purchase_Order_items.objects.all()
    company=company_details.objects.get(id=request.user.id)
    context={
        'pt':purchase_table,
        'po_t':purchase_order_table,
        'company':company,
        }
    return render(request,'purchase_order.html',context)

@login_required(login_url='login')
def purchase_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def purchase_customer(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
        
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,CPsalutation=sal,Firstname=first,
                                    Lastname=last,CPemail=email,CPphone=mobile,
                                    CPmobile= wphone,CPskype=skname,CPdesignation=desg,
                                     CPdepartment=dept,user=u )
            ctmr.save()

        return HttpResponse({"message": "success"})

@login_required(login_url='login')
def purchase_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def payment_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.Terms + str(option.Days)

    return JsonResponse(options)

@login_required(login_url='login')
def customer_det(request):

    company= company_details.objects.get(user = request.user)
    st=company.state
    name = request.POST.get('name')
    print(name)

    vdr = customer.objects.get(user=company.user_id,customerName=name)
    email = vdr.customerEmail
    gstin = 0
    gsttr = vdr.GSTTreatment
    adres=vdr.Address2
    streat=vdr.Address1
    city=vdr.city
    state=vdr.state
    print(email)
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin,'adres':adres,'st':st,'streat':streat,'city':city,'state':state},safe=False)

    
@login_required(login_url='login')    
def vendor_det(request):

    company= company_details.objects.get(user = request.user)

    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id,first_name = fname,last_name = lname,id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    address=vdr.baddress  + '' + vdr.bcity + ''+vdr.bstate +''+vdr.bzip+''+vdr.bcountry
    print(address)
    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr,'address':address},safe=False)

    
@login_required(login_url='login')
def purchase_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit

    return JsonResponse(options)

@login_required(login_url='login')
def purchase_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        ut=request.POST['unit']
        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)

        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                    user=user,creat=history,interstate=inter,intrastate=intra)

        item.save()







        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
    
@login_required(login_url='login')    
def purchase_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)

        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        

@login_required(login_url='login')
def purchase_account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.accountName

    return JsonResponse(options)


@login_required(login_url='login')
def create_Purchase_order(request):

    company = company_details.objects.get(user = request.user)
    if request.method == 'POST':
        typ=request.POST.get('option')
        vname = request.POST.get('vendor')
        vmail = request.POST.get('email_inp')
        vgst_t = request.POST.get('gst_trt_inp')
        vgst_n = request.POST.get('gstin_inp')
            
        orgname = request.POST.get('orgName')
        org_gst = request.POST.get('gstNumber')
        org_address = request.POST.get('orgAddress')
        org_street = request.POST.get('orgstreet')
        org_city = request.POST.get('orgcity')
        org_state = request.POST.get('orgstate')
            
        cname = request.POST.get('custom')
        cmail = request.POST.get('custMail')
        caddress = request.POST.get('custAddress')
        cstreet = request.POST.get('custStreet')
        ccity = request.POST.get('custcity')
        cstate = request.POST.get('custstate')

        src_supply = request.POST.get('srcofsupply')
        po = request.POST['pur_ord']
        ref = request.POST['ref']
        terms = request.POST['terms']
        start = request.POST.get('start_date')
        end =  request.POST.get('end_date')
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        shipping_charge= request.POST['shipping_charge']
        grand_total=request.POST['grandtotal']
        note=request.POST['customer_note']
        terms_con = request.POST['tearms_conditions']
        orgMail=request.POST.get('orgMail')
        u = User.objects.get(id = request.user.id)
        print('yes')
        print(typ)
        if typ=='Organization':
           

            purchase = Purchase_Order(vendor_name=vname,
                                    vendor_mail=vmail,
                                    vendor_gst_traet=vgst_t,
                                    vendor_gst_no=vgst_n,
                                    Org_name=orgname,
                                    Org_address=org_address,
                                    Org_gst=org_gst,
                                    Org_street=org_street,
                                    Org_city=org_city,
                                    Org_state=org_state,
                                    Org_mail=orgMail,
                                    Pur_no=po,
                                    ref=ref,
                                    customer_name = '',
                                    customer_mail='',
                                    customer_address='',
                                    customer_street='',
                                    customer_city='',
                                    customer_state='',
                                    source_supply=src_supply,
                                    payment_terms = terms,
                                    Ord_date = start,
                                    exp_date = end,
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    shipping_charge = shipping_charge,
                                    grand_total=grand_total,
                                    note=note,
                                    term=terms_con,
                                    company=company,
                                    user = u,typ=typ  )
            purchase.save()

            p_bill = Purchase_Order.objects.get(id=purchase.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            purchase = Purchase_Order(vendor_name=vname,
                                    vendor_mail=vmail,
                                    vendor_gst_traet=vgst_t,
                                    vendor_gst_no=vgst_n,
                                    customer_name = cname,
                                    customer_mail=cmail,
                                    customer_street=cstreet,
                                    customer_city=ccity,
                                    customer_state=cstate,
                                    Pur_no=po,
                                    ref=ref,
                                    Org_name='',
                                    Org_address='',
                                    Org_gst='',
                                    Org_street='',
                                    Org_city='',
                                    Org_state='',
                                    Org_mail='',
                                    customer_address=caddress,
                                    source_supply=src_supply,
                                    payment_terms = terms,
                                    Ord_date = start,
                                    exp_date = end,
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    shipping_charge = shipping_charge,
                                    grand_total=grand_total,
                                    note=note,
                                    term=terms_con,
                                    company=company,
                                    user = u,typ=typ)
            purchase.save()

            p_bill = Purchase_Order.objects.get(id=purchase.id)

    
            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
            item = request.POST.getlist("item[]")
            accounts = request.POST.getlist("account[]")
            quantity = request.POST.getlist("quantity[]")
            rate = request.POST.getlist("rate[]")
            tax = request.POST.getlist("tax[]")
            discount = request.POST.getlist("discount[]")
            amount = request.POST.getlist("amount[]")
            if len(item) == len(accounts) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                for i in range(len(item)):
                    created = Purchase_Order_items.objects.create(
                        item=item[i],
                        account=accounts[i],
                        quantity=quantity[i],
                        rate=rate[i],
                        tax=tax[i],
                        discount=discount[i],
                        amount=amount[i],
                        user=u,
                        company=company,
                        PO=p_bill
                    )
                print('Done')

        return redirect('purchaseView')
    return render(request,'create_purchase_order.html')

def purchase_delet(request,id):
    po=Purchase_Order.objects.get(id=id)
    po.delete()
    return redirect('purchaseView')

    
def purchase_bill_view(request,id):
    po=Purchase_Order.objects.all()
    po_t=Purchase_Order_items.objects.filter(PO=id)
    po_table=Purchase_Order.objects.get(id=id)
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'pot':po_t,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
    }
    return render(request, 'purchase_bill_view.html',context)
    
    
def EmailAttachementView_purchase(request):

        if request.method == 'POST':
                
            subject =request.POST['subject']
            message = request.POST['message']
            email = request.POST['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, 'purchasemail.html')
            except:
               return render(request, 'purchasemail.html')

        return render(request, 'purchasemail.html')
        
        
def export_purchase_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = Purchase_Order.objects.filter(user=user)
    challan = Purchase_Order.objects.get(id=id)
    items = Purchase_Order_items.objects.filter(PO=challan)
    print(challan.customer_name) 
    print(challan.customer_name)
    total = challan.grand_total

    template_path = 'pdfchallan.html'
    context = {
        'company': company,
        'pot':challn_on,
        'po_item': challan,
        'po_table': items, 
    }
    fname=challan.Pur_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def edit(request,pk):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    po=Purchase_Order.objects.get(id=pk)
    po_tabl=Purchase_Order_items.objects.filter(PO=pk)
    context={
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'po':po,        
        'po_table':po_tabl,
        'company':company
    }
    return render(request,'edit_purchase_order.html',context)
    
    
def edit_Purchase_order(request,id):

    company = company_details.objects.get(user = request.user)
    po_id=Purchase_Order.objects.get(id=id)
    if request.method == 'POST':
        typ=request.POST['typ']
        print('yes')
        print(typ)
        if typ=='Organization':
            po_id.vendor_name = request.POST.get('vendor')
            po_id.vendor_mail = request.POST.get('email_inp')
            po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
            po_id.vendor_gst_no = request.POST.get('gstin_inp')
            po_id.typ=typ
            po_id.Org_name = request.POST.get('orgName')
            po_id.Org_address = request.POST.get('gstNumber')
            po_id.Org_gst = request.POST.get('orgAddress')

            po_id.Org_street=request.POST.get('orgstreet')
            po_id.Org_city=request.POST.get('orgcity')
            po_id.Org_state=request.POST.get('orgstate')
            po_id.Org_mail=request.POST.get('orgMail')

            po_id.customer_name = ''
            po_id.customer_mail = ''
            po_id.customer_address = ''
            po_id.customer_street = ''
            po_id.customer_city = ''
            po_id.customer_state = ''
            

            po_id.source_supply = request.POST.get('srcofsupply')
            po_id.Pur_no = request.POST['pur_ord']
            po_id.ref = request.POST['ref']
            po_id.payment_terms = request.POST['terms']
            po_id.Ord_date = request.POST.get('start_date')
            po_id.exp_date =  request.POST.get('end_date')
            po_id.sub_total =request.POST['subtotal']
            po_id.sgst=request.POST['sgst']
            po_id.cgst=request.POST['cgst']
            po_id.igst=request.POST['igst']
            po_id.tax_amount = request.POST['total_taxamount']
            po_id.shipping_charge= request.POST['shipping_charge']
            po_id.grand_total=request.POST['grandtotal']
            po_id.note=request.POST['customer_note']
            po_id.term = request.POST['tearms_conditions']
            u = User.objects.get(id = request.user.id)

            
            po_id.save()

            p_bill = Purchase_Order.objects.get(id=po_id.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            po_id.vendor_name = request.POST.get('vendor')
            po_id.vendor_mail = request.POST.get('email_inp')
            po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
            po_id.vendor_gst_no = request.POST.get('gstin_inp')
            po_id.typ=typ
            
            po_id.Org_name = ''
            po_id.Org_address = ''
            po_id.Org_gst = ''
            po_id.Org_street=''
            po_id.Org_city=''
            po_id.Org_state=''
            po_id.Org_mail=''
            po_id.customer_name = request.POST.get('custom')
            po_id.customer_mail = request.POST.get('custMail')
            po_id.customer_address = request.POST.get('custAddress')
            po_id.customer_street = request.POST.get('custstreet')
            po_id.customer_city = request.POST.get('custcity')
            po_id.customer_state = request.POST.get('custstate')

            po_id.source_supply = request.POST.get('srcofsupply')
            po_id.Pur_no = request.POST['pur_ord']
            po_id.ref = request.POST['ref']
            po_id.payment_terms = request.POST['terms']
            po_id.Ord_date = request.POST.get('start_date')
            po_id.exp_date =  request.POST.get('end_date')
            po_id.sub_total =request.POST['subtotal']
            po_id.sgst=request.POST['sgst']
            po_id.cgst=request.POST['cgst']
            po_id.igst=request.POST['igst']
            po_id.tax_amount = request.POST['total_taxamount']
            po_id.shipping_charge= request.POST['shipping_charge']
            po_id.grand_total=request.POST['grandtotal']
            po_id.note=request.POST['customer_note']
            po_id.term = request.POST['tearms_conditions']
            
            u = User.objects.get(id = request.user.id)

            
            po_id.save()

            p_bill = Purchase_Order.objects.get(id=po_id.id)

        if request.FILES.get('file') is not None:
            po_id.file = request.FILES['file']
        else:
            po_id.file = "/static/images/default.jpg"
        po_id.save()
        item = request.POST.getlist("item[]")
        accounts = request.POST.getlist("account[]")
        quantity = request.POST.getlist("quantity[]")
        rate = request.POST.getlist("rate[]")
        tax = request.POST.getlist("tax[]")
        discount = request.POST.getlist("discount[]")
        amount = request.POST.getlist("amount[]")

        obj_dele = Purchase_Order_items.objects.filter(PO=p_bill.id)
        obj_dele.delete()

        if len(item) == len(accounts) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            for i in range(len(item)):
                created = Purchase_Order_items.objects.create(
                    item=item[i],
                    account=accounts[i],
                    quantity=quantity[i],
                    rate=rate[i],
                    tax=tax[i],
                    discount=discount[i],
                    amount=amount[i],
                    user=u,
                    company=company,
                    PO=p_bill
                )

                print('Done')

            return redirect('purchase_bill_view',id)
    return redirect('purchaseView')


    
    
def change_status(request,pk):
    pur=Purchase_Order.objects.get(id=pk)
    pur.status='Approved'
    pur.save()
    return redirect('purchase_bill_view',pk)
    
def change_status_draft(request,pk):
    pur=Purchase_Order.objects.get(id=pk)
    pur.status='Draft'
    pur.save()
    return redirect('purchase_bill_view',pk)
    
def draft(request,id):
    company = company_details.objects.get(user = request.user)
    po_table=Purchase_Order.objects.all()
    po=Purchase_Order.objects.filter(status='Draft')
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
        'company':company,
    }
    return render(request,"purchase_bill_view.html",context)
    
    
def Approved(request,id):
    company = company_details.objects.get(user = request.user)
    po_table=Purchase_Order.objects.all()
    po=Purchase_Order.objects.filter(status='Approved')
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
        'company':company,
    }
    return render(request,"purchase_bill_view.html",context)
    
    
###################################################################### CHART OF ACCOUNT


def chartofaccount_home(request):
    company=company_details.objects.get(user=request.user)
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    # view=Chart_of_Account.objects.filter(user=user)
    view=Chart_of_Account.objects.all()
    return render(request,"chartofaccount_home.html", {'view':view,'company':company})

def create_account(request):
    if request.method=='POST':
        a=Chart_of_Account()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def chartofaccount_view(request,id):
    company=company_details.objects.get(user=request.user)
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    # view=Chart_of_Account.objects.filter(user=user)
    # ind=Chart_of_Account.objects.get(user=user,id=id)
    view=Chart_of_Account.objects.all()
    ind=Chart_of_Account.objects.get(id=id)

    doc=Chart_of_Account_Upload.objects.filter(account=ind)
    print(view)
    return render(request,"chartofaccount_view.html", {'view':view,'ind':ind,'doc':doc,'company':company})  

def create_account_view(request):
    if request.method=='POST':
        a=Chart_of_Account()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def edit_chart_of_account(request,pk):
    if request.method=='POST':
        a=Chart_of_Account.objects.get(id=pk)
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type1",None)
        a.account_name = request.POST.get("account_name1",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status=request.POST.get("radiobutton",None)

        if a.account_type=="Other Current Assets":        
            a.sub_account = request.POST.get("sub_account1",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account1",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Cash":        
            a.sub_account = request.POST.get("sub_account2",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account2",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Fixed Asset":        
            a.sub_account = request.POST.get("sub_account3",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account3",None)
            else:
               a.parent_account = "null"           
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Stock":        
            a.sub_account = request.POST.get("sub_account4",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account4",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Current Liability":        
            a.sub_account = request.POST.get("sub_account5",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account5",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Long Term Liability":        
            a.sub_account = request.POST.get("sub_account6",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account6",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Liability":        
            a.sub_account = request.POST.get("sub_account7",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account7",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Equity":        
            a.sub_account = request.POST.get("sub_account8",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account8",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Income":        
            a.sub_account = request.POST.get("sub_account9",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account9",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Expense":        
            a.sub_account = request.POST.get("sub_account10",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account10",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Cost Of Goods Sold":        
            a.sub_account = request.POST.get("sub_account11",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account11",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Expense":        
            a.sub_account = request.POST.get("sub_account12",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account12",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Bank":        
            a.sub_account ="null"         
            a.parent_account = "null"
            a.bank_account_no = request.POST.get("account_number")
            a.currency = request.POST.get("parent_account22")

        if a.account_type=="Credit Card":        
            a.sub_account ="null"         
            a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = request.POST.get("parent_account32")
        
        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def upload_chart_of_account(request,pk):
    if request.method=='POST':
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        account=Chart_of_Account.objects.get(id=pk)
        account_type=account.account_type
        account_name=account.account_name
        title=request.POST['file_title']
        description=request.POST['description']
        document=request.FILES.get('file')
        doc_upload=Chart_of_Account_Upload(user=user,account=account,account_type=account_type,account_name=account_name,title=title,description=description,document=document)
        doc_upload.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')

def download_chart_of_account(request,pk):
    document=get_object_or_404(Chart_of_Account_Upload,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def proj(request):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=customer.objects.all()
    print("Hello")
    print(data)
    u=User.objects.all()
    tasks=task.objects.all()
    uz=usernamez.objects.all()
    uc=usercreate.objects.all()
    company=company_details.objects.get(user=request.user)
    return render(request,'proj.html',{'data':data,'u':u,'tasks':tasks,'uz':uz,'uc':uc,'company':company})
    
def vproj(request):
   
    proj=project1.objects.filter(user=request.user)
    tsk=task.objects.all()
    active=Project.objects.all()
    company=company_details.objects.get(user=request.user)
    return render(request,'projlist.html',{'proj':proj,'tsk':tsk,'active':active,'company':company})
    
    
def addproj(request):
    if request.method == 'POST':
        user_id=request.user.id
        user=User.objects.get(id=user_id)
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        c_name = request.POST.get('c_name')
        billing = request.POST.get('billing')
        rateperhour = request.POST.get('rateperhour')
        budget = request.POST.get('budget')
        #comment=request.POST.get('comment')

        taskname1 = request.POST.getlist('taskname[]')
        print(taskname1)
        taskdes1 = request.POST.getlist('taskdes[]')
        print(taskdes1)
        taskrph1 = request.POST.getlist('taskrph[]')
        print(taskrph1)
        billable1 = request.POST.getlist('billable[]')
        print(billable1)
        user_select1 = request.POST.getlist('user_select[]')
        print(user_select1)
        email1 = request.POST.getlist('email[]')
        print(email1)

# Ensure all lists have the same length
        max_length = max(len(taskname1), len(taskdes1), len(taskrph1), len(billable1))
        taskname1.extend([''] * (max_length - len(taskname1)))
        taskdes1.extend([''] * (max_length - len(taskdes1)))
        taskrph1.extend([''] * (max_length - len(taskrph1)))
        billable1.extend(['Not Billed'] * (max_length - len(billable1)))
        

        cat = customer.objects.get(id=c_name)
        proj = project1(name=name, desc=desc, c_name=cat, billing=billing, rateperhour=rateperhour, budget=budget,user=user)
        proj.save()

        mapped_tasks = zip(taskname1, taskdes1, taskrph1, billable1)
        mapped_tasks = list(mapped_tasks)
        for ele in mapped_tasks:
            billable = 'Billed' if ele[3] == 'on' else 'Not Billed'
            tasks, created = task.objects.get_or_create(
                taskname=ele[0],
                taskdes=ele[1],
                taskrph=ele[2],
                proj=proj,
                billable=billable
            )

        mapped_users = zip(user_select1, email1)
        mapped_users = list(mapped_users)
        for elez in mapped_users:
            usrz, varez = usernamez.objects.get_or_create(
                usernamez=elez[0], emailz=elez[1], projn=proj
            )
        
    return redirect('vproj')



def overview(request,id):
    proj=project1.objects.filter(id=id)
    projc = get_object_or_404(project1, id=id)
    print(proj)
    proje=project1.objects.filter(user=request.user)
    usern=usernamez.objects.filter(projn=id)
    taskz=task.objects.filter(proj=id)
    uc=usercreate.objects.all()
    company=company_details.objects.get(user=request.user)
    project = get_object_or_404(project1, id=id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            projc.comment = comment_text  # Set the comment field of the specific project object
            projc.save()  # Save the project object with the updated comment


    return render(request,'overview.html',{'proj':proj,'proje':proje,'usern':usern,'taskz':taskz,'project':project,'projc':projc,'company':company})

# def comment(request, product_id):
#     if request.method == 'POST':
#         user = request.user
#         product = AddItem.objects.get(id=product_id)
#         new_comment = request.POST.get('comment')
        
#         # Save the new comment to the database
#         Comments_item.objects.create(item=product, user=user, content=new_comment)

#     # Retrieve all the comments for the product
#     comments = Comments_item.objects.filter(item=product_id).values_list('content', flat=True)

#     response_data = {'comments': list(comments)}
#     return JsonResponse(response_data)

    
    
def commentdb(request, pk):
    if request.method == 'POST':     
        c_user_id=request.user.id  
        c_data=User.objects.get(id=c_user_id)
        c_comment=request.POST['comment']
        c_data3=Vendor_Credits.objects.all()
        c_data2=Vendor_Credits.objects.get(id=pk)
        comments= Credits_comments_table(user=c_data,vendor=c_data2,comment=c_comment)
        Credits_comments_table.objects.filter(vendor=pk).order_by('id')
        comments.save()
        
        context = {
            "allproduct": c_data3,
            "c_data2": c_data2,
            "comments": comments,
        }
        return redirect("show_credits",pk=pk)


 

def editproj(request,id):
    proj=project1.objects.get(id=id)
    proje=project1.objects.all()
    data=customer.objects.all()
    uc=usercreate.objects.all()
    usern=usernamez.objects.filter(projn=id)
    taskz=task.objects.filter(proj=id)
    company=company_details.objects.get(user=request.user)
    return render(request,'editoverview.html',{'data':data,'proj':proj,'proje':proje,'uc':uc,'usern':usern,'taskz':taskz,'company':company})
    
    
    
def editprojdb(request,id):
  if request.method == 'POST':
        proj=project1.objects.get(id=id)
        proj.name = request.POST.get('name')
        proj.desc = request.POST.get('desc')
        proj.c_name_id = request.POST.get('c_name')
        proj.billing = request.POST.get('billing')
        proj.rateperhour = request.POST.get('rateperhour')
        proj.budget = request.POST.get('budget')

        taskname1 = request.POST.getlist('taskname[]')
        print(taskname1)
        taskdes1 = request.POST.getlist('taskdes[]')
        print(taskdes1)
        taskrph1 = request.POST.getlist('taskrph[]')
        print(taskrph1)
        billable1 = request.POST.getlist('billable[]')
        print(billable1)
        user_select1 = request.POST.getlist('user_select[]')
        print(user_select1)
        email1 = request.POST.getlist('email[]')
        print(email1)
       
        
        proj.save()

        # Delete existing usernamez objects for the project
        usernamez.objects.filter(projn=proj).delete()


        objects_to_delete = task.objects.filter(proj_id=proj.id)
        objects_to_delete.delete()

        
        mapped_tasks = zip(taskname1, taskdes1, taskrph1, billable1)
        mapped_tasks = list(mapped_tasks)
        for ele in mapped_tasks:
            billable = 'Billed' if ele[3] == 'on' else 'Not Billed'
            tasks, created = task.objects.get_or_create(
                taskname=ele[0], taskdes=ele[1], taskrph=ele[2], billable=billable, proj=proj
            )



        mapped_users = zip(user_select1, email1)
        mapped_users = list(mapped_users)
        for elez in mapped_users:
            usrz, varez = usernamez.objects.get_or_create(
                usernamez=elez[0], emailz=elez[1], projn=proj
            )

        
        return redirect('overview',id)
  
def delproj(request,id):
    projd=project1.objects.get(id=id)
    projd.delete()
    return redirect('vproj')
    
    
def itemdata2(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    
        
    item = AddItem.objects.get(Name=id)
    cus=Vendor_Credits.objects.get(company_name=cust)
    rate = item.s_price
    place=company.state
    gst = item.intrastate
    igst = item.interstate
    desc=item.s_desc
    print(place)
    mail=cus.vendor_email
    
    place_of_supply = Vendor_Credits.objects.get(company_name=cust).source_supply
    print(place_of_supply)
    return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst})
    return redirect('/')
    
    
def createuser(request):
    if request.method == 'POST':
        usernamezz = request.POST.get('usernamezz')
        emailzz = request.POST.get('emailzz')
        
        # Check if a user with the same username already exists
        existing_user = usercreate.objects.filter(usernamezz=usernamezz).first()
        
        if existing_user:
            return JsonResponse({"status": "error", "message": "User already exists"})
        else:
            proj = usercreate(usernamezz=usernamezz, emailzz=emailzz)
            proj.save()
            return JsonResponse({"status": "success", "username": usernamezz, "email": emailzz})
    
    return render(request, "proj.html")
            
            
def toggle_status(request, project_id):
    project = get_object_or_404(project1, id=project_id)
    project.active = not project.active
    project.save()
    return JsonResponse({'status': project.active})
    
    
def itemdata_challan_save(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    

    

    item = AddItem.objects.get(Name=id, user=user)
    name=item.Name
    rate = item.p_price
    place = company.state

    return JsonResponse({"status": " not", 'place': place, 'rate': rate})
    return redirect('/')


def apr(request):
    company = company_details.objects.get(user=request.user)
    pt=Purchase_Order.objects.filter(status='Approved')
    return render(request,'purchase_order.html',{'pt':pt,"company":company})


def drf(request):
    company = company_details.objects.get(user=request.user)
    pt=Purchase_Order.objects.filter(status='Draft')
    return render(request,'purchase_order.html',{'pt':pt,"company":company})


def add_customers(request):
    
    company = company_details.objects.get(user=request.user)
    sb=payment_terms.objects.all()
    hi=Pricelist.objects.all()
    return render(request,'customer.html',{'sb':sb,'hi':hi,'company':company})
    
def profileasc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    rec_bill = recurring_invoice.objects.filter(user=request.user).order_by('name')
    context = {
        'recur': rec_bill,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'viewrecurpage.html', context)
    
    
def profiledesc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user = request.user)
    rec_bill =recurring_invoice.objects.filter(user = request.user).order_by('-name')

    context = {
            'recur':rec_bill,
            'cmp1': cmp1,
            "company":company,
            }
    return render(request,'viewrecurpage.html',context)
    
    
def payment_lists(request,payment_id):
    company = company_details.objects.all()
    payment = get_object_or_404(payment_made, id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    return render(request,'payment_list.html',{'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company})
    

def payment_template(request,payment_id):
    payment = get_object_or_404(payment_made,id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    company = company_details.objects.all()
    context = {'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company}
    return render(request,'payment_template.html',context)
    
def delete_payment(request, payment_id):
   payment = payment_made.objects.filter(id=payment_id)
   payment.delete()
   return redirect('paymentmethod')
   
   
def payment_delete_details(request):
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(payment_made,id=payment_id)
    payment.delete()
    return redirect('paymentmethod')
    
def payment_details(request, payment_id):
    payment = get_object_or_404(payment_made, id=payment_id)
    vendor = vendor_table.objects.all()  # Fetch all vendor data
    bank = banking.objects.all()
    option = method.objects.all()
    company = company_details.objects.all()
    return render(request, 'payment_details_edit.html', {'payment': payment ,'vendor': vendor,'bank':bank,'option':option,'company':company})
    
    
def add_option(request):
    if request.method == "POST":
        option_name = request.POST.get('option')

        # Save the new option to the database
        new_option = method(option=option_name)
        new_option.save()
        print(option_name)

        response_data = {
            "message": "success",
            "option": option_name,
        }

        return JsonResponse(response_data)
    
    
def options(request):
    
    if not method.objects.filter(option='BOX').exists():
            method(option='BOX').save()
    if not method.objects.filter(option='UNIT').exists():
            method(option='UNIT').save()
    if not method.objects.filter(option='LITRE').exists():
            method(option='LITRE').save()
    return render(request,'payment_method_add.html')
    
    
def add_options(request):
    if request.method=='POST':
        option_name=request.POST['option']
        method(option=option_name).save()
        return redirect('payment_edit')
    return render(request,"payment_details_edit.html")
    
    
def marks(request):
    
    if not method.objects.filter(unit='Online').exists():
        method_instance = method(unit='Online')
        method_instance.save()
        
    if not method.objects.filter(unit='Cheque').exists():
        method_instance = method(unit='Cheque')
        method_instance.save()
        
    if not method.objects.filter(unit='UPI').exists():
        method_instance = method(unit='UPI')
        method_instance.save()
    return render(request,'sucess.html')
    
    
def payment_banking(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'payment_banking_add.html',{"bank":banks,"company":company})   
    
def option_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = method.objects.all()
    for option in option_objects:
        options[option.id] = option.option
    print(options)    

    return JsonResponse(options)
    
def banking_dropdown(request):

    user = User.objects.get(id=request.user.id)

    banks = {}
    bank_objects = banking.objects.all()
    for bank in bank_objects:
        banks[bank.id] = bank.bnk_name

    return JsonResponse(banks)


# def banking_dropdown(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = banking.objects.filter(user = user)
#     for option in option_objects:
        
#         options[option.id] = [ option.bnk_name, option.id]
#     return JsonResponse(options)


def added_banking(request):
  
    if request.method == "POST":
        main_name = request.POST.get('main_name')
        alias = request.POST.get('main_alias')
        acunt_type = request.POST.get('main_type')
        ac_holder = request.POST.get('ac_holder')
        ac_number = request.POST.get('ac_number')
        ifsc = request.POST.get('ifsc')
        sw_code = request.POST.get('sw_code')
        bnk_name = request.POST.get('bnk_name')
        br_name = request.POST.get('br_name')
        chqrng = request.POST.get('alter_chq')
        chqprnt = request.POST.get('en_chq')
        chqprnty = request.POST.get('chq_prnt')
        name = request.POST.get('name')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        bnk_det = request.POST.get('bnk_det')
        pan = request.POST.get('pan')
        regtype = request.POST.get('register_type')
        gstin = request.POST.get('gstin')
        gst_det = request.POST.get('gst_det')
        balance = request.POST.get('balance')

        
        u = User.objects.get(id = request.user.id)

       
        data = banking(
            name=main_name,
            alias=alias,
            acc_type=acunt_type,
            ac_holder=ac_holder,
            ac_no=ac_number,
            ifsc=ifsc,
            swift_code=sw_code,
            bnk_name=bnk_name,
            bnk_branch=br_name,
            chq_book=chqrng,
            chq_print=chqprnt,
            chq_config=chqprnty,
            mail_name=name,
            mail_addr=address,
            mail_country=country,
            mail_state=state,
            mail_pin=pin,
            bd_bnk_det=bnk_det,
            bd_pan_no=pan,
            bd_reg_typ=regtype,
            bd_gst_no=gstin,
            bd_gst_det=gst_det,
            opening_bal=balance,
            user=u
        )
        data.save()
        response_data = {
            "message": "success",
            "bnk_nm":bnk_name,
            
        }

        return JsonResponse(response_data)
    
    
def payment_banking_edit(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'payment_banking_edit.html',{"bank":banks,"company":company})  
    
    
def added_banking_edit(request):
    if request.method == "POST":
        a=banking()
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.user=request.user
        a.opening_bal = request.POST.get('balance',None)
        a.save()
        return redirect("payment_edit") 
    
    
@login_required(login_url='login')
def delete_comment(request, product_id, comment_id):
    try:
        comment = Comments_item.objects.get(id=comment_id, item_id=product_id, user=request.user)
        comment.delete()
    except Comments_item.DoesNotExist:
        pass

    return redirect('detail', product_id)
    
    
def save_bank_payment(request):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect('paymentadd_method')
        
        
def payroll_create(request):
    company=company_details.objects.get(user=request.user)
    return render(request,'payroll_create.html',{'company':company})
    
    
def editpayroll(request,id):
    p=Payroll.objects.get(id=id)
    
    if request.method=='POST':
        p.title=request.POST['title']
        p.first_name=request.POST['fname']
        p.last_name=request.POST['lname']
        p.alias=request.POST['alias']
        p.joindate=request.POST['joindate']
        p.salary=request.POST['salary']   
        # p.image=request.FILES.get('file')
        new=request.FILES.get('file')
        old= p.image
        if old!=None and new==None:
            p.image=old
        else:
            p.image=new
        p.emp_number = request.POST['empnum']
        p.designation = request.POST['designation']
        p.location=request.POST['location']
        p.gender=request.POST['gender']
        p.dob=request.POST['dob']
        p.blood=request.POST['blood']
        p.parent=request.POST['fm_name']
        p.spouse_name=request.POST['s_name']  
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+" "+padd2      
        p.address=address 
        p.permanent_address=paddress 
        p.Phone=request.POST['phone']
        ephone=request.POST['ephone']
        if ephone =="":
            p.emergency_phone=None
        else:
            p.emergency_phone=request.POST['ephone']
        p.email=request.POST['email']
        p.ITN=request.POST['itn']
        p.Aadhar=request.POST['an']
        p.UAN=request.POST['uan']
        p.PFN=request.POST['pfn']
        p.PRAN=request.POST['pran']
        istds=request.POST['istds']
        if istds == '1':
            p.isTDS=request.POST['pora']
            p.TDS=request.POST['tds']
        else:
            p.isTDS='No'
            p.TDS=0
        p.save()
        
        if Bankdetails.objects.filter(payroll=p).exists():
            b=Bankdetails.objects.get(payroll=p)
            b.acc_no=request.POST['acc_no']  
            b.IFSC=request.POST['ifsc']
            b.bank_name=request.POST['b_name']
            b.branch=request.POST['branch']
            b.transaction_type=request.POST['ttype']
            b.save()
        else:
            bank=request.POST['bank']
            if(bank == '1'):
                accno=request.POST['acc_no']       
                ifsc=request.POST['ifsc']       
                bname=request.POST['b_name']       
                branch=request.POST['branch']
                ttype=request.POST['ttype']
                b=Bankdetails(payroll=p,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
                b.save()
        
    else:
        return redirect('payroll_view',id=id)
    return redirect('payroll_view',id=id)

def createpayroll(request):
    if request.method=='POST':
        title=request.POST['title']
        fname=request.POST['fname']
        lname=request.POST['lname']
        alias=request.POST['alias']
        joindate=request.POST['joindate']
        saltype=request.POST['saltype']
        if (saltype == 'Fixed'):
            salary=request.POST['fsalary']
        else:
            salary=request.POST['vsalary']
        image=request.FILES.get('file')
        if image == None:
            image="image/img.png"
        empnum=request.POST['empnum']
        designation = request.POST['designation']
        location=request.POST['location']
        gender=request.POST['gender']
        dob=request.POST['dob']
        blood=request.POST['blood']
        fmname=request.POST['fm_name']
        sname=request.POST['s_name']        
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+padd2
        phone=request.POST['phone']
        ephn=request.POST['ephone']
        if ephn=="":
            ephone=None
        else:
            ephone=request.POST['ephone']
        email=request.POST['email']
        isdts=request.POST['tds']
        if isdts == '1':
            istdsval=request.POST['pora']
            if istdsval == 'Percentage':
                tds=request.POST['pcnt']
            elif istdsval == 'Amount':
                tds=request.POST['amnt']
        else:
            istdsval='No'
            tds = 0
        itn=request.POST['itn']
        an=request.POST['an']        
        uan=request.POST['uan'] 
        pfn=request.POST['pfn']
        pran=request.POST['pran']
        payroll= Payroll(title=title,first_name=fname,last_name=lname,alias=alias,image=image,joindate=joindate,salary_type=saltype,salary=salary,emp_number=empnum,designation=designation,location=location,
                         gender=gender,dob=dob,blood=blood,parent=fmname,spouse_name=sname,address=address,permanent_address=paddress ,Phone=phone,emergency_phone=ephone,
                         email=email,ITN=itn,Aadhar=an,UAN=uan,PFN=pfn,PRAN=pran,isTDS=istdsval,TDS=tds)
        payroll.save()

        bank=request.POST['bank']
        if(bank == '1'):
            accno=request.POST['acc_no']       
            ifsc=request.POST['ifsc']       
            bname=request.POST['b_name']       
            branch=request.POST['branch']
            ttype=request.POST['ttype']
            b=Bankdetails(payroll=payroll,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
            b.save()
        attach=request.FILES.get('attach')       
        if(attach):
            att=Payrollfiles(attachment=attach,payroll=payroll)
        # messages.success(request,'Saved succefully !')
        print(bank)
        return redirect('payroll_list')
    else:
        return redirect('payroll_create')
        
        
def payroll_list(request):
    company=company_details.objects.get(user=request.user)
    p=Payroll.objects.all()
    return render(request,'payroll_list.html',{'pay':p,'company':company})
    
    
def payroll_delete(request,pid):
    p=Payroll.objects.get(id=pid)
    p.delete()
    return redirect('payroll_list')
    
    
def payroll_view(request,id):
    payroll=Payroll.objects.all()
    p=Payroll.objects.get(id=id)
    com=Commentmodel.objects.filter(payroll=p)
    b=Bankdetails.objects.filter(payroll=p)
    attach=Payrollfiles.objects.filter(payroll=p)
    company=company_details.objects.get(user=request.user)
    print(p)
    print(attach)
    return render(request,'payroll_view.html',{'pay':payroll,'p':p,'b':b,'com':com,'attach':attach,'company':company})

def payroll_active(request,id):
    p=Payroll.objects.get(id=id)
    if p.status == 'Active':
        p.status = 'Inactive'
    else:
        p.status = 'Active'
    p.save()
    return redirect('payroll_view',id=id)

def payroll_file(request,id):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        pay=Payroll.objects.get(id=id)
        p=Payrollfiles(attachment=uploaded_file,payroll=pay)
        p.save()
        print("hellooooooooooooooooo")
        return redirect('payroll_view',id)
    else:
        return redirect('payroll_view',id)
    # 

def img_download(request,id):
    p=Payroll.objects.get(id=id)
    image_file = p.image

    response = FileResponse(image_file)
    response['Content-Disposition'] = f'attachment; filename="{image_file.name}"'
    # return redirect('payroll_view',id=id)
    return response
    
    
def file_download(request,aid):
    att= Payrollfiles.objects.get(id=aid)
    file = att.attachment
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response
    
    
def payroll_edit(request,pid):  
    p=Payroll.objects.get(id=pid)
    company=company_details.objects.get(user=request.user)
    address=p.address
    paddress=p.permanent_address
    add1, add2 = split_paragraph(address)
    padd1, padd2 = split_paragraph(paddress)
    b=Bankdetails.objects.filter(payroll=p)
    print(b)
    context = {
                'add1' : add1,
                'add2' : add2, 'padd1' : padd1, 'padd2': padd2,
                'pay':p,'b':b,'company':company
            }
    return render(request,'payroll_edit.html',context)

def add_payrollcomment(request,pid):
    p=Payroll.objects.get(id=pid)
    if request.method== 'POST':
        comment=request.POST['comments']
        c= Commentmodel(comment=comment,payroll=p)
        c.save()
    return redirect('payroll_view',id=pid)
    
    
def delete_payrollcomment(request,cid):
    
    try:
        comment = Commentmodel.objects.get(id=cid)
        p=comment.payroll
        print("================================")
        comment.delete()
        return redirect('payroll_view', p.id)
    except:
        return redirect('payroll_view', p.id)
        
        
def projcomment(request,id):
    proj = project1.objects.get(id=id)
    proje=project1.objects.filter(user=request.user)
    return render(request,'comment.html',{'proj':proj,'proje':proje})
    
    
def projcommentdb(request, id):
    projc = get_object_or_404(project1, id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            if projc.comment:
                projc.comment += "\n" + comment_text  # Add new comment to existing comments
            else:
                projc.comment = comment_text  # If no comments exist, set it as the first comment
            projc.save()

    return redirect('overview', id=id)
    
    
    
def entr_custmrA1(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('email')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('v_gsttype')
            gstin=request.POST.get('v_gstin')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,
                          customerType=type,
                        companyName=cpname,
                        customerEmail=email,
                        customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,
                         designation=desg,department=dept,
                           website=wbsite
                           ,GSTTreatment=gstt,
                           GSTIN=gstin,
                           placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,
                             PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,
                                Facebook=fbk,
                                Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("proj")
        return render(request,'customerzz.html')
        
        
def payment_termA1(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return HttpResponse( {"message":"success"})
        
        
def add_customers1(request):
    sb=payment_terms.objects.all()
    hi=Pricelist.objects.all()
    return render(request,'customerzz.html',{'sb':sb,'hi':hi})
    
    
#####################expense##############################################################
    
def expensepage(request):
    company = company_details.objects.get(user = request.user)
    expenses = ExpenseE.objects.filter(user=request.user)
    context = {
        'expenses': expenses,
        'company':company
       }
    return render(request,'expense.html',context)

def save_expense(request):
    company = company_details.objects.get(user = request.user)
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            date = request.POST.get('date')
            
           
            expense_account = request.POST.get('expense_account')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            expense_type = request.POST.get('expense_type')
            paid = request.POST.get('paid')

            notes = request.POST.get('notes')
            if request.POST.get('expense_type') == 'goods':
                hsn_code = request.POST.get('sac')
                sac = request.POST.get('hsn_code')
            else:
                hsn_code = request.POST.get('hsn_code')
                sac = request.POST.get('sac')
    
            gst_treatment = request.POST.get('gst_treatment')
            gstin=request.POST.get('gstin',None)
            destination_of_supply = request.POST.get('destination_of_supply')
            reverse_charge = request.POST.get('reverse_charge')
            tax = request.POST.get('tax')
            invoice = request.POST.get('invoice')
            c = request.POST.get('customer')
            customere = customer.objects.get(id=c)
            v= request.POST.get('vendor')
            vendor=vendor_table.objects.get(id=v)

          
            taxamt = request.POST.get('taxamt',False)
           
            image = request.FILES.get('image')


            expense = ExpenseE.objects.create(
                user=request.user,
                date=date,
                image=image,
                expense_account=expense_account,
                amount=amount,
                currency=currency,
                taxamt=taxamt,
                sac=sac,
                expense_type=expense_type,
                paid=paid,
                notes=notes,
                hsn_code=hsn_code,
                gst_treatment=gst_treatment,
                gstin=gstin,
                destination_of_supply=destination_of_supply,
                reverse_charge=reverse_charge,
                tax=tax,
                invoice=invoice,
                customer_name= customere,
                vendor=vendor,
                company=company
            )

            expense.save()

            return redirect('expensepage')
        else:
          
            c = customer.objects.filter(user=request.user)
            v = vendor_table.objects.filter(user=request.user)
            accounts = AccountE.objects.filter(user=request.user)
            account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
            p = payment_termsE.objects.filter(user=request.user)
            cp= company_details.objects.get(user = request.user)
            return render(request, 'addexpense.html', {'company':cp,'vendor':v,'customer': c,'payments':p,'accounts': accounts, 'account_types': account_types,
            })
   
def upload_documents(request, expense_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        expense = ExpenseE.objects.get(id=expense_id)
        attachment_file = request.FILES.get('attachment')

        doc_data = AttachE.objects.create(user=user, expense=expense, attachment=attachment_file)
        doc_data.save()

        return redirect("expense_details", pk=expense.pk)
   
def upload_documents(request, expense_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        expense = ExpenseE.objects.get(id=expense_id)
        attachment_file = request.FILES.get('attachment')

        doc_data = AttachE.objects.create(user=user, expense=expense, attachment=attachment_file)
        doc_data.save()

        return redirect("expense_details", pk=expense.pk)

def add_accountE(request):
    accounts = AccountE.objects.filter(user=request.user)
    account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
    if request.method=='POST':
        a=AccountE()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
       
        a.save()
       
        
    return HttpResponse('Account saved successfully')
    return render(request, 'addexpense.html', {
        'accounts': accounts,
        'account_types': account_types,
    })

def account_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    account_objects = AccountE.objects.filter(user=user)
    for account in account_objects:
        
        options[account.id] = {
            'account_name': account.account_name,
            'account_type': account.account_type
        }

    return JsonResponse(options)  
       



def add_custmr(request):
    
    # company = ExpenseE.objects.get(user = request.user)
    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)
        if balance == '':
           balance = None

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country, fax = fax, phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
def customer_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user=user)
    for option in option_objects:
        display_name = option.customerName
        options[option.id] = [display_name, f"{display_name}"]
        
    return JsonResponse(options)

        
# def customer_dropdownE(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = addcustomerE.objects.filter(user = user)
#     for option in option_objects:
#         options[option.id] = [option.customer_name]


#     return JsonResponse(options)        
        
        
def edit_expensee(request,expense_id):
    company = company_details.objects.get(user = request.user)
    if request.user.is_authenticated:
        expense = ExpenseE.objects.get(id=expense_id)

        if request.method == 'POST':
            date = request.POST.get('date')
            expense_account = request.POST.get('expense_account')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            expense_type = request.POST.get('expense_type')
            paid = request.POST.get('paid')
            notes = request.POST.get('notes')
            if request.POST.get('expense_type') == 'goods':
                hsn_code = request.POST.get('sac')
                sac = request.POST.get('hsn_code')
            else:
                hsn_code = request.POST.get('hsn_code')
                sac = request.POST.get('sac')
            gst_treatment = request.POST.get('gst_treatment')
            destination_of_supply = request.POST.get('destination_of_supply')
           
            tax = request.POST.get('tax')
            invoice = request.POST.get('invoice')
            c = request.POST.get('customer')
            customere = customer.objects.get(id=c)
            v = request.POST.get('vendor')
            vendor = vendor_table.objects.get(id=v)
            reporting_tags = request.POST.get('reporting_tags')
            taxamt = request.POST.get('taxamt', False)
           
            reverse_charge = request.POST.get('reverse_charge')
            if reverse_charge == 'True':
                expense.reverse_charge = True
            else:
                expense.reverse_charge = False

            gstin = request.POST.get('gstin', None)
            if gstin is not None:
                expense.gstin = gstin
            else:
                expense.gstin = None

            if request.FILES.get('image'):
                image = request.FILES['image']
            elif expense.image:
                image = expense.image
            else:
                image = None

            expense.date = date
            expense.expense_account = expense_account
            expense.amount = amount
            expense.currency = currency
            expense.taxamt = taxamt
            expense.sac = sac
            expense.expense_type = expense_type
            expense.paid = paid
            expense.notes = notes
            expense.hsn_code = hsn_code
            expense.gst_treatment = gst_treatment
            expense.gstin=gstin
            expense.destination_of_supply = destination_of_supply
            expense.reverse_charge = reverse_charge
            expense.tax = tax
            expense.invoice = invoice
            expense.customer_name = customere
            expense.reporting_tags = reporting_tags
            expense.vendor = vendor
            expense.image=image
            
            expense.company=company
            expense.save()

            return redirect('expense_details',pk=expense.pk)
        else:
           
            c = customer.objects.filter(user=request.user)
            v = vendor_table.objects.filter(user=request.user)
            accounts = AccountE.objects.filter(user=request.user)
            account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
            p = payment_termsE.objects.filter(user=request.user)
            cp= company_details.objects.get(user = request.user)
            return render(request, 'editexpense.html', {'company':cp ,'vendor': v, 'customer': c, 'accounts': accounts, 'account_types': account_types, 'expense': expense})

def delet(request,id):
    items=ExpenseE.objects.filter(id=id)
    items.delete()
    
    return redirect('expensepage')



    
def add_vendore(request):
    
    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email',None)
        website=request.POST.get('website',None)
        w_mobile=request.POST.get('work_mobile',None)
        p_mobile=request.POST.get('pers_mobile',None)
        skype = request.POST.get('skype',None)
        desg = request.POST.get('desg',None)
        dpt = request.POST.get('dpt',None)
        gsttype=request.POST.get('gsttype',None)
        gstin=request.POST.get('gstin',None)
        panno=request.POST.get('panno',None)
        supply=request.POST.get('sourceofsupply',None)
        currency=request.POST.get('currency',None)
        balance=request.POST.get('openingbalance',None)
        payment=request.POST.get('paymentterms',None)
        street=request.POST.get('street',None)
        city=request.POST.get('city',None)
        state=request.POST.get('state',None)
        pincode=request.POST.get('pincode',None)
        country=request.POST.get('country',None)
        fax=request.POST.get('fax',None)
        phone=request.POST.get('phone',None)
        shipstreet=request.POST.get('shipstreet',None)
        shipcity=request.POST.get('shipcity',None)
        shipstate=request.POST.get('shipstate',None)
        shippincode=request.POST.get('shippincode',None)
        shipcountry=request.POST.get('shipcountry',None)
        shipfax=request.POST.get('shipfax',None)
        shipphone=request.POST.get('shipphone',None)
        
        u = User.objects.get(id = request.user.id)
        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse("success")

# def vendor_dropdownE(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = vendor_tableE.objects.filter(user=user)
#     for option in option_objects:
#         # options[option.id] = [option.first_name + " " + option.last_name, option.first_name + " " + option.last_name + " " + str(option.id)]
#         display_name = f"{option.salutation} {option.first_name} {option.last_name}"
#         options[option.id] = [display_name, display_name + " " + str(option.id)]
#         # options[option.id] = display_name
#     return JsonResponse(options)

def vendor_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user=user)
    for option in option_objects:
        display_name = f"{option.salutation} {option.first_name} {option.last_name}"
        options[option.id] = [display_name, display_name]
    return JsonResponse(options)
    
    
def deletefile(request,aid):
    att=Payrollfiles.objects.get(id=aid)
    p=att.payroll
    att.delete()
    return redirect('payroll_view',p.id)
    
    
def project_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def customer_dropdown_proj(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.id , option.customerName]

    return JsonResponse(options) 
    
    
def recurbills_payzzz(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        name = request.POST.get('name')
        days = request.POST.get('days')

        # Create a new payment_terms object and save it to the database
        payment_term = payment_terms(Terms=name, Days=days)
        payment_term.save()

        # Return a JSON response indicating success
        return JsonResponse({"message": "success"})
        
        
def split_paragraph(paragraph):
    if paragraph is None:
        return '',''
    else:
        words = paragraph.split()
        total_words = len(words)
        midpoint = None
        for i in range(total_words):
            if i > total_words // 2 and words[i].isalpha():
                midpoint = i
                break
        if midpoint is None:
            # If no suitable midpoint found, split at the actual midpoint
            midpoint = total_words // 2
    
        first_half = ' '.join(words[:midpoint])
        second_half = ' '.join(words[midpoint:])
        return first_half, second_half
    
    
def filter_by_draft(request):
    user = request.user
    estimates=Estimates.objects.filter(status='draft',user=user)
    return render(request, 'all_estimates.html', {'estimates':estimates})
    
    
def filter_by_sent(request):
    user = request.user
    estimates=Estimates.objects.filter(status='sent',user=user)
    return render(request, 'all_estimates.html', {'estimates':estimates})
    
    
def filter_by_draft_estimate_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user,status='draft')
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'estimate_slip.html', context)
    
    
def filter_by_sent_estimate_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user,status='sent')
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'estimate_slip.html', context)
    
    
def add_est_comment(request,pk):
    if request.method=="POST":
        user=request.user      
        estimate=Estimates.objects.get(id=pk)
       
        comment=estimate_comments()
        comment.user=user
        comment.estimate=estimate
        comment.comments=request.POST.get('comments')
       
        comment.save()
    return redirect('estimateslip',estimate.id)
    
    
###########Report############
def report_inventory_view(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'reports_inventory.html',{'company':company})
    
    
def report_view(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'reports.html',{'company':company})

def inventory_summary(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    return render(request,'inventory_summary.html',{'company':company,'item':item})


def custom_repot(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'custom_report_inventory.html',{'company':company,'items':item})

def inventory_Valuation_summary(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'inventory-valuation.html',{'company':company,'item':item})


def custom_valuation_repot(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'custom-valuation-report.html',{'company':company,'items':item})


def show_hide(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'show_hide.html',{'company':company})

def general(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'custom-valuation-report.html',{'company':company})
    
    
#Abin - Vendor Credits

@login_required(login_url='login')
def vendor_credits_home(request):

    company = company_details.objects.get(user = request.user)
    recur = Vendor_Credits_Bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        

    sorted_recur = sorted(recur, key=lambda r: r['vendor_name'],reverse=True) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'vendor_credits_home.html',context)
    
    

def getitems2(request):
    cmp1 = request.user
    id=request.GET.get('id')
    print(id)
    data=AddItem.objects.get(Name=id,user_id=cmp1)
    print(data)
    price=data.s_price
    return JsonResponse({"price":price})
    
    
def vendor_credits(request):
    c = customer.objects.all()
    p = AddItem.objects.all()
    i = invoice.objects.all()
    pay = payment_terms.objects.all()

    if request.user.is_authenticated:
        vendors = vendor_table.objects.all()
        if request.method == 'POST':
            # c=request.POST['cx_name']
            # cus=customer.objects.get(customerName=c) 
            # print(cus.id)  
            # custo=cus.id
            company_name = request.POST.get('sel')
            vendor_email = request.POST.get('email')
            baddress = request.POST.get('address')
            gst_treatment = request.POST.get('gst')
            source_supply = request.POST.get('placeofsupply')
            credit_note = request.POST.get('credit_note')
            order_no = request.POST.get('order_number')
            vendor_date = request.POST.get('credit_date')
            cxnote = request.POST['customer_note']
            subtotal = request.POST['subtotal']
            igst = request.POST['igst']
            cgst = request.POST['cgst']
            sgst = request.POST['sgst']
            adjustment = request.POST['adjustment_charge']
            totaltax = request.POST['totaltax']
            t_total = request.POST['t_total']

            file = request.FILES['file'] if 'file' in request.FILES else "/static/images/alt.jpg"
            # tc = request.POST['ter_cond']
            status = request.POST['sd']
            if status == 'draft':
                print(status)
            else:
                print(status)

            product = request.POST.getlist('item[]')
            hsn = request.POST.getlist('hsn[]')           
            quantity = request.POST.getlist('quantity[]')          
            rate = request.POST.getlist('rate[]')           
            discount = request.POST.getlist('desc[]')           
            tax = request.POST.getlist('tax[]')     
                 
            total = request.POST.getlist('amount[]')
            print(total)

            inv = Vendor_Credits.objects.create(
                
                user=request.user,
                # customer_id=custo,
                company_name=company_name,
                vendor_email=vendor_email,
                baddress=baddress,
                credit_note=credit_note,
                gst_treatment=gst_treatment,
                source_supply=source_supply,
                order_no=order_no,
                vendor_date=vendor_date,
                cgst=cgst,
                sgst=sgst,
                adjustment=adjustment,
                cxnote=cxnote,
                subtotal=subtotal,
                igst=igst,
                t_tax=totaltax,
                grandtotal=t_total,
                status=status,
                file=file
            )
            inv.save()
            inv_id=Vendor_Credits.objects.get(id=inv.id)

            if len(product) == len(hsn) == len(quantity) == len(discount) == len(tax) == len(total) == len(rate):
                
                mapped = zip(product, hsn, quantity, discount, tax, total, rate)
                mapped = list(mapped)
            
                for element in mapped:
                    created = Vendor_invoice_item.objects.create(
                        inv=inv_id,
                        product=element[0],
                        hsn=element[1],
                        quantity=element[2],
                        discount=element[3],
                        tax=element[4],
                        total=element[5],
                        rate=element[6]
                    )
                    created.save()
            return redirect('vendor_credits_home')

    context = {
        'c': c,
        'p': p,
        'i': i,
        'pay': pay,
        'vendors': vendors,
    }

    return render(request, 'vendor_credits.html', context)
    
    
def show_credits(request, pk):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=Vendor_Credits.objects.filter(user=udata)
    vcredit=Vendor_Credits.objects.get(id=pk)
    mdata=Credits_mail_table.objects.filter(vendor=pk)
    ddata=Credits_doc_upload_table.objects.filter(user=udata,vendor=vcredit)

    cdata = Credits_comments_table.objects.filter(vendor=vcredit).order_by('-id')
    # comment = Credits_comments_table.objects.filter(vendor=pk).order_by('id')
    return render(request,'show_credit.html',{'vdata':vdata1,'vcredit':vcredit,'mdata':mdata,'ddata':ddata,'cdata':cdata})
    
    
@login_required(login_url='login')
def delete_comment_credit(request, pk,vid):
    comment = Credits_comments_table.objects.get(id=pk)
    comment.delete()

    return redirect('show_credits',pk=vid)
    
    
def credit_sendmail(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata2=Vendor_Credits.objects.get(id=pk)
        mail_from=settings.EMAIL_HOST_USER
        mail_to=request.POST['email']
        subject=request.POST['subject']
        content=request.POST['content']
        mail_data=Credits_mail_table(user=udata,vendor=vdata2,mail_from=mail_from,mail_to=mail_to,subject=subject,content=content)
        mail_data.save()

        subject = request.POST['subject']
        message = request.POST['content']
        recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

        return redirect("vendor_credits_home")
        
        
def credit_upload_document(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata=Vendor_Credits.objects.get(id=pk)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=Credits_doc_upload_table(user=udata,vendor=vdata,title=title,document=document)
        doc_data.save()
        return redirect("vendor_credits_home")
        
        
def credit_download_doc(request,pk):
    document=get_object_or_404(Credits_doc_upload_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response
    
    
def credit_delete_vendor(request,pk):
    if Credits_comments_table.objects.filter(vendor=pk).exists():
        user2=Credits_comments_table.objects.filter(vendor=pk)
        user2.delete()
    if Credits_mail_table.objects.filter(vendor=pk).exists():
        user3=Credits_mail_table.objects.filter(vendor=pk)
        user3.delete()
    if Credits_doc_upload_table.objects.filter(vendor=pk).exists():
        user4=Credits_doc_upload_table.objects.filter(vendor=pk)
        user4.delete()

    
    user1=Vendor_Credits.objects.get(id=pk)
    user1.delete()
    return redirect("vendor_credits_home")
    
    
def edit_vendor_credits(request,id):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    po=Vendor_Credits_Bills.objects.get(id=id)
    po_tabl=Vendor_Credits_Bills_items_bills.objects.filter(recur_bills=id)
    context={
        'company' : company,
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'po':po,        
        'po_table':po_tabl,
    }
    return render(request,'edit_vendor_credits.html',context)
    
    
def credits_statement(request,id):
    sales=Vendor_Credits.objects.get(id=id)
    saleitem=Vendor_invoice_item.objects.filter(inv_id=id)
    sale_order=Vendor_Credits.objects.all()
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'sale':sales,
        'saleitem':saleitem,
        'sale_order':sale_order,
        'comp':company,
        'vendor':vendor,
        
        
                    }
    return render(request,'vender_credit_state.html',context)
    
    
def add_customer_for_vcredit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            
            salutation=request.POST['salutation']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            company_name=request.POST['company_name']
            vendor_display_name=request.POST['v_display_name']
            vendor_email=request.POST['vendor_email']
            vendor_wphone=request.POST['w_phone']
            vendor_mphone=request.POST['m_phone']
            skype_number=request.POST['skype_number']
            designation=request.POST['designation']
            department=request.POST['department']
            website=request.POST['website']
            gst_treatment=request.POST['gst']
            
            gst_number=request.POST['gst_number']
            pan_number=request.POST['pan_number']
            
            source_supply=request.POST['source_supply']
            currency=request.POST['currency']
            opening_bal=request.POST['opening_bal']
            payment_terms=request.POST['payment_terms']
            
            battention=request.POST['battention']
            bcountry=request.POST['bcountry']
            baddress=request.POST['baddress']
            bcity=request.POST['bcity']
            bstate=request.POST['bstate']
            bzip=request.POST['bzip']
            bphone=request.POST['bphone']
            bfax=request.POST['bfax']
        

          
           
            u = User.objects.get(id = request.user.id)

          
            ctmr=vendor_table(salutation=salutation,first_name=first_name,
                        last_name=last_name,company_name=company_name,vendor_display_name=vendor_display_name,
                         vendor_email=vendor_email,vendor_wphone=vendor_wphone,vendor_mphone=vendor_mphone,
                           skype_number=skype_number,designation=designation,department=department, website=website,
                             gst_treatment=gst_treatment,gst_number=gst_number,pan_number=pan_number,
                                source_supply=source_supply,currency=currency,opening_bal=opening_bal,payment_terms=payment_terms,baddress=baddress,
                                 battention=battention,bcountry=bcountry,bcity=bcity,bstate=bstate,
                                  bzip=bzip,bphone=bphone,bfax=bfax,user=u )
            ctmr.save()  
            
            return redirect("vendor_credits")
        return render(request,"add_vendor_vcredits.html",)
        
        
def additem_vendor_page(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'add_vendor_credit_items.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })
                            
                            
                            
def additem_vendor_credit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("vendor_credits")
    return render(request,'add_vendor_credit_items.html')
    
def poject_itemz(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(usercreate, usernamezz=user_id)
    email = user.emailzz
    return JsonResponse({'email': email})
    
def report(request):
  return render(request, 'reports.html')

def fifo_cost(request):
    company = company_details.objects.get(user = request.user)
    return render(request, 'fifo_cost.html', {'company': company})

def product_sales(request):
    company = company_details.objects.get(user = request.user)
    return render(request, 'product_sales.html', {'company': company})

def show_customize_product(request):
    general = "url1"
    show = "url2"
    
    company = company_details.objects.get(user = request.user)
    
    context = {
        'url1' : general,
        'url2' : show,
        'company': company,
    }
    return render(request, 'customize_show_product.html', context)

def product_customize(request):
    general = "url1"
    show = "url2"
    
    items = AddItem.objects.all()
    company = company_details.objects.get(user = request.user)
    
    context = {
        'url1' : general,
        'url2' : show,
        'item' : items,
        'company': company,
    }
    return render(request, 'customize_product.html', context)

def customize_fifo(request):
    items = AddItem.objects.all()
    company = company_details.objects.get(user = request.user)
    context = {
        'item': items,
        'company': company,
        }
    return render(request, 'customize_fifo.html', context)
    
    
    
#-----------bills-----sumayya------------------------------------------------------------------------------------------------

def view_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('-id')
    company = company_details.objects.get(user=user)
    context = {
        'bills': bills,
        'company': company,
    }

    return render(request, 'viewbills.html', context)


def new_bill(request):
    user = request.user
    company = company_details.objects.get(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    vendors = vendor_table.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    terms = payment_terms.objects.all()
    units = Unit.objects.all()
    account = Chart_of_Account.objects.all()
    account_types = Chart_of_Account.objects.values_list('account_type', flat=True).distinct()
    sales_acc = Sales.objects.all()
    pur_acc = Purchase.objects.all()
    last_id = PurchaseBills.objects.filter(user_id=user.id).order_by('-id').values('id').first()
    if last_id:
        last_id = last_id['id']
        next_no = last_id+1
    else:
        next_no = 1
    context = {'company': company,
               'items': items,
               'vendors': vendors,
               'customers': customers,
               'terms': terms,
               'units': units,
               'b_no': next_no,
               'acc': account,
               'acc_types':account_types,
               's_acc': sales_acc,
               'p_acc': pur_acc,
               }

    return render(request, 'newbill.html',context)

def get_customer_data_bill(request):
    user = request.user
    name = request.GET.get('id')
    print(name)
    custobject = customer.objects.get(customerName=name, user=user)
    email = custobject.customerEmail
    pos = custobject.placeofsupply
    print(email)
    print(pos)
    return JsonResponse({"status": " not", 'email': email, 'pos': pos})
    return redirect('/')

def get_vendor_data_bill(request):
    user = request.user
    name = request.GET.get('id')
    first_name, last_name = name.split(' ')
    print(name)
    print(first_name)
    print(last_name)
    vendorobject = vendor_table.objects.get(first_name=first_name, last_name=last_name)
    email = vendorobject.vendor_email
    sos = vendorobject.source_supply
    print(email)
    print(sos)
    return JsonResponse({"status": " not", 'email': email, 'sos': sos})
    return redirect('/')

@login_required(login_url='login')
def add_vendor_bills(request):
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        fullname = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        s_supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vend = vendor_table(user = u,salutation=title,first_name=first_name,last_name=last_name,company_name=comp_name,vendor_display_name=fullname,
                            vendor_email=email,vendor_wphone=w_mobile,vendor_mphone=p_mobile,skype_number=skype,designation=desg,
                            department=dpt,website=website,gst_treatment=gsttype,gst_number=gstin,pan_number=panno,source_supply=s_supply,
                            currency=currency,opening_bal=balance,payment_terms=payment,bcountry=country,baddress=street,bcity=city,
                            bstate=state,bphone=phone,bfax=fax,scountry=shipcountry,saddress=shipstreet,scity=shipcity,
                            sstate=shipstate,sphone=shipphone,sfax=shipfax)
        vend.save()

        response_data = {
            "message": "success",
            "fullname":fullname,
            "email": email,
            "sos": s_supply,
            "gstin": gstin
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def entr_custmr_for_bills(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        response_data = {
            "message": "success",
            "name":name,
            "email": email,
            "pos": supply
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def create_account_bills(request):
    u = User.objects.get(id = request.user.id)
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        type=request.POST.get('type')
        name=request.POST.get('name')

        u = User.objects.get(id = request.user.id)

        acc = Chart_of_Account(account_type=type,account_name=name,user = u)
        acc.save()

        response_data = {
            "message": "success",
            "name":name,
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def create_payment_terms_bills(request):
    u = User.objects.get(id = request.user.id)
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        t_name=request.POST.get('name')
        t_days=request.POST.get('days')

        u = User.objects.get(id = request.user.id)

        term = payment_terms(Terms=t_name,Days=t_days)
        term.save()

        response_data = {
            "message": "success",
            "t_name":t_name,
        }

        return JsonResponse(response_data)
    
def additem_bills(request):
    
    radio=request.GET.get('radios')
    inter=request.GET.get('inters')
    intra=request.GET.get('intras')
    type=request.GET.get('types')
    name=request.GET.get('names')
    unit=request.GET.get('units')
    sel_price=request.GET.get('sel_prices')
    sel_acc=request.GET.get('sel_accs')
    s_desc=request.GET.get('s_descs')
    cost_price=request.GET.get('cost_prices')
    cost_acc=request.GET.get('cost_accs')      
    p_desc=request.GET.get('p_descs')
    u=request.user.id
    us=request.user
    history="Created by" + str(us)
    user=User.objects.get(id=u)
    unit=Unit.objects.get(id=unit)
    sel=Sales.objects.get(id=sel_acc)
    cost=Purchase.objects.get(id=cost_acc)
    ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                    )
    ad_item.save()

    return JsonResponse({"status": " not", 'name': name})

def itemdata_bills(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    print(id)
    print(cust)

    item = AddItem.objects.get(Name=id, user=user)

    rate = item.p_price
    return JsonResponse({"status": " not", 'rate': rate})
    return redirect('/')

def create_purchase_bill(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        vendor_email = request.POST['vendor_email']
        sos = request.POST['sos']
        cust_name = request.POST['customer_name']
        cust_email = request.POST['customer_email']
        pos = request.POST['pos']
        bill_number = request.POST['bill_number']
        order_number = request.POST['order_number']
        bill_date = request.POST['bill_date']
        due_date = request.POST['due_date']
        terms = request.POST['p_terms']

        item = request.POST.getlist('item[]')
        account = request.POST.getlist('account[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        # cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        discount = request.POST['discount_amnt']
        total = request.POST['total']
        # tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Draft'

        bill = PurchaseBills(user=user, customer_name=cust_name,customer_email= cust_email,place_of_supply=pos,vendor_name=vendor_name,
                             vendor_email=vendor_email,source_of_supply=sos,bill_no=bill_number, order_number=order_number, bill_date=bill_date, 
                             due_date=due_date,payment_terms=terms, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, 
                             shipping_charge=shipping,discount=discount, total=total, status=status,attachment=attachment)
        bill.save()

        if len(item) == len(quantity) == len(rate) == len(account) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, account, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], account=element[3], tax_percentage=element[4], amount=element[5])
    return redirect('view_bills')


def create_purchase_bill1(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        vendor_email = request.POST['vendor_email']
        vendor_gst = request.POST['gst_no']
        sos = request.POST['sos']
        cust_name = request.POST['customer_name']
        cust_email = request.POST['customer_email']
        pos = request.POST['pos']
        bill_number = request.POST['bill_number']
        order_number = request.POST['order_number']
        bill_date = request.POST['bill_date']
        due_date = request.POST['due_date']
        terms = request.POST['p_terms']

        item = request.POST.getlist('item[]')
        account = request.POST.getlist('account[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        # cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        discount = request.POST['discount_amnt']
        total = request.POST['total']
        # tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Save'

        bill = PurchaseBills(user=user, customer_name=cust_name,customer_email= cust_email,place_of_supply=pos,vendor_name=vendor_name,
                             vendor_email=vendor_email,vendor_gst_no=vendor_gst,source_of_supply=sos,bill_no=bill_number, order_number=order_number, bill_date=bill_date, 
                             due_date=due_date,payment_terms=terms, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, 
                             shipping_charge=shipping,discount=discount, total=total, status=status,attachment=attachment)
        bill.save()

        if len(item) == len(quantity) == len(rate) == len(account) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, account, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], account=element[3], tax_percentage=element[4], amount=element[5])
    return redirect('view_bills')



def bill_view(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user=user)
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
    }
    return render(request, 'bill_slip.html', context)

def add_comment_bills(request,bill_id):
    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=bill_id) 
        bill.comments = request.POST['comment']
        bill.save()
        return redirect('bill_view',b_id = bill_id)
    



def edit_bill(request,bill_id):
    user = request.user
    company = company_details.objects.get(user=user)
    customers = customer.objects.filter(user_id=user.id)
    vendors = vendor_table.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    bill = PurchaseBills.objects.get(id=bill_id)
    bill_items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    terms = payment_terms.objects.all()
    account = Chart_of_Account.objects.all()
    account_types = Chart_of_Account.objects.values_list('account_type', flat=True).distinct()
    sales_acc = Sales.objects.all()
    pur_acc = Purchase.objects.all()
    context = {
        'company': company,
        'bill': bill,
        'customers': customers,
        'items': items,
        'bill_items': bill_items,
        'vendors': vendors,
        'terms': terms,
        'acc': account,
        'acc_types':account_types,
        's_acc': sales_acc,
        'p_acc': pur_acc,
    }
    return render(request, 'edit_bill.html', context)

def update_bills(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=pk)
        bill.user = user
        bill.vendor_name = request.POST['vendor_name']
        bill.vendor_email = request.POST['vendor_email']
        bill.source_of_supply = request.POST['sos']
        bill.customer_name = request.POST['customer_name']
        bill.customer_email = request.POST['customer_email']
        bill.place_of_supply = request.POST['pos']
        bill.bill_no = request.POST['bill_number']
        bill.order_number = request.POST['order_number']
        bill.bill_date = request.POST['bill_date']
        bill.due_date = request.POST['due_date']
        bill.payment_terms = request.POST['p_terms']

        bill.sub_total = request.POST['subtotal']
        bill.igst = request.POST['igst']
        bill.sgst = request.POST['sgst']
        bill.cgst = request.POST['cgst']
        bill.tax_amount = request.POST['total_taxamount']
        bill.shipping_charge = request.POST['shipping_charge']
        bill.discount = request.POST['discount_amnt']
        bill.total = request.POST['total']
        bill.status = 'Draft'

        old=bill.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            bill.attachment = old
        else:
            bill.attachment = new

        bill.save()

        item = request.POST.getlist('item[]')
        account = request.POST.getlist('account[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')

       
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        objects_to_delete = PurchaseBillItems.objects.filter(purchase_bill_id=bill.id)
        objects_to_delete.delete()

        
        if len(item) == len(quantity) == len(rate) == len(account) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, account, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], account=element[3], tax_percentage=element[4], amount=element[5])
    return redirect('bill_view',b_id = bill.id)

def upload_file_bills(request,bill_id):
    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=bill_id) 
        bill.attachment = request.FILES.get('file')
        bill.save()
        return redirect('bill_view',b_id = bill_id)

def delete_bill(request,bill_id):
    bill = PurchaseBills.objects.get(id = bill_id)
    bill.delete()
    return redirect('view_bills')

def search_bill(request):
    if request.method == "POST":
        user = request.user
        company = company_details.objects.get(user=user)
        search = request.POST['search']
        cloumn = request.POST['type']

        if cloumn == '1' or search  == '':
            return redirect('view_bills')    

        else :
            if cloumn == '2':
                bills = PurchaseBills.objects.filter(user=user,customer_name=search).all()

                context = {
                    'bills': bills,
                    'company': company,
                }

                return render(request, 'viewbills.html', context)

            else:
                if cloumn == '3':
                    bills = PurchaseBills.objects.filter(user=user,bill_no=search).all()

                    context = {
                        'bills': bills,
                        'company': company,
                    }

                    return render(request, 'viewbills.html', context)       
   
    
    return redirect('view_bills')
    
    
@login_required(login_url='login')    
def expense_pay(request):
    
    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_termsE(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def pay_dropdownE(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_termsE.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.Terms]

    return JsonResponse(options)   
    
    
# def get_vendor_gst_treatment(request):
#     v_user = request.user
#     user = User.objects.get(id=v_user.id)
  
#     vendor = request.GET.get('vendor')
#     vendor = vendor_tableE.objects.get(vendor_display_name=vendor, user=user)
#     gst_treatment = vendor.gst_treatment
   
#     return JsonResponse({'gst_treatment':gst_treatment})
# def get_vendor_gst_treatment(request):
#     v_user = request.user
#     user = User.objects.get(id=v_user.id)

#     vendor_name = request.GET.get('vendor') 
#     try:
#         vendor = vendor_tableE.objects.get(vendor_display_name=vendor_name, user=user)
#         gst_treatment = vendor.gst_treatment
#     except vendor_tableE.DoesNotExist:
#         gst_treatment = None

#     print(f"Vendor Name: {vendor_name}, GST Treatment: {gst_treatment}")

#     return JsonResponse({'gst_treatment': gst_treatment})


def get_vendor_gst_treatment(request):
    v_user = request.user
    user = User.objects.get(id=v_user.id)

    vendor_name = request.GET.get('vendor') 
    if vendor_name: 
        try:
            vendor = vendor_table.objects.get(id=vendor_name, user=user)
            gst_treatment = vendor.gst_treatment
            gstin = vendor.gst_number  
        except vendor_table.DoesNotExist:
            gst_treatment = None
            gstin = None

        print(f"Vendor Name: {vendor_name}, GST Treatment: {gst_treatment}, GSTIN: {gstin}")

        return JsonResponse({'gst_treatment': gst_treatment, 'gstin': gstin})
    else:
     
        return JsonResponse({'gst_treatment': None, 'gstin': None})
    
    
def get_company_state(request):
    user = request.user
    try:
        company = company_details.objects.get(user=user)
        state = company.state
    except company_details.DoesNotExist:
        state = None
    print("Fetched State:", state)
    return JsonResponse({"state": state})
    
def reports(request):
    return render(request,'reports.html') 
    
    
def salesby_customer(request):
    customer1 = customer.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request, 'salesby_customer.html', {'cust': customer1, 'company_data': company_data})
    
    
def customize_report(request):
    company_data = company_details.objects.get(user=request.user)

    return render(request, 'customize_report.html',{'company_data': company_data})

    return render(request, 'customize_report.html',{'company_data': company_data})
    
def general_customize(request):
    return render(request,'general_customize.html') 
    
def salesby_item(request):
    items = AddItem.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request, 'salesby_item.html', {'items': items, 'company_data': company_data})
    
def customize_report1(request):
    company_data = company_details.objects.get(user=request.user)
    items = AddItem.objects.all()
    customers = customer.objects.all()
    available_columns = ["Sales(FCY)", "Sales with Tax", "Company Name", "First Name", "Last Name", "Website",
                         "Customer Email", "Mobile Phone", "WorkPhone", "Department", "Designation"]
    
    context = {
        "available_columns": available_columns,
    }
    return render(request, 'customize_report1.html', {'items': items, 'customers': customers,'company_data': company_data})
    
    
def customerAtoZ_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('customer_name')
    company = company_details.objects.get(user=user)
    context = {
        'bills': bills,
        'company': company,
    }

    return render(request, 'viewbills.html', context)
    
def vendorAtoZ_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('vendor_name')
    company = company_details.objects.get(user=user)
    context = {
        'bills': bills,
        'company': company,
    }

    return render(request, 'viewbills.html', context)
    
    
def sendmails(request,id):
    if request.method=='POST':
       user_id=request.user.id
       udata=User.objects.get(id=user_id)
       cdata2=customer.objects.get(id=id)
       mail_from=settings.EMAIL_HOST_USER
       mail_to=request.POST['sendto']
       subject=request.POST['subject']
       content=request.POST['messag']
       mail_data=customer_mail_table(user=udata,customr=cdata2,mail_from=mail_from,mail_to=mail_to,subject=subject,content=content)
       mail_data.save()
       #----------------------------------------------
       subject=request.POST['subject']
       messag=request.POST['messag']
       sendto=request.POST['sendto']
       send_mail(subject,messag,settings.EMAIL_HOST_USER,
                 [sendto],fail_silently=False)
       return redirect('view_customr')
       
       
def cust_comments(request,id):
    if request.method=='POST':
       user_id=request.user.id
       udata=User.objects.get(id=user_id)
       cdata2=customer.objects.get(id=id)
       comment=request.POST['comments']
       cmts=customer_comments_table(user=udata,customr=cdata2,comment=comment)
       cmts.save()
       return redirect('view_customr')
       
def cust_Attach_files(request,id):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        cdata2=customer.objects.get(id=id)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=customer_doc_upload_table(user=udata,customr=cdata2,title=title,document=document)
        doc_data.save()
        return redirect('view_customr')
        
def sales_order(request):
    company = company_details.objects.get(user = request.user)
    data = SalesOrder.objects.all()
    return render(request, 'sales_order.html', {'data':data, 'company': company})
    
    
def sales_summery(request):
    company = company_details.objects.get(user = request.user)
    data = AddItem.objects.all()
    
    return render(request, 'sales_summery.html', {'data':data, 'company': company})
    
    
def transaction(request, pk):
    product = AddItem.objects.get(id = pk)
    company = company_details.objects.get(user = request.user)
    
    items=AddItem.objects.all()
    
    estimate = EstimateItems.objects.filter(item_name = product.Name)
    sales_order = sales_item.objects.filter(product = product.Name)
    recurring_invoice = recur_itemtable.objects.filter(iname = product.Name)
    purchase_order = Purchase_Order_items.objects.filter(item = product.Name)
    recurring_bills = recurring_bills_items.objects.filter(item = product.Name)
    invoice = invoice_item.objects.filter(product = product.Name)
    deliveryChellan = ChallanItems.objects.filter(item_name = product.Name)
    bills = PurchaseBillItems.objects.filter(item_name = product.Name)
    expense = Expense.objects.filter(goods_label = product.Name)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    
    context = {
        'allproduct': items,
        'product': product,
        'company': company,
        
        'estimate': estimate,
        'sales_order': sales_order,
        'recurring_invoice': recurring_invoice,
        'purchase_order': purchase_order,
        'recurring_bills': recurring_bills,
        'invoice': invoice,
        'deliveryChellan': deliveryChellan,
        'bills': bills,
        'expense': expense,
        'stock': stock,
    }
    
    return render(request, 'transactions.html', context)
    
    
login_required(login_url='login')
def view_sales_order_all(request):
    sales=SalesOrder.objects.all()
    return render(request,'view_sales_order.html',{"sale":sales})   
    
login_required(login_url='login')
def view_sales_order_Draft(request):
    sales=SalesOrder.objects.filter(status="draft")
    return render(request,'view_sales_order.html',{"sale":sales}) 
    
login_required(login_url='login')
def view_sales_order_approved(request):
    sales=SalesOrder.objects.filter(status="Approved")
    return render(request,'view_sales_order.html',{"sale":sales}) 

@login_required(login_url='login')
def customer_dropdown_sales(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.customerName]

    return JsonResponse(options)
    
    
def gstr2_load(request):
    company = company_details.objects.get(user=request.user)
    purchase= PurchaseBills.objects.all()
    purchaseItem=PurchaseBillItems.objects.all()
    recur_bills=recurring_bills.objects.all()
    recur_add_bills=recurring_bills_items.objects.all()
  
   
    context={'company':company,'purchase':purchase,'purchases':purchaseItem,'recur_bills':recur_bills,'recur_add_bills':recur_add_bills}
    return render(request,'GSTR_2.html',context)
    
def sales_by_hsn_load(request):
     company = company_details.objects.get(user=request.user)
    #  item = AddItem.objects.all()
     invoices=invoice.objects.all()
     invoice_items = invoice_item.objects.all()
 
     return render(request,'sales_by_hsn.html',{'company':company,'invoice':invoices,'invoice_item':invoice_items})
     
     
def export_sales_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    sales = SalesOrder.objects.get(id=id)
    items = sales_item.objects.filter(sale_id=id)
    

    template_path = 'pdfsales.html'
    context = {
        'company': company,
        'sale':sales,
        'item':items,
        
    }
    fname=sales.sales_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
    
#---------------------shamreena---GSTR1 & GSTR_3B

def GSTR_3Bpage(request):
    company = company_details.objects.get(user=request.user)
    context={
       
        'company':company
    }
    return render(request,'GSTR_3B2.html',context)
    
def GSTR_1page(request):
    company = company_details.objects.get(user=request.user)
    data=invoice.objects.all()
    invoices=recurring_invoice.objects.all()
    reinv=RetainerInvoice.objects.all()
    context={
        'invoices':invoices,
        'data':data,
        'reinv':reinv,
        'company':company
    }
    return render(request,'gstr1_s2.html', context)
    
    
def change_vendor_status(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    vdata=vendor_table.objects.get(id=pk)
    if vdata.status == 'Active':
        vdata.status = 'Inactive'
        vdata.save()
    else:
        vdata.status = 'Active'
        vdata.save()
    return redirect('view_vendor_details',pk=vdata.id)
    
    
#Reshna-banking

def bank_home(request):
    cp= company_details.objects.get(user = request.user)
    banks= Bankcreation.objects.filter(user=request.user)
    bank_balances = []
    for bank in banks:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
   
    
    return render(request, 'bank_home.html', {'company': cp,'bank_balances': bank_balances})

def create_bank(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            date = request.POST.get('date')
            name = request.POST.get('name')
            opn_bal = float(request.POST.get('opn_bal', 0.0))
            bal_type=request.POST.get('bal_type')
            branch= request.POST.get('branch')
            ac_no= request.POST.get('ac_no')
            ifsc=request.POST.get('ifsc')
            if bal_type == 'Credit':
                opn_bal = -opn_bal
            else:
                opn_bal = opn_bal


            bank = Bankcreation.objects.create(
                user=request.user,
                name=name,
                opn_bal=opn_bal,
                bal_type=bal_type,
                branch=branch,
                ac_no=ac_no,
                ifsc=ifsc,
                date=date
              
            )

            bank.save()
            banka = Bankcreation.objects.get(id=bank.id)

            if len(request.FILES) != 0:
                banka.document=request.FILES['file'] 
                banka.save()

            return redirect('bank_home')
        else:
          
          
            cp= company_details.objects.get(user = request.user)
            return render(request, 'addbank.html', {'company':cp})

def edit_bank(request,bank_id):
    if request.user.is_authenticated:
        bank = Bankcreation.objects.get(id=bank_id,user=request.user)
        if request.method == 'POST':
            bank.name = request.POST.get('name')
            bank.opn_bal = float(request.POST.get('opn_bal', 0.0))
            bank.bal_type = request.POST.get('bal_type')
            if bank.bal_type == 'Credit':
                bank.opn_bal = -bank.opn_bal
            else: 
                bank.opn_bal = bank.opn_bal
            
           
            bank.date = request.POST.get('date')
            print(type(bank.date))
            bank.branch = request.POST.get('branch')
            bank.ac_no = request.POST.get('ac_no')
            bank.ifsc = request.POST.get('ifsc')
            bank.save()
            return redirect('bank_listout',id=bank_id)
        else:
          
          
            cp= company_details.objects.get(user = request.user)
            return render(request, 'editbank.html', {'company':cp,'bank': bank})

def delete_bank(request, bank_id):
    if request.user.is_authenticated:
        bank = Bankcreation.objects.get(id=bank_id, user=request.user)
        bank.delete()
    return redirect('bank_home')  

# def bank_listout(request,id):
#     cp= company_details.objects.get(user = request.user)
#     bank= Bankcreation.objects.filter(user=request.user)
#     banks =get_object_or_404(Bankcreation, id=id)      
#     bankc=transactions.objects.filter(user=request.user,bank=banks)
#     bank_balance = sum([transaction.amount for transaction in bankc])
#     bank_balances = []
#     for bank in bank:
#         transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
#         balance = sum([transaction.amount for transaction in transactions_for_bank])
#         bank_balances.append((bank, balance))

#     return render(request,'banklistout.html', {'company':cp, 'bank':bank ,'banks':banks,'bankc':bankc,'bank_balance':bank_balance,'bank_balances': bank_balances})   

def bank_listout(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)

    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))

    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})


def banktocash(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date = request.POST.get('date')
            fromB = request.POST.get('fromB')
            toB = request.POST.get('toB')
            amount = float(request.POST.get('amount', 0.0))
            description = request.POST.get('description')
            type = request.POST.get('type')
            adjtype = request.POST.get('adjtype') 
            adjacname = request.POST.get('adjacname')
            bank = Bankcreation.objects.get(id=id)

            if type == 'Cash To Bank Transfer':
                to_bank = Bankcreation.objects.get(id=toB)
                cash_to_banktransaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    toB=toB,
                    amount=amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=to_bank
                )
               
                cash_to_banktransaction.save()

            if type == 'Adjust Bank Balance':
                if adjtype == 'Reduce Balance':
                    amount = -amount
                else:
                    amount=amount
                ad_bank = Bankcreation.objects.get(id=adjacname)
                adj_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    adjacname=adjacname,
                    description=description,
                    date=date,
                    adjtype=adjtype,
                    type=type,
                    bank=ad_bank,
                    amount=amount
                )
                
                
                adj_transaction.save()

            if type == 'Bank To Cash Transfer':
                from_bankB = Bankcreation.objects.get(id=fromB)
                bank_to_cash_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    toB=toB,
                    amount=-amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=from_bankB
                )
               
                bank_to_cash_transaction.save()
                
            if type == 'Bank To Bank Transfer':
                from_bank = Bankcreation.objects.get(id=fromB)
                to_bank = Bankcreation.objects.get(id=toB)
                from_bank_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=from_bank.name,
                    toB=to_bank.name,
                    amount=-amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=from_bank
                )
                
                from_bank_transaction.save()

               
                to_bank_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=from_bank.name,
                    toB=to_bank.name,
                    amount=amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=to_bank
                )
               
                to_bank_transaction.save()

            return redirect('bank_listout', id=id)
        else:
            b = Bankcreation.objects.filter(user=request.user)
            cp = company_details.objects.get(user=request.user)
            return render(request, 'banklistout.html', {'company': cp, 'bank': b})


def bank_attachfile(request,id):

    company = company_details.objects.get(user = request.user)
    bank = Bankcreation.objects.get(user = request.user,id=id)
    print(bank)

    if request.method == 'POST':

        bank.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bank.document = request.FILES['file']

        bank.save()
        return redirect('bank_listout',id=id)

def nameasc(request):
    cp = company_details.objects.get(user = request.user)
    bank =Bankcreation.objects.filter(user = request.user).order_by('name')
    print(bank)
    bank_balances = []
    for bank in bank:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
    return render(request, 'bank_home.html', {'company': cp, 'bank_balances': bank_balances})

def namedes(request):
    cp = company_details.objects.get(user = request.user)
    bank =Bankcreation.objects.filter(user = request.user).order_by('-name')
    print(bank)
    bank_balances = []
    for bank in bank:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
    return render(request, 'bank_home.html', {'company': cp, 'bank_balances': bank_balances})

def view_nameasc(request,id):
    cp = company_details.objects.get(user = request.user)
    banks_list =Bankcreation.objects.filter(user = request.user).order_by('name')
    print(banks_list)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})

def view_namedes(request,id):
    cp = company_details.objects.get(user = request.user)
    banks_list =Bankcreation.objects.filter(user = request.user).order_by('-name')
    print(banks_list)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    return render(request, 'banklistout.html', {'bankcompany': cp,'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank,})

def bank_status(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)

    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    # if request.method == 'POST':
        selected_bank = get_object_or_404(Bankcreation, id=id)
        # new_status = request.POST.get('action')
        # selected_bank.status = new_status
        if selected_bank.status == 'Active':
            selected_bank.status = 'Inactive'
        else:
            selected_bank.status = 'Active'
        selected_bank.save()
        # selected_bank.save()

        # return JsonResponse({'message': 'Status updated successfully'})
    
    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})

def bank_pdf(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'banklistout.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    context = {
    'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 
    'bank_balance': bank_balance, 'bank_balances': bank_balances ,
    'transactions_for_selected_bank':transactions_for_selected_bank
    }
    html = template.render(Context(context))

    fname = selected_bank.name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={fname}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response
        
        
@login_required(login_url='login')
def vendor_credit_dropdown(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user = user)
    for option in option_objects:
        
        options[option.id] = [option.salutation, option.first_name, option.last_name, option.id]
    return JsonResponse(options)
    
    
@login_required(login_url='login')
def vendor_credit_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        hsn=request.POST['hsn']
        ut=request.POST['unit']
        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)

        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,hsn=hsn,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                    user=user,creat=history,interstate=inter,intrastate=intra)

        item.save()


        return HttpResponse({"message": "success"})
    
@login_required(login_url='login')
def vendor_credit_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
    
    
@login_required(login_url='login')
def get_vendor_credit_det(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id, id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    baddress = vdr.baddress

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr, 'baddress' : baddress},safe=False)
    
    
@login_required(login_url='login')
def get_vendor_credit_det1(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    # name = request.POST.get('id')
    full_name = request.POST.get('id')
    first_name, last_name = full_name.split() if full_name else ('', '')
    print(first_name)
    print(last_name)


    vdr = vendor_table.objects.get(user=company.user_id, first_name=first_name,last_name=last_name)
    
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    baddress = vdr.baddress

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr, 'vendor_name' : baddress},safe=False)
    
@login_required(login_url='login')
def view_vendor_credits(request,id):

    company = company_details.objects.get(user = request.user)
    bills = Vendor_Credits_Bills.objects.filter(user = request.user)
    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)
    
    #cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    # vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    #cust_name = cust.customerName
    # vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                #'customer' : cust,
                # 'vendor' : vend,
                #'customer_name' : cust_name,
                # 'vendor_name' : vend_name,
            }

    return render(request, 'view_vendor_credits.html',context)
    
@login_required(login_url='login')
def vendor_credit_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        r_bill = Vendor_Credits_Bills.objects.get(user = request.user, id = id)
        r_bill.comments = cmnt
        r_bill.save()

        return redirect('vendor_credits_home',id)
    return redirect('vendor_credits_home')
    
@login_required(login_url='login')
def vendor_credit_add_file(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)
    print(bill)

    if request.method == 'POST':

        bill.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bill.document = request.FILES['file']

        bill.save()
        return redirect('view_recurring_bills',id)
        
        
def vendor_credit_email(request,id):

    company = company_details.objects.get(user = request.user)
    bill = Vendor_Credits_Bills.objects.get(user = request.user,id=id)

    if request.method == 'POST':

        recipient =request.POST.get('recipient')
        sender =request.POST.get('sender')
        sub =request.POST.get('subject')
        message =request.POST.get('message')

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'view_vendor_credits.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()
        

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    if template:
        prntonly_content = str(template)

    # print(prntonly_content)
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
        temp_file.write(prntonly_content.encode('utf-8'))

    with open(temp_file.name, 'rb') as attachment_file:
        attachment_content = attachment_file.read()

    email = EmailMessage(
        subject=sub,
        body=message,
        from_email=sender,
        to=[recipient],
    )
    email.attach('Recurring Bill',attachment_content , 'text/html')

    email.send()
     
    return HttpResponse(status=200)
    
@login_required(login_url='login')
def vc_view_vendorasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =Vendor_Credits_Bills.objects.filter(user = request.user).order_by('company_name')

    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    # cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                # 'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def vc_view_vendordesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =Vendor_Credits_Bills.objects.filter(user = request.user).order_by('-vendor_name')

    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    # cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                # 'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def delete_vendor_credits(request, id):

    company = company_details.objects.get(user = request.user)
    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    rbill.delete() 
    billitem.delete() 
     
    return redirect('vendor_credits_home')
    
def add_vendor_credits(request):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    context={
        'company' : company,
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        
    }
        
    return render(request,'create_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def create_vendor_credit(request):

    company = company_details.objects.get(user = request.user)
    if request.method == 'POST':
        typ=request.POST.get('option')
        vname = request.POST.get('vendor')
        vmail = request.POST.get('email_inp')
        vgst_t = request.POST.get('gst_trt_inp')
        vgst_n = request.POST.get('gstin_inp')
        vaddress = request.POST.get('address_inp')
        
        credit_note = request.POST.get('credit_note')
        order_no = request.POST.get('order_number')
        vendor_date = request.POST.get('credit_date')

        src_supply = request.POST.get('srcofsupply')
     
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        adjustment= request.POST['shipping_charge']
        # adjustment=request.POST['adjustment_charge']
        grand_total=request.POST['grandtotal']
        note=request.POST['customer_note']
      
        u = User.objects.get(id = request.user.id)
        print('yes')
        print(typ)
        if typ=='Organization':
           

            purchase = Vendor_Credits_Bills(vendor_name=vname,
                                    vendor_email=vmail,
                                    gst_treatment=vgst_t,
                                    gst_number=vgst_n,
                                    address=vaddress,
                                        
                                    vendor_date=vendor_date,
                                    order_no=order_no,
                                    credit_note=credit_note,
                             
                                    source_supply=src_supply,
                                      
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                     
                                    adjustment=adjustment,
                                    grand_total=grand_total,
                                    note=note,
                                   
                                    company=company,
                                    user = u )
            purchase.save()

            p_bill = Vendor_Credits_Bills.objects.get(id=purchase.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            purchase = Vendor_Credits_Bills(vendor_name=vname,
                                    vendor_email=vmail,
                                    gst_treatment=vgst_t,
                                    gst_number=vgst_n,
                                    address=vaddress,
                                        
                                    vendor_date=vendor_date,
                                    order_no=order_no,
                                    credit_note=credit_note,
                              
                                    source_supply=src_supply,
                                  
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    
                                    adjustment=adjustment,
                                    grand_total=grand_total,
                                    note=note,
                                        # term=terms_con,
                                    company=company,
                                    user = u)
            purchase.save()

            p_bill = Vendor_Credits_Bills.objects.get(id=purchase.id)

        
            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
            item = request.POST.getlist("item[]")
            accounts = request.POST.getlist("account[]")
            hsn = request.POST.getlist("hsn[]")
            quantity = request.POST.getlist("quantity[]")
            rate = request.POST.getlist("rate[]")
            tax = request.POST.getlist("tax[]")
            discount = request.POST.getlist("discount[]")
            amount = request.POST.getlist("amount[]")
            if len(item) == len(accounts) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                for i in range(len(item)):
                    created = Vendor_Credits_Bills_items_bills.objects.create(
                        item=item[i],
                        account=accounts[i],
                        
                        hsn=hsn[i],
                        quantity=quantity[i],
                        rate=rate[i],
                        tax=tax[i],
                        discount=discount[i],
                        amount=amount[i],
                        user=u,
                        company=company,
                        recur_bills=p_bill
                    )
                print('Done')

        return redirect('vendor_credits_home')
    return render(request,'create_vendor_credits.html')
    
    
def change_vendor_credits(request,id):

    company = company_details.objects.get(user = request.user)
    po_id=Vendor_Credits_Bills.objects.get(id=id)
    if request.method == 'POST':
    
        po_id.vendor_name = request.POST.get('vendor')
        po_id.vendor_mail = request.POST.get('email_inp')
        po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
        po_id.vendor_gst_no = request.POST.get('gstin_inp')
            
        po_id.vaddress = request.POST.get('address_inp')       
        po_id.credit_note = request.POST.get('credit_note')
        po_id.order_no = request.POST.get('order_number')
        po_id.vendor_date = request.POST.get('credit_date')

        po_id.source_supply = request.POST.get('srcofsupply')

        po_id.sub_total =request.POST['subtotal']
        po_id.sgst=request.POST['sgst']
        po_id.cgst=request.POST['cgst']
        po_id.igst=request.POST['igst']
        po_id.tax_amount = request.POST['total_taxamount']
        po_id.grand_total=request.POST['grandtotal']
        po_id.note=request.POST['customer_note']
        # po_id.adjustment=request.POST['add_round_off']
        po_id.adjustment=request.POST['shipping_charge']
        
        u = User.objects.get(id = request.user.id)

            
        po_id.save()

        p_bill = Vendor_Credits_Bills.objects.get(id=po_id.id)

        if len(request.FILES) != 0:
            p_bill.document=request.FILES['file'] 
            p_bill.save()
            print('save')
    else:
        po_id.vendor_name = request.POST.get('vendor')
        po_id.vendor_mail = request.POST.get('email_inp')
        po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
        po_id.vendor_gst_no = request.POST.get('gstin_inp')
            
        po_id.vaddress = request.POST.get('address_inp')       
        po_id.credit_note = request.POST.get('credit_note')
        po_id.order_no = request.POST.get('order_number')
        po_id.vendor_date = request.POST.get('credit_date')
        po_id.source_supply = request.POST.get('srcofsupply')
        po_id.sub_total =request.POST['subtotal']
        po_id.sgst=request.POST['sgst']
        po_id.cgst=request.POST['cgst']
        po_id.igst=request.POST['igst']
        po_id.tax_amount = request.POST['total_taxamount']
        po_id.grand_total=request.POST['grandtotal']
        po_id.note=request.POST['customer_note']
        # po_id.adjustment=request.POST['add_round_off']
        po_id.adjustment=request.POST['shipping_charge']
            
        u = User.objects.get(id = request.user.id)

            
        po_id.save()

        p_bill = Vendor_Credits_Bills.objects.get(id=po_id.id)

    if request.FILES.get('file') is not None:
        po_id.file = request.FILES['file']
    else:
        po_id.file = "/static/images/default.jpg"
    po_id.save()
    item = request.POST.getlist("item[]")
    accounts = request.POST.getlist("account[]")
    hsn = request.POST.getlist("hsn[]")
    quantity = request.POST.getlist("quantity[]")
    rate = request.POST.getlist("rate[]")
    tax = request.POST.getlist("tax[]")
    discount = request.POST.getlist("discount[]")
    amount = request.POST.getlist("amount[]")

    obj_dele = Vendor_Credits_Bills_items_bills.objects.filter(recur_bills=p_bill.id)
    obj_dele.delete()

    if len(item) == len(accounts) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
        for i in range(len(item)):
            created = Vendor_Credits_Bills_items_bills.objects.create(
                item=item[i],
                account=accounts[i],
                hsn=hsn[i],
                quantity=quantity[i],
                rate=rate[i],
                tax=tax[i],
                discount=discount[i],
                amount=amount[i],
                user=u,
                company=company,
                recur_bills=p_bill
            )

            print('Done')

        return redirect('view_vendor_credits',id)
    return redirect('vendor_credits_home')
    
    
@login_required(login_url='login')
def vendor_credits_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
    
@login_required(login_url='login')
def vendor_credits_pay_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.Terms + str(option.Days)

    return JsonResponse(options)

@login_required(login_url='login')
def vendor_credits_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def vendor_credits_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit

    return JsonResponse(options)

@login_required(login_url='login')    
def vendor_credits_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)

        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        

@login_required(login_url='login')
def vendor_credits_account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.accountName

    return JsonResponse(options)

def export_vendor_credit_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = Vendor_Credits_Bills.objects.filter(user=user)
    challan = Vendor_Credits_Bills.objects.get(id=id)
    items = Vendor_Credits_Bills_items_bills.objects.filter(PO=challan)
    print(challan.customer_name) 
    print(challan.customer_name)
    total = challan.grand_total

    template_path = 'pdfchallan.html'
    context = {
        'company': company,
        'pot':challn_on,
        'po_item': challan,
        'po_table': items, 
    }
    fname=challan.Pur_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
def itemdata_vendor_credit(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    

    

    item = AddItem.objects.get(Name=id, user=user)
    name=item.Name
    rate = item.p_price
    hsn = item.hsn
    place = company.state

    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'hsn': hsn})
    return redirect('/')
    
    
@login_required(login_url='login')
def vendor_credit_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
        
############### BALANCE SHEET ################## 
def load_balance_sheet(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'balance_sheet.html', {"company":company})
    
def load_customize_report_bs(request):
    return render(request,'customize_report_bs.html', {"range":range(2,24)})
    
def update_balancesheet(request):
    if request.method=='POST':
        newdate= request.POST.get('newdate', False)
        return render(request,'balance_sheet.html', {"range":range(2,24),"newdate":newdate[4:],"valid":1})
    
############### HORIZONTAL BALANCE SHEET ################## 
def load_horizontal_balance_sheet(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'horizontal_balance_sheet.html', {"company":company})
    
def load_customize_report_hbs(request):
    return render(request,'customize_report_hbs.html')
    
def update_hbalancesheet(request):
    if request.method=='POST':
        newdate= request.POST.get('newdate', False)
        return render(request,'horizontal_balance_sheet.html', {"range":range(2,24),"newdate":newdate[4:]})
    
def party_statement(request):
    cust=customer.objects.all()
    company = company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.all()
    context={
        "customer":cust,
        "company":company,
        "vendor":vendor

    }
    return render(request,"party_statement.html",context)

def get_transactions(request):
    party = request.GET.get('party')
    st_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    st_date = datetime.strptime(st_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    estimates = Estimates.objects.filter(customer__customerName=party,estimate_date__range=(st_date, end_date))
    estimates_list = [ {'date': estimate.estimate_date,'transaction': "Estimate",'reference': estimate.reference,}
        for estimate in estimates
    ]
    re_invoice=RetainerInvoice.objects.filter(customer_name__customerName=party,retainer_invoice_date__range=(st_date, end_date))
    re_inv_list = [ {'date': re_invo.retainer_invoice_date,'transaction': "Retainer Invoice",'reference': re_invo.refrences,"total":re_invo.total_amount}
        for re_invo in re_invoice
    ]
    sales_order=SalesOrder.objects.filter(customer__customerName=party,sales_date__range=(st_date, end_date))
    sales_list = [ {'date': sale.sales_date,'transaction': "Sales order",'reference': sale.reference,"total":sale.grandtotal}
        for sale in sales_order
    ]
    del_chel=DeliveryChellan.objects.filter(customer_name=party,chellan_date__range=(st_date, end_date))
    del_chel_list=[ {'date': chel.chellan_date,'transaction': "Delivery Chellan",'reference': chel.reference,"total":chel.total}
        for chel in del_chel
    ]
    invo=invoice.objects.filter(customer__customerName=party,inv_date__range=(st_date, end_date))
    inv_list=[ {'date': inv.inv_date,'transaction': "Invoice",'reference': "","total":inv.grandtotal}
        for inv in invo
    ]
    rec_inv=recurring_invoice.objects.filter(cust_name__customerName=party,start__range=(st_date, end_date))
    recinv_list=[ {'date': recinv.start,'transaction': "Recurring Invoice",'reference':"", "total":recinv.total,}
        for recinv in rec_inv
    ]
    sale_lists=re_inv_list+sales_list+del_chel_list+inv_list+recinv_list
    sale_total=0.0
    for i in sale_lists:
        sale_total=sale_total+float(i["total"])    

    expense=Expense.objects.filter(vendor__vendor_display_name=party,start_date__range=(st_date, end_date))
    expense_list=[ {'date': exp.start_date,'transaction': "Expense",'reference': "",}
        for exp in expense
    ]
    pur_order=Purchase_Order.objects.filter(vendor_name=party,Ord_date__range=(st_date, end_date))
    pur_list=[ {'date':pur.Ord_date,'transaction': "Purchase Order",'reference': pur.ref,"total":pur.grand_total}
        for pur in pur_order
    ]
    pay_made=payment_made.objects.filter(vendor__vendor_display_name=party,date__range=(st_date, end_date))
    pay_list=[ {'date':pay.date,'transaction': "payment made",'reference': pay.reference,"total":pay.amount}
        for pay in pay_made
    ]
    pur_bills=PurchaseBills.objects.filter( Q(vendor_name=party) | Q(customer_name=party),
    bill_date__range=(st_date, end_date))
    pur_bill_list=[ {'date':bill.bill_date,'transaction': "Bill",'reference': "","total":bill.total}
        for bill in pur_bills
    ]
    re_pur_bill=recurring_bills.objects.filter(Q(vendor_name=party) | Q(customer_name=party),start_date__range=(st_date, end_date))
    re_pur_bill_list=[ {'date':re_bill.start_date,'transaction': "Recurring Bill",'reference': " ","total":re_bill.grand_total}
        for re_bill in re_pur_bill
    ]
    purchase_list=pur_list+pay_list+pur_bill_list+re_pur_bill_list
    pur_total=0.0
    for i in purchase_list:
        pur_total+=float(i["total"])   
    return JsonResponse({"transactions": re_inv_list+estimates_list+sales_list+
                         del_chel_list+inv_list+recinv_list+expense_list+pur_list+pay_list
                         +pur_bill_list+re_pur_bill_list,"sale_total":sale_total,"pur_total":pur_total})


def all_parties(request):
    custom=customer.objects.all()
    vend=vendor_table.objects.all()
    company = company_details.objects.get(user=request.user)
    return render(request,'all_parties.html',{"cust":custom,"vendor":vend, "company":company,})
    
def purchasebyitem(request):
    user=request.user
    customer1 = customer.objects.filter(user=user)
    company_data = company_details.objects.get(user=request.user)
    bills = PurchaseBillItems.objects.all()
    return render(request,'purchases_by_item.html',{'cust': customer1, 'company': company_data,'bills':bills})

def customize_report_purchasebyitem(request):
    user=request.user
    vendor=vendor_table.objects.all()
    company_data = company_details.objects.get(user=request.user)
    bills = PurchaseBillItems.objects.all()
    return render(request,'customize_report_purchasebyitem.html',{'vendors':vendor,'company': company_data,'bills':bills})
   
def purchasebyvendor(request):
    customer1 = customer.objects.all()
    company_data = company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.all()
    return render(request,'purchases_by_vendor.html',{'cust': customer1, 'company': company_data,'vendors':vendor})


def customize_vendor_report(request):
    vendor=vendor_table.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request,'customize_report_vendor.html',{'vendors':vendor,'company': company_data})
    
def ewaylistout(request):
     proj=EWayBill.objects.filter(user=request.user)
     custom=customer.objects.all()
     company=company_details.objects.get(user=request.user)
     return render(request,'ewaylistout.html',{'proj':proj,'custom':custom,'company':company})
     
def ewaycreate(request):
     user_id=request.user.id
     udata=User.objects.get(id=user_id)
     data=customer.objects.all()
     payments=payment_terms.objects.all()
     trans=Transportation.objects.all()
     units = Unit.objects.all()
     sales=Sales.objects.all()
     purchase=Purchase.objects.all()
     sales_type = set(Sales.objects.values_list('Account_type', flat=True))
     purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
     item = AddItem.objects.filter(user = request.user)
     company=company_details.objects.get(user=request.user)
     return render(request,'ewaycreate.html',{'data':data,'payments':payments,'trans':trans,'units':units,'sales':sales,'purchase':purchase,'sales_type':sales_type,'purchase_type':purchase_type,'item':item,'company':company})
     
def ewayb_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype,GSTIN=gstin, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
def customer_dropdown_ewayb(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.id , option.customerName]

    return JsonResponse(options) 
    
def recurbills_pay_eway(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        name = request.POST.get('name')
        days = request.POST.get('days')

        # Create a new payment_terms object and save it to the database
        payment_term = payment_terms(Terms=name, Days=days)
        payment_term.save()

        # Return a JSON response indicating success
        return JsonResponse({"message": "success"})
        
def add_transportation(request):
    if request.method == 'POST':
        transportation_method = request.POST.get('method')
        if transportation_method:
            transportation = Transportation(method=transportation_method)
            transportation.save()
            return JsonResponse({'message': 'Transportation added successfully.'})
        else:
            return JsonResponse({'message': 'Transportation method is required.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405) 
        
        
def ewaybills_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        
        type=request.POST.get('type')
        name=request.POST.get('name')
        ut=request.POST.get('unit')
        inter=request.POST.get('inter')
        intra=request.POST.get('intra')
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)

        u  = User.objects.get(id = request.user.id)

        item=AddItem(type=type,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=u ,creat=history,interstate=inter,intrastate=intra,unit = units,sales = sel, purchase = cost)

        item.save()

        return HttpResponse({"message": "success"})
    
    return HttpResponse("Invalid request method.")
    
    
def eway_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.filter(user = request.user)
    for option in option_objects:
        options[option.id] = [option.Name,option.id]

    return JsonResponse(options)
    
    
def eway_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
def eway_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = [option.unit,option.id]

    return JsonResponse(options)
    
    
def unit_get_rate(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':
        id=request.POST.get('id')

        item = AddItem.objects.get( id = id, user = user)
         
        rate = 0 if item.s_price == "" else item.s_price

        return JsonResponse({"rate": rate},safe=False)  
        
        
def create_ewaybillz(request):
    
    
    if request.method == 'POST':
        user_id=request.user.id
        user=User.objects.get(id=user_id)

        doc = request.POST.get('doc')
        transsub = request.POST.get('transsub')
        customerzz = request.POST.get('customerzz')
        cemail= request.POST.get('cemail')
        cgst_trt_inp = request.POST.get('cgst_trt_inp')
        cgstin_inp = request.POST.get('cgstin_inp')
        invoiceno = request.POST.get('invoiceno')
        date = request.POST.get('date')
        trans = request.POST.get('trans')
        adda = request.POST.get('adda')
        addb = request.POST.get('addb')
        srcofsupply = request.POST.get('srcofsupply')
        transportation = request.POST.get('transportation')
        km = request.POST.get('km')
        vno = request.POST.get('vno')
        
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        shipping_charge= request.POST['shipping_charge']
        adj= request.POST['adj']
        grand_total=request.POST['grandtotal']
        note=request.POST['note']
        cat = customer.objects.get(id=customerzz)
        eway_bill = EWayBill.objects.create(
            
            doc=doc,
            transsub=transsub,
            customerzz=customerzz,
            cemail=cemail,
            cgst_trt_inp=cgst_trt_inp,
            cgstin_inp=cgstin_inp,
            invoiceno=invoiceno,
            date=date,
            trans=trans,
            adda=adda,
            addb=addb,
            srcofsupply=srcofsupply,
            transportation=transportation,
            km=km,
            vno=vno,
            note=note,
            grand_total=grand_total,
            adj=adj,
            shipping_charge=shipping_charge,
            tax=tax,
            igst=igst,
            cgst=cgst,
            sgst=sgst,
            sub_total=sub_total,
            user=user,
            cust=cat,
        )

        items = request.POST.getlist("item[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")
        taxes = request.POST.getlist("tax[]")
        discounts = request.POST.getlist("discount[]")
        amounts = request.POST.getlist("amount[]")
        
        if len(items) == len(quantities) == len(rates) == len(discounts) == len(taxes) == len(amounts):
            for i in range(len(items)):
                EWayBillItem.objects.create(
                    eway_bill=eway_bill,
                    item=items[i],
                    quantity=quantities[i],
                    rate=rates[i],
                    tax=taxes[i],
                    discount=discounts[i],
                    amount=amounts[i],
                )

            return redirect('ewaylistout')
    
    return render(request, 'ewaycreate.html')
    
def ewayoverview(request,id):
    eway=EWayBill.objects.filter(user=request.user)
    ewayi=EWayBill.objects.filter(id=id)
    company=company_details.objects.get(user=request.user)
    ewayb = EWayBillItem.objects.filter(eway_bill_id=id)  # Fetch items related to the EWayBill id
    projc = get_object_or_404(EWayBill, id=id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            projc.comment = comment_text  # Set the comment field of the specific project object
            projc.save()  # Save the project object with the updated comment
    return render(request, 'ewayoverview.html',{'eway':eway,"ewayi":ewayi,'ewayb':ewayb,'projc':projc,'company':company})
    
    
def delete_ewaybills(request, id):

    
    ebill=EWayBill.objects.get(user = request.user, id= id)
    billway = EWayBill.objects.filter(user = request.user,id=id)

    ebill.delete() 
    billway.delete() 
     
    return redirect('ewaylistout')
    
def ewayedit(request,id):
     user_id=request.user.id
     udata=User.objects.get(id=user_id)
     data=customer.objects.all()
     payments=payment_terms.objects.all()
     trans=Transportation.objects.all()
     units = Unit.objects.all()
     sales=Sales.objects.all()
     purchase=Purchase.objects.all()
     sales_type = set(Sales.objects.values_list('Account_type', flat=True))
     purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
     item = AddItem.objects.filter(user = request.user)
     eway=EWayBill.objects.get(id=id)
     ewayi=EWayBill.objects.filter(id=id)
     ewayb=EWayBillItem.objects.filter(eway_bill_id=id)
     company=company_details.objects.get(user=request.user)
     return render(request,'ewayedit.html',{'data':data,'payments':payments,'trans':trans,'units':units,'sales':sales,'purchase':purchase,'sales_type':sales_type,'purchase_type':purchase_type,'item':item,'eway':eway,'ewayb':ewayb,'ewayi':ewayi,'company':company})
     

def ewaybill_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        e_bill = EWayBill.objects.get(user = request.user, id = id)
        e_bill.comments = cmnt
        e_bill.save()

        return HttpResponse({"message": "success"})
        
        
def ewayeditdb(request, id):
    eway = get_object_or_404(EWayBill, id=id)

    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        # Update EWayBill fields
        eway.doc = request.POST.get('doc')
        eway.transsub = request.POST.get('transsub')
        eway.customerzz = request.POST.get('customerzz')
        eway.cemail = request.POST.get('cemail')
        eway.cgst_trt_inp = request.POST.get('cgst_trt_inp')
        eway.cgstin_inp = request.POST.get('cgstin_inp')
        eway.invoiceno = request.POST.get('invoiceno')
        eway.date = request.POST.get('date')
        eway.trans = request.POST.get('trans')
        eway.adda = request.POST.get('adda')
        eway.addb = request.POST.get('addb')
        eway.srcofsupply = request.POST.get('srcofsupply')
        eway.transportation = request.POST.get('transportation')
        eway.km = request.POST.get('km')
        eway.vno = request.POST.get('vno')
        eway.sub_total = request.POST['subtotal']
        eway.sgst = request.POST['sgst']
        eway.cgst = request.POST['cgst']
        eway.igst = request.POST['igst']
        eway.tax = request.POST['total_taxamount']
        eway.shipping_charge = request.POST['shipping_charge']
        eway.adj = request.POST['adj']
        eway.grand_total = request.POST['grandtotal']
        eway.note = request.POST['note']
        eway.save()

        # Delete existing EWayBillItems associated with this EWayBill
        EWayBillItem.objects.filter(eway_bill=eway).delete()

        # Update EWayBillItems
        items = request.POST.getlist("item[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")
        taxes = request.POST.getlist("tax[]")
        discounts = request.POST.getlist("discount[]")
        amounts = request.POST.getlist("amount[]")

        if len(items) == len(quantities) == len(rates) == len(discounts) == len(taxes) == len(amounts):
            for i in range(len(items)):
                EWayBillItem.objects.create(
                    eway_bill=eway,
                    item=items[i],
                    quantity=quantities[i],
                    rate=rates[i],
                    tax=taxes[i],
                    discount=discounts[i],
                    amount=amounts[i],
                )

            return redirect('ewayoverview' ,id=id)

    return render(request, 'ewayedit.html', {'eway': eway})
    
def ewaycommentdb(request, id):
    projc = get_object_or_404(EWayBill, id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            if projc.comment:
                projc.comment += "\n" + comment_text  # Add new comment to existing comments
            else:
                projc.comment = comment_text  # If no comments exist, set it as the first comment
            projc.save()

    return redirect('ewayoverview', id=id)
    
def get_transportation_options(request):
    transportation_options = Transportation.objects.all().values_list('method', flat=True)
    options_list = list(transportation_options)
    return JsonResponse({'options': options_list})
def purchase_customer_eway(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            gstin=request.POST.get('gstin')
            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
        
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,GSTIN=gstin,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,CPsalutation=sal,Firstname=first,
                                    Lastname=last,CPemail=email,CPphone=mobile,
                                    CPmobile= wphone,CPskype=skname,CPdesignation=desg,
                                     CPdepartment=dept,user=u )
            ctmr.save()

        return HttpResponse({"message": "success"})
def get_customerdet_eway(request):
    company= company_details.objects.get(user = request.user)
    name = request.POST.get('name')
    id = request.POST.get('id')
    cust = customer.objects.get(user=company.user_id,id=id)
    email = cust.customerEmail
    cust_id=id
    cust_place_supply=cust.placeofsupply
    gstin = cust.GSTIN
    gsttr = cust.GSTTreatment
    # cstate = cust.placeofsupply.split("] ")[1:]
    print(email)
    print(gstin)
    print(id)
    # state = 'Not Specified' if cstate == "" else cstate
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin , 'cust_id':cust_id,'cust_place_supply':cust_place_supply},safe=False)
