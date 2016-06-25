import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from numpy import zeros


os.chdir(' ')
df = pd.read_csv('bids.csv')
df['diff'] = df['After'] - df['Before']
#df = df[df['diff'] < 0]
#df['ddate'] = df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df['Date'] = pd.to_datetime(df['Date'])
df['CPAGKW'] = df['Campaign'] + df['Adgroup'] + df['Keyword']

individual_kw = set(df['CPAGKW'])
individual_kw = list(individual_kw)
NN = len(individual_kw)
drops_data = pd.DataFrame(columns=('Line No.', 'Date', 'Year', 'Month', 'Day', 'Campaign', 'Adgroup', 'Keyword', 'Before', 'After', 'diff', 'CPAGKW'))
for ii in range(NN):
    tmp = df[(df['CPAGKW'] == individual_kw[ii])]
    q = ii % 100
    if q == 0:
        print ii, " th record completed out of total ", len(individual_kw)
    tmp = tmp.sort(['Date'])

    nn = len(tmp)
    for j in range(nn):
        if j == 0:
            diff_days = (tmp['Date'].iloc[j] - datetime.strptime('2014-03-03', '%Y-%m-%d')).days
        else:
            diff_days = (tmp['Date'].iloc[j] - tmp['Date'].iloc[j-1]).days
        dd = tmp['Date'].iloc[j]
        num_drops_month = len(tmp[(tmp['Date'] <= (dd + timedelta(days=30))) & (tmp['Date'] >= dd) & (tmp['diff'] < 0)])
        if tmp['diff'].iloc[j] < 0 and diff_days >= 30 and num_drops_month >= 5:
            #print 'haha'
            drops_data = drops_data.append(tmp.iloc[j], ignore_index=True)


drops_data.to_csv('lower_b.csv', sep=',')


st = datetime.now()
dat = pd.read_csv("byday.csv", skiprows=5)
dat['Date'] = pd.to_datetime(dat['Day'])
dat['Keyword'] = dat['Keyword'].str.replace('[','')
dat['Keyword'] = dat['Keyword'].str.replace(']','')
dat['Cost'] = dat['Cost'].str.replace(',','')
dat['Cost'] = dat['Cost'].astype('float64')
dat['posimps'] = dat['Impressions'] * dat['Avg. position']
dat['CPAGKW'] = dat['Campaign'] + dat['Ad group'] + dat['Keyword']


def get_before_after_bidchange_data(bids, dat):

    n = len(bids)

    before_clicks = zeros(n)
    before_imps = zeros(n)
    before_cost = zeros(n)
    before_posimps = zeros(n)
    after_clicks = zeros(n)
    after_imps = zeros(n)
    after_cost = zeros(n)
    after_posimps = zeros(n)

    for i in range(n):
        kw_dat = dat[dat['CPAGKW'] == bids['CPAGKW'].iloc[i]]
        pre_30d = bids['Date'].iloc[i] - timedelta(days=30)
        post_30d = bids['Date'].iloc[i] + timedelta(days=30)
        pre_dat = kw_dat[(kw_dat['Date'] < bids['Date'].iloc[i]) & (kw_dat['Date'] >= pre_30d)]
        post_dat = kw_dat[(kw_dat['Date'] > bids['Date'].iloc[i]) & (kw_dat['Date'] <= post_30d)]
        pre_clicks = sum(pre_dat['Clicks'])
        pre_imps = sum(pre_dat['Impressions'])
        pre_cost = sum(pre_dat['Cost'])
        pre_posimps = sum(pre_dat['posimps'])
        post_clicks = sum(post_dat['Clicks'])
        post_imps = sum(post_dat['Impressions'])
        post_cost = sum(post_dat['Cost'])
        post_posimps = sum(post_dat['posimps'])

        before_clicks[i] = pre_clicks
        before_imps[i] = pre_imps
        before_cost[i] = pre_cost
        before_posimps[i] = pre_posimps
        after_clicks[i] = post_clicks
        after_imps[i] = post_imps
        after_cost[i] = post_cost
        after_posimps[i] = post_posimps

        q2 = i % 100
        if q2 == 0:
            print i, " th record completed out of total ", len(bids)

    bids.reset_index(drop=True, inplace=True)
    bidss = pd.concat([bids,
                      pd.DataFrame(before_clicks, columns=['before_clicks']),
                      pd.DataFrame(before_imps, columns=['before_imps']),
                      pd.DataFrame(before_cost, columns=['before_cost']),
                      pd.DataFrame(before_posimps, columns=['before_posimps']),
                      pd.DataFrame(after_clicks, columns=['after_clicks']),
                      pd.DataFrame(after_imps, columns=['after_imps']),
                      pd.DataFrame(after_cost, columns=['after_cost']),
                      pd.DataFrame(after_posimps, columns=['after_posimps'])], axis=1)

    return bidss


result = get_before_after_bidchange_data(drops_data, dat)
result.to_csv('output.csv', sep=',')
print (datetime.now() - st).seconds
