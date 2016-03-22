import os 
import re
import pandas as pd
import datetime

df = pd.read_csv('ch_history.csv', skiprows=1)
df = df[(df['Campaign'] == 'Search - Generic - Exact')|(df['Campaign'] == 'Search - Generic - Exact 2')]  
df = df.reset_index(drop=True)

line_num = list()
dates = list()
YY = list()
MM = list()
DD = list()
campaign = list()
adgroup = list()
keyword = list()
before_bid = list()
after_bid = list()

for ii in range(0, len(df)):
    cp = df['Campaign'][ii]
    ag = df['Ad Group'][ii]
    str = df['Changes'][ii] 
    date_time = datetime.datetime.strptime(df['Date & time'][ii], '%b %d, %Y %I:%M:%S %p')
    date_string = date_time.strftime('%Y-%m-%d')
    str_split = re.split('\n',str)
	
    for jj in range(0, len(str_split)):
        split2 = re.split(' ',str_split[jj])
		
        if (split2[1] == 'Exact' and split2[4] == 'max' and split2[5] == 'CPC'):
            num_kw = int(split2[0])	
			
            for kk in range(1, num_kw+1):
                split3 = re.split('\$', str_split[jj + kk])
                kw_indx1 = split3[0].index('[')
                kw_indx2 = split3[0].index(']')
                kw = split3[0][kw_indx1 + 1 : kw_indx2]
                before1 = re.split(' ',split3[1])[0]
				
                if(')' in before1):
                    before = float(before1[:-1])
                else:
                    before = float(before1)   
                try:
				  after = float(split3[2])
                except:
				  print ii, jj, kk, split3
                line_num.append(ii)
                dates.append(date_string)
                YY.append(date_time.year) 
                MM.append(date_time.month) 
                DD.append(date_time.day)
                campaign.append(cp)
                adgroup.append(ag)
                keyword.append(kw)
                before_bid.append(before)
                after_bid.append(after) 
   

clean_df = pd.DataFrame({'Line No.': line_num})
clean_df['Date'] = dates
clean_df['Year'] = YY
clean_df['Month'] = MM
clean_df['Day'] = DD
clean_df['Campaign'] = campaign
clean_df['Adgroup'] = adgroup
clean_df['Keyword'] = keyword
clean_df['Before'] = before_bid
clean_df['After'] = after_bid
clean_df.to_csv('bids.csv', sep=',')
