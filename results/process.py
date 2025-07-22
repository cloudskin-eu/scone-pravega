import os
import json
import glob
import yaml
import statistics
import pandas as pd
from matplotlib import pyplot as plt



########################################################################
# General Data
########################################################################

test_cases = ['TC01', 'TC02', 'TC03', 'TC04', 'TC05', 'TC06',
              'TC07', 'TC08', 'TC09', 'TC10', 'TC11', 'TC12']
environments = ['STANDARD', 'SCONE']

########################################################################
# Average results
########################################################################

def getTimes(times, testcase, envronment):
    tmp = times[ (times['Test_Case'] == testcase) & (times['Env'] == envronment) ]
    return tmp.iloc[0]

report_data = {
    'Test_Case': [],
    'Producer_Rate': [],
    'Environment': [],
    'Message_Size': [],
    'Latency_50': [],
    'Latency_75': [],
    'Latency_95': [],
    'Latency_99': [],
    'Messages': [],
    'Bytes': [],
    'Duration': [],
    'Throughout': [],
}

df = pd.read_csv('times.csv')
for test_case in test_cases:
    for env in environments:
        # Times
        row = getTimes(df, test_case, env)
        # Configuration
        file_path = test_case + '-OMB-' + env + '.yaml'
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        # Results
        file_path = test_case + '-OMB-' + env + '.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Set results
        report_data['Test_Case'].append( test_case )
        report_data['Producer_Rate'].append( config['producerRate'] )
        report_data['Environment'].append( env )
        report_data['Message_Size'].append( config['messageSize'] )
        report_data['Latency_50'].append( data.get('aggregatedPublishLatency50pct') )
        report_data['Latency_75'].append( data.get('aggregatedPublishLatency75pct') )
        report_data['Latency_95'].append( data.get('aggregatedPublishLatency95pct') )
        report_data['Latency_99'].append( data.get('aggregatedPublishLatency99pct') )
        report_data['Messages'].append( data.get('totalMessagesSent') )
        report_data['Duration'].append( row['Time'] )
        report_data['Bytes'].append( data.get('totalBytesSent') * 0.000001 ) 
        report_data['Throughout'].append( (data.get('totalBytesSent') * 0.000001) / row['Time'] )

res = pd.DataFrame(report_data)
res.to_csv('result.csv', index=False)
print('Metrics written in result.csv')

########################################################################
# Percentiles
########################################################################

report_data = {
    'Test_Case': [],
    'Producer_Rate': [],
    'Environment': [],
    'Message_Size': [],
    'Percentile': [],
    'Latency': [] 
}

for test_case in test_cases:
    for env in environments:
        file_path = test_case + '-OMB-' + env + '.yaml'
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        
        file_path = test_case + '-OMB-' + env + '.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        latencies = data.get('aggregatedPublishLatencyQuantiles')
        for key, value in latencies.items():
            report_data['Test_Case'].append( test_case )
            report_data['Producer_Rate'].append( config['producerRate'] )
            report_data['Environment'].append( env )
            report_data['Message_Size'].append( config['messageSize'] )
            report_data['Percentile'].append( key )
            report_data['Latency'].append( value )

res = pd.DataFrame(report_data)
res.to_csv('percentiles.csv', index=False)
print('Metrics written in percentiles.csv')
