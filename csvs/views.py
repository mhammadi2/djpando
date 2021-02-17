from django.shortcuts import render
from .forms import  CsvForm
from .models import Csv
from django.db import models
import csv
from django.contrib.auth.models import User
from products.models import  Product, Purchase
# Create your views here.

## Use following functions for sales_data2.csv format files with 6 cols or fields.
def upload_file_view(request):
    error_message = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)

                for row in reader:
                    row = "".join(row)
                    row = row.replace(";", " ")
                    row = row.split()
                    user = User.objects.get(id=row[3])
                    prod, _ = Product.objects.get_or_create(name=row[0])
                    Purchase.objects.create(
                        product=prod,
                        price = int(row[2]),
                        quantity = int(row[1]),
                        salesman = user,
                        date = row[4]+ " "+ row[5]
                    )

            obj.activated=True
            obj.save()
            success_message= "Uploaded sucessfully"
        except:
            error_message = "Ups. Something went wrong...."

    context = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'csvs/upload.html', context)


### Use for sales_data_1.csv file
    # def upload_file_view(request):
    # error_message = None
    # success_message = None
    # form = CsvForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    #     form = CsvForm()
        
    #     obj = Csv.objects.get(activated=False)
    #     print("After obj", obj)
    #     with open(obj.file_name.path, 'r') as f:
    #         reader = csv.reader(f)

    #         for row in reader:
    #             print("Just Row", row)
    #             # row = "".join(row)
    #             # # print("After joining",row)
    #             # row = row.replace(",","  ")
    #             # print("after replacing",row)
    #             # row = row.split()
    #             # print("row after split",row)
    #             user = User.objects.get(id=row[3])
    #             print("user", user)
    #             prod, _ = Product.objects.get_or_create(name=row[0])
    #             print ("product", prod)
    #             Purchase.objects.create(
    #                 product=prod,
    #                 price = int(row[2]),
    #                 quantity = int(row[1]),
    #                 salesman = user,
    #                 # date = row[4]+ " "+ row[5]
    #                 date = row[4]
    #             )

    #     obj.activated=True
    #     obj.save()
           

    # context = {
    #     'form': form,
    #     'success_message': success_message,
    #     'error_message': error_message,
    # }
    # return render(request, 'csvs/upload.html', context)