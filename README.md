## Getting started with programmable assessments 
Autoptic PQL is a functional language for timeseries data analysis. Here is a simple example with AWS Cloudwatch.
```
//query cloudwatch and get instance CPU utilization for the last hour
where("$cw_aws")
.what("CPUUtilization; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'")
.when("1h")
        .alias("$where[0].what[0].when[0]").as("ts_cpu")

//compute the 15th and 99th percentile summary statistics
.percentile("$ts_cpu;0.15;0.99").as("perc_cpu")

//print the percentile values, and all cpu timeseries data points.
.print("$perc_cpu","$ts_cpu")
        .out("cloudwatch_results.json")
```
PQL programs are executed through the Autoptic API. [Get a free endpoint]() and follow the steps to run the example.

#### 1. Configure access to AWS Cloudwatch

Create a local env.json file and add the contents below or [download the template](./examples/env_cw.json).
```
{
  "data":
  [
    {
      "name": "cw_aws",
      "type": "CloudWatch",
      "vars": {
        "AwsRegion": "us-east-1",
        "window": "300s",
        "aws_access_key_id": "",
        "aws_secret_access_key": ""
      }
    }
  ]
}
```
Add your account credentials in the "aws_access_key_id" and "aws_secret_access_key". The account must have read access to Cloudwatch. For more information check the [AWS guide on access credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) .

#### 2. Edit and save the PQL program
[Download the example](./examples/simple.pql) and change the query parameters in the "what" function to match an object in your AWS resources. The sample query is looking up "CPUUtilization" of an EC2 instance. [Check the full Cloudwatch metrics list](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html) for more options.

#### 3. Run the program through your endpoint and check the results

## Autoptic Architecture
PQL programs are edited locally and posted through a secure API endpoint to the Autoptic PQL runtime where code is executed. The runtime will get timeseries data from the remote sources configured in the program and return the computed results to the requesting client.  
![alt text](https://www.autoptic.io/assets/img/architecture_logical.png)

## PQL Program Structure
![alt text](https://www.autoptic.io/assets/img/pql_structure.png)
### Query
Query functions describe data inputs from the data sources:

[where](#where) | [what](#what) | [when](#when) | [window](#window) | [open](#open) | [as](#as) | [alias](#alias)

### Aggregate
Aggregate functions handle timeseries data reduction or aggregation:

[filter](#filter) | [merge](#merge)

### Compute
Compute functions allow computing simple or more complex statistics: 

[average](#average) | [min](#min) | [max](#max) | [count](#count) | [percentile](#percentile) | [math](#math)

### Output
Output functions direct how the resulting output will be handled:

[assert](#assert) | [sort](#sort) | [head](#head) | [tail](#tail) | [print](#print) | [out](#out)

### Data Source Reference
Data source references specify which data sources will be used from the environment definition:

[cloudwatch](#cloudwatch) | [prometheus](#prometheus)
		
## Functions
#### alias
---
#### as
---
#### assert
---
#### average
---
#### count
---
#### head
Selects the first set of data points from a timeseries variable.
- parameters: 1 timeseries variable and 1 integer | percent value.
- use: 
	- get the first 15 datapoints `head("$cpu0_user; 15")`
	- get the first 2% of datapoints `head("$cpu0_user; 2%")`
---
#### filter
---
#### math
---
#### max
---
#### merge
---
#### min
---
#### open
---
#### out
---
#### percentile
Computes percentile summaries for select timeseries.
- parameters: 1 timeseries variable and N+1 percentile float attributes.
- use
	- compute 1st percentile `percentile("$aws_cpu;0.01")`
	- compute 15th and 98th percentile `percentile("$aws_cpu;0.15;0.98")`
---
#### print
Outputs a set of timeseries variables.
- parameters: N+1 timeseries variables
- use: 
	- output stats and timeseries values `print("$cnt_aws", "$cnt_prom", "$assert_cnts")`
---
#### sort
Sorts all data points in a timeseries variable.
- paramertes: 1 timeseries variable and 1 integer flag.
- use:
	- sort in ascending order `sort("$prom_cpu_5m_last30m_filtered; 1")`
	- sort in descending order `sort("$prom_cpu_5m_last30m_filtered; 0")`
---
#### tail
Selects the last set of data points from a timeseries variable.
- parameters: 1 timeseries variable and 1 integer | percent value.
- use: 
	- get the last 20 datapoints `tail("$cpu0_user; 20")`
	- get the last 3% of datapoints `tail("$cpu0_user; 3%")`
---
#### window
Selects the granularity of the time series data retrieved from the data source.
- parameters: n+1 time windows/buckets
- use:
	- 30 second window selection `window("30s")`
	- 5 seconds and 1 hour window selections `window("5s","1h")`
- default: 300s
---
#### what
Defines the query keywords and metadata submitted to the data sources.
- parameters: n+1 queries
- use:
	- get instance CPU utilization from AWS `what("CPUUtilization; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'")`
	- get cpu utilization from Prometheus `what("node_cpu_seconds_total")`
	- get multiple metrics from AWS EC2 instance
	```
	what(
	  "CPUUtilization; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'",
	  "NetworkOut; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'",
	  "NetworkIn; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'"
	)	
	```
	- get metrics from AWS and Prometheus
	```
	what(
	  "CPUUtilization; Average; InstanceId='i-00f8880d7a4d502db'; namespace='AWS/EC2'",
	  "node_cpu_seconds_total"
	)
	```
---
#### when
Selects the query time ranges for the program
- parameters:  n+1 time ranges
- use:
	- releative time selection 
		- recent 5 minutes `when("5m")` 
		- recent 1 hour `when("1h")`
		- recent 7 days `when("7d")`
	- absolute time selection
		- start and end date time `"when("start = '02-22-2022 00:00:00 +00'; end = '02-22-2022 23:59:59 +00'")`
	- multi selection
		- recent 24 hours and 2-22-22 `when("24h","start = '02-22-2022 00:00:00 +00'; end = '02-22-2022 23:59:59 +00'")`
---
#### where 
Selects the data sources that will be used in the program from the [data source configuration](#data-sources).
- parameters: n+1 data source references
- use: 
	- 3 data source references `where("$dsA","$dsB","$dsC")`

## Data Sources
#### cloudwatch
#### prometheus

## Example programs
Check out the [example programs](./examples/) for more ideas on how to use PQL to the max!
