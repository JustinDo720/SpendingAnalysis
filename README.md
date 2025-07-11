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