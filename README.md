# Spending Analysis Application 

## Objective 

Spending Analysis helps **reduce costs** by learning about **spending patterns** through tracking and analysis of financial data. This **RESTAPI** will take in *CSV* files as input, processes and categorizes spending data, and generates charts and actionable results.

## MVP Key Features 

**Upload CSV**
- Our application should accept CSV files 
- *Date*, *Vendor*, *Category*, *Amount*

**Parse & Store Data**
- `pandas` to parse rows 
- API should be able to return all of our transactions (Each row should be in our database)

**Key Endpoints**
- *Top Vendors* 
- *Spending Via Category*
- *Monthly Trend*

## Expenditure CSV Example 

We'll be building this RESTFul Application around a CSV that looks like this:

```csv
Date,Vendor,Category,Amount
2025-06-01,Walmart,Grocery,124.56
2025-06-03,Amazon,Shopping,89.99
2025-06-05,Netflix,Entertainment,15.99
2025-06-08,Duke Energy,Utilities,103.21
2025-06-10,Uber,Transport,25.00
```

[Sample CSV File](sample_transactions.csv) 

## Development Tracking 

**07/11/25**
- Django + Django Restframework 
- Added URLS and built Default Routers 
- Set Default Authentication as `SessionAuthentication` 
- Set Default Permission to `IsAuthenticatedOrReadOnly`
- Added Authentication urls: `path('api-auth/', include('rest_framework.urls')),`
- Created Category Viewset for full CRUD 
- Created Home Page functional API view to return the **reverse** links to all of our API 
- Made Transactions ListCreate + RetrieveUpdateDelete API views 
- Tied hyperlinks to each view via (URL in serializer)

Result: Full CRUD operations on Transactions + Categories with hyperlinks and customized Serializers.

---

**07/12/25**
- Planning for API Accept CSV 
  - Pandas data manipulation 
  - Return meaningful/actionable insights 
- `ListCreate` now accepts CSV, creates Category: `get_or_create` builds transactions, Provides summary 
- Hyperlink Transactions --> File Upload 
- Individual File Upload URL should direct us to a summary + nested Transactions 
- Summary => Rebuild all the data from **prefetched transactions**, Dataframe then:
  - Total Spent
  - Spending Per Category: Group By Category, Access Amount, Sum, Sort via Descdening, Transform to Dictionary 
  - Top Vendors: Group By Vendor, Access Amount, Sum, Sort via Descdening, Head(n), Transform to Dictionary
- Summary Url => `SerializerMethodField` 
  - Make sure we get request through: `self.context.get('request')` and we're using `from rest_framework.reverse import reverse`
  - `reverse('api_name', args=[obj.id], request=request, format=None)`
  - Need to supply the id since we have `<int:upload_id>` in our url 
  
Result: API View accepts CSV Uploads, creates Transactions + Categories. Summary API for files based on related transactions.

**07/14/25**
- Corsheaders for React Frontend 
- `"corsheaders"` in settings.py and `pip install django-cors-headers`
- Disabled Permissions because we are not using SJWT
- Connected Frontend with CSV Upload 

Result: React frontend works with uploaded CSV files + Displays Summary Report

<img src='spending_analysis_demo1.gif'>

**07/15/25**
- Plans:
  - Improve Summary? (Monthly Totals (money/time)-> Category Growth (% increase/decrease))
  - Build Dashbaord for file uploads + Summary access
  - Look into how Tableau could help our App (FastAPI/Flask Microservice)
  - AI plans -> Smart summaries -> Translate raw analytics into executive-friendly reports or actionable suggestions (FastAPI/Flask Microservice)
- Added Media Root + Url to `urls.py` using: `MEDIA_URL = os.path.join(BASE_URL, 'media')`
- File Name instance method for serializer to display individual file names
- Summary now includes
  - Number of **Categories**, **Vendors** 
  - Date Range **Max** and **Min**
  - **Spending per Vendor**
  
Result: More information on Summary to display on frontend. Media Files are viewable locally. Plans for microservices.


**07/16/25**
- **WeasyPrint** for Template -> PDF 
- Django Bootstrap CDN for templates (Need the **Bootstrap.min.css** static files instead: [here](https://getbootstrap.com/docs/5.3/getting-started/download/))
- [GTK for WeasyPrint](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
  - If Production make sure you dockerize your container with this dependencny 
- WeasyPrint need `base_url` to access our static files 
- Use Django `HTTPResponse` to set the content type as `application/pdf` 
- Proviide the `Content-Disposition` as `attachment; file="filename_here.pdf"`

Result: API View that downloads a PDF version of our template based on HTML string.