import pandas as pd


machine = 'Desktop'

if machine == 'Server' :
    folder_path = r'C:\Users\paulp\OneDrive - Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Benchmark_Indices'

if machine == 'Laptop' :
    folder_path = r'C:\Users\Kyle Jennings\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Benchmark_Indices'

if machine == 'Desktop' :
    # path = r'C:\Users\ktjje\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\output - Yield Curve.csv'
    # path_unemployment = r'C:\Users\ktjje\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\output - FED Unemployment Rate.csv'
    path = r'C:\Users\Kyle Jennings\OneDrive - Arcadian Holdings LLC\5.  Arcadian Financial\Vista_v0.05\GetEconomicData\Data Files\output - Yield Curve.csv'
    path_unemployment = r'C:\Users\Kyle Jennings\OneDrive - Arcadian Holdings LLC\5.  Arcadian Financial\Vista_v0.05\GetEconomicData\Data Files\output - FED Unemployment Rate.csv'


df1 = pd.read_csv(path)

df1 = df1[df1 != "."].dropna()
df1['value'] = pd.to_numeric(df1['value'])
df1['date'] = pd.to_datetime(df1['date'])
# Need to omit blank datapoints from the dataseta nd convert values to numbers in order for pandas to recognize the data properly

# In the future, will need to drop duplicate date values

print(df1)

df2 = df1.sort_values('value', ascending=True)

# df2 = df1[df1 < 0]


print(df2)


avg_allTime = "{:.2f}".format(df1['value'].mean())

# print("{:.2f}".format(avg_allTime))
print("\n")
print("All Time Average: " + str(avg_allTime))


df_analysis_headers = ['Average', 'Minimum', 'Maximum', 'Median', 'Standard Deviation']
df_analysis_rows = [5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
# Need to add 'D' to these
# df_analysis_rows = ['5D', '10D', '20D', '1 Month', '2 Month', '3 Month', '4 Month', '5 Month', '6 Month', '7 Month', '8 Month', '9 Month', '10 Month', '11 Month', '12 Month']
# Note that '12 Month' is not precisely the same as '1 Year'; 'Months' are just rounded out to 30 days


# df_analysis_rows = ['5D', '10D', '20D', '1M', '2M', '3M', '150D', '180D']

# print(df1.tail(30))



# set the datetime column as the index
df1 = df1.set_index('date')

# create a rolling window of 30 calendar days
rolling_window = df1.rolling('30D')

# calculate the average values for the rolling window
avg = rolling_window.mean()

# select the last row of the rolling window
last_row = avg.iloc[-1]['value']

# print the average values for the last 30 calendar days
print(last_row)



averages_list = []
minimums_list = []
medians_list =[]

for row in df_analysis_rows :
    rolling_window = df1.rolling(str(row) + 'D')

    avg = rolling_window.mean()
    avg_value = avg.iloc[-1]['value']
    averages_list.append(avg_value)

    min = rolling_window.min()
    min_value = min.iloc[-1]['value']
    minimums_list.append(min_value)

    med = rolling_window.median()
    med_value = med.iloc[-1]['value']
    medians_list.append(med_value)









df3 = pd.DataFrame(
    {'Days': df_analysis_rows,
     'Average': averages_list,
     'Minimum': minimums_list,
     'Median': medians_list
    })

#    data={df_analysis_rows, averages_list}) #, columns='Average', index=df_analysis_rows)

df3 = df3.round(2)

df3['DIF'] = df3['Average'] - df3['Median']

list_skew = []

for value in df3['DIF'] :
    if value < 0 :
        list_skew.append('Negative')
    
    if value >= 0 :
        list_skew.append('Positive')

df3['Skew'] = list_skew

print(df3.to_string(index=False))