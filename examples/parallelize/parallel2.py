import boto3
import concurrent.futures
import time
import pdb

# Function to fetch metric data for a given MetricName with retries
def fetch_metric_data_with_retry(metric_name, max_retries=3):
    cloudwatch = boto3.session.Session().client('cloudwatch', region_name='us-east-1')
    startDate = '29-08-2023 00:00:00 +00'
    endDate = '29-08-2023 06:59:59 +00'
    period = 300

    # Use a custom 'Id' based on the metric name
    id_prefix = 'custom_'  # You can change this prefix as needed
    id_value = id_prefix + metric_name

    for retry in range(max_retries):
        try:
            return cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': id_value,
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/RDS',
                                'MetricName': metric_name,  # Use the provided MetricName
                                'Dimensions': [
                                    {
                                        'Name': 'DBInstanceIdentifier',
                                        'Value': 'odoo-prod'  # Update with your DBInstanceIdentifier
                                    },
                                ]
                            },
                            'Period': period,
                            'Stat': 'Average'
                        },
                    }
                ],
                StartTime=startDate,
                EndTime=endDate,
                ScanBy='TimestampAscending',
                LabelOptions={
                    'Timezone': '-0300'
                }
            )
        except Exception as e:
            print(f"Metric '{metric_name}' query failed with error: {e}")
            if retry < max_retries - 1:
                wait_time = 2 ** retry  # Exponential backoff (2^retry seconds)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Max retries exceeded for metric '{metric_name}'")

# List of MetricNames you want to query in parallel
metric_names = [
    'CPUUtilization',
    'DatabaseConnections',
    'FreeStorageSpace',
    'ReadIOPS',
    'WriteIOPS',
    'ReadLatency',
    'WriteLatency',
    'ReadThroughput',
    'WriteThroughput',
    'SwapUsage',
    'DiskQueueDepth',
    'ReplicaLag',
    'FreeableMemory',
    'CPUCreditUsage',
    'CPUCreditBalance',
    'NetworkReceiveThroughput',
    'NetworkTransmitThroughput',
    'VolumeBytesUsed',
    'VolumeReadIOPs',
    'VolumeWriteIOPs',
    'VolumeReadBytes',
    'VolumeWriteBytes',
    'ActiveTransactions',
    'CommitLatency',
    'Deadlocks',
    'FailedSQLServerAgentJobsCount'
]

# Control the number of max_workers
max_workers = len(metric_names)  # Set the desired number of workers

# Create a ThreadPoolExecutor to run queries in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit queries in parallel
    futures = {executor.submit(fetch_metric_data_with_retry, metric_name): metric_name for metric_name in metric_names}

    # Wait for all queries to complete and retrieve results
    for future in concurrent.futures.as_completed(futures):
        metric_name = futures[future]
        try:
            result = future.result()
            # Process the result as needed
            #print(f"Metric '{metric_name}' query result: {result}")
        except Exception as e:
            print(f"Metric '{metric_name}' query failed with error: {e}")
            raise(e)

#pdb.set_trace()