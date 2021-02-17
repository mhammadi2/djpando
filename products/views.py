from django.shortcuts import render
from .models import Product, Purchase
import  pandas as pd
from  .utils import get_simple_plot,get_salesman_from_id,get_image
from .forms import PurchaseForm
import matplotlib.pyplot as plt
import seaborn as sns
# from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    #print(df)
    df['salesman_id'] = df['salesman_id'].apply(get_salesman_from_id)
    df.rename({'salesman_id':'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    # print(df)
    plt.switch_backend('Agg')
    plt.xticks(rotation=45) # rotation for x axis ticks by 45 degrres
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    # hue for differenct color for different Bar plot
    plt.tight_layout()
    graph = get_image()

    #return HttpResponse("Hello Salesperson")
    return render(request, 'products/sales.html', {'graph': graph})
          
@login_required
def chart_select_view(request):
    #Checking Queryset
    # qs1 = Product.objects.all().values()
    # qs2 = Product.objects.all().values_list()
    # print(qs1)
    # print("____")
    # print (qs2) 
    #Display Dataframe as below
    error_message = None
    df = None
    graph = None
    price = None

    try:
        product_df = pd.DataFrame(Product.objects.all().values())
        #print(product_df)
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']
        # df = pd.merge(purchase_df, product_df, on='product_id')
        #print(purchase_df.shape)
    
        
        if product_df.shape[0]>0: # Checking Database has some records or object or rows.
            #Drop id_y and date_y and renaming
            df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis = 1)
            price = df['price']
            if request.method == 'POST':
                #print(request.POST)
                chart_type = request.POST['sales']
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                #Checking Input Form Entry and Size of the  Database(Row,COl)
                # print(chart_type)
                # print(date_from, date_to)
                # print(purchase_df.shape)
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

                if chart_type !="":
                    if date_from !="" and date_to !="":
                        df = df[(df['date']>date_from) & (df['date']<date_to)]
                        df2 = df.groupby('date',as_index=False)['total_price'].agg('sum')
                        # print(chart_type, df2)
                    graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'], data=df)
                else:
                    error_message = 'Please enter a Chart Type to move Forward'
        else:
            error_message = "No records or rows in the Database"

    except:
        product_df = None
        purchase_df = None
        error_message = 'No records in the database'

    context = {
        # 'products': product_df.to_html(),
        # 'purchase': purchase_df.to_html(),
        #'df': df.to_html(),
        'error_message': error_message,
        'graph': graph,
        'price':price,
    }
    return render(request, 'products/main.html', context) #Each App name/template file to avoid conflicts

@login_required
def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message=None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user #login user
        obj.save()

        form = PurchaseForm() # reset the form
        added_message = "The purchase has been added"

    context = {
        'form': form,
        'added_message': added_message,
    }
    return render(request, 'products/add.html', context)
