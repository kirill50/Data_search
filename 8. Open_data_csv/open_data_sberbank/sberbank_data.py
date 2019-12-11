import pandas as pd
from pick import pick
import matplotlib.pyplot as plt

data_frame=pd.read_csv("/Users/kirillvolkov/PycharmProjects/Data_search/open_data_sberbank/opendata.csv",
                       encoding = "cp1251", sep=',', parse_dates=['date'], dayfirst=True, index_col='date' )

category=data_frame['name'].drop_duplicates().values.tolist()
region=data_frame['region'].drop_duplicates().values.tolist()

#Insert the time period from 15-01-2015 to 01-02-2019:
prepared_frame = data_frame[(data_frame.index > '2015-01-01') & (data_frame.index <= '2016-01-28')]

question1='Выбираем необходимую категорию: '
question2='Выбираем регион: '

chosen_category=(pick(category,question1))[0]
chosen_region=(pick(region,question2))[0]

result=prepared_frame[prepared_frame['name']==chosen_category]
result=result[result['region']==chosen_region]
print(result)

plt.plot(result['value'], color='red' ,marker='o')
plt.title(chosen_category, loc='left')
plt.xlabel('Дата',fontweight='bold')
plt.show()
