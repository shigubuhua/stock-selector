## stock importer and data processing

#### use easyquotation and tushare

as data source for all stock history data (daily)
as query source: for certain stock minuete or real time data

- tushare:
main source due to free history data;
the data is in tushare data frame, export: to_json(orient='index')
the output index is data like '2011-12-20', can be parse to datetime obj
then add code and datetime and save in pymongo


#### use fbprophet

as a simple predictor for certain stock
``` pip install numpy cython pystan fbprophet```
for windows, a C++ compiler must be installed;

- pandas dataframe https://chrisalbon.com/python/pandas_dataframe_importing_csv.html
``` raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
```

#### build strategy

- use strategy pick up stock list, and test its prediction result
- use trader strategy to calculate a strategy's profit for a time period