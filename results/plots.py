import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt

########################################################################
# General function
########################################################################

def format_label(size):
    if int(size) == 100:
        return '100B'
    elif int(size) == 1024:
        return '1KB'
    elif int(size) == 10240:
        return '10KB'
    elif int(size) == 102400:
        return '100KB'

########################################################################
# Write Latency Percentiles by Event Size
########################################################################

def get_dfs(data):
    data1 = data[ data['Environment'] == 'STANDARD' ]
    data2 = data[ data['Environment'] == 'SCONE' ]

    return data1, data2

def split_event_size(data):
    data1 = data[ data['Message_Size'] == 100 ]
    data2 = data[ data['Message_Size'] == 1024 ]
    data3 = data[ data['Message_Size'] == 10240 ]
    data4 = data[ data['Message_Size'] == 102400 ]
    return [data1, data2, data3, data4]

def get_security(data):
    return data['Environment'].iloc[0]

def get_label(row):
    return str(int(row['Producer_Rate'])) + ' e/s'

def subplot_cdf(data1, data2, row, title, autolimit=False):
    fig, axs = plt.subplots(2, 2)
    
    spr1 = split_event_size(data1)
    spr2 = split_event_size(data2)
    a = 0
    for i in range(2):
        for j in range(2):
            labels = list(spr1[i].apply(get_label, axis=1))
            
            lbl = 'Event Size ' + format_label(spr1[a]['Message_Size'].iloc[0])
            axs[i][j].plot(labels, spr1[a][row], label=get_security(spr1[a]) )
            axs[i][j].plot(labels, spr2[a][row], label=get_security(spr2[a]) )

            axs[i][j].set_yscale('log')
            if autolimit:
                axs[i][j].set_ylim(0.001, 1000)
            else:
                axs[i][j].set_ylim(1, 10000)
            axs[i][j].set_title(lbl)
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;

    fig.suptitle(title)
    plt.tight_layout()
    #plt.show()
    plt.savefig('img/' + title + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot ' + title + ' generated')

df = pd.read_csv('result.csv')
df1, df2 = get_dfs(df)
subplot_cdf(df1, df2, 'Latency_50', 'Write Latency 50 pct')
subplot_cdf(df1, df2, 'Latency_75', 'Write Latency 75 pct')
subplot_cdf(df1, df2, 'Latency_95', 'Write Latency 95 pct')
subplot_cdf(df1, df2, 'Latency_99', 'Write Latency 99 pct')
subplot_cdf(df1, df2, 'Throughout', 'Throughout', autolimit=True)

########################################################################
# CDF by Producer Rate
########################################################################

def get_title(data):
    pr = data['Producer_Rate'].iloc[0]
    mz = data['Message_Size'].iloc[0]
    return 'Event Size ' + format_label(mz) + ' | Producer Rate ' + str(pr) + ' e/s'

def split_data(data, test_cases):
    res = []
    for test_case in test_cases:
        tmp = data[ (data['Test_Case'] == test_case) ]
        res.append(tmp)
    return res

def subplot_cdf_percentile(data, test_cases):
    fig, axs = plt.subplots(2, 2)

    a = 0
    data_list = split_data(data, test_cases)
    
    for i in range(2):
        for j in range(2):
            f1 = data_list[a][ data_list[a]['Environment'] == 'STANDARD' ]
            f2 = data_list[a][ data_list[a]['Environment'] == 'SCONE' ]
            message_size = f1['Message_Size'].iloc[0]
            
            axs[i][j].plot(f1['Latency'], f1['Percentile'], label='STANDARD')
            axs[i][j].plot(f2['Latency'], f2['Percentile'], label='SCONE')
            axs[i][j].set_xscale('log')
            axs[i][j].set_xlim(0.1, 10000)
            axs[i][j].set_title('Event Size ' + format_label(message_size))
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;

    producer_rate = data_list[0]['Producer_Rate'].iloc[0]
    fig.suptitle('Producer Rate ' + str(producer_rate) + ' e/s')
    plt.tight_layout()
    #plt.show()
    plt.savefig('img/Percentile_PM' + str(producer_rate) + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot Percentile generated')

df = pd.read_csv('percentiles.csv')
subplot_cdf_percentile(df, ['TC01', 'TC02', 'TC03', 'TC04'])
subplot_cdf_percentile(df, ['TC05', 'TC06', 'TC07', 'TC08'])
subplot_cdf_percentile(df, ['TC09', 'TC10', 'TC11', 'TC12'])


