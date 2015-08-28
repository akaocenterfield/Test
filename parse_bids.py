import os 
import pandas as pd
import datetime

df = pd.read_csv('change_history.csv', skiprows=range(0,1))
df.columns.values

line_num = list()
dates = list()
YY = list()
MM = list()
DD = list()
keyword = list()
before_bid = list()
after_bid = list()

for ii in range(0, len(df)):
    str = df['Changes'][ii] 
    str_list = str.split(' ',3)
    if (str_list[1] != 'max' and str_list[2] != 'CPC'):
        print ii, 'th row does not contain Max. CPC changes!'
        continue
    date_time = datetime.datetime.strptime(df['Date & time'][ii], '%b %d, %Y %I:%M:%S %p')
    date_string = date_time.strftime('%Y-%m-%d')
    num_kw = int(str_list[0])   
    bid_change = str.split('\n') 
    
    for jj in range(0, num_kw):
        tmp = bid_change[jj+1].split(':')
        kw = tmp[0][3:-1]                
        try:
            before = float(tmp[1].split('$')[1].split(' ')[0])
        except: 
            before = float(tmp[1].split('$')[1].split(')')[0])
        after = float(tmp[1].split('$')[2])      

        line_num.append(ii)
        dates.append(date_string)
        YY.append(date_time.year) 
        MM.append(date_time.month) 
        DD.append(date_time.day)
        keyword.append(kw)
        before_bid.append(before)
        after_bid.append(after) 

clean_df = pd.DataFrame({'Line No.': line_num})
clean_df['Date'] = dates
clean_df['Year'] = YY
clean_df['Month'] = MM
clean_df['Day'] = DD
clean_df['Keyword'] = keyword
clean_df['Before'] = before_bid
clean_df['After'] = after_bid
clean_df.to_csv('bids.csv', sep=',')

