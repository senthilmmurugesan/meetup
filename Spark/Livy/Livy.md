# **Livy**

Livy is an open source REST interface for interacting with Apache Spark from anywhere. It supports executing snippets of code or programs in a Spark context that runs locally or in Apache Hadoop YARN.

 * Interactive Scala, Python and R shells
 * Batch submissions in Scala, Java, Python
 * Multiple users can share the same server (impersonation support)
 * Can be used for submitting jobs from anywhere with REST
 * Does not require any code change to your programs

### **prerequisites**

```pip install requests```

If you have `Kerborized cluster`, you may need the below python package

```pip install requests-kerborose```

Here's a step-by-step example of interacting with Livy in Python with the Requests library. By default Livy runs on port `8998` 

## Spark

### Start Livy Session

Following code is for Livy server running on Kerberos
for `Kerberos` you need `requests_kerberos` library 


### Importing required packages
```
import json, pprint, requests, textwrap
import random
import math
import sys
from requests_kerberos import HTTPKerberosAuth, REQUIRED
```



```
host = '127.0.0.1:8998'
data = {'name': 'spark'}
headers = {'Content-Type': 'application/json'}
```

### Session Post request
```
r = requests.post(host + '/sessions', data=json.dumps(data), headers=headers, auth=HTTPKerberosAuth())
r.json()
```


### Get session state
```
session_url = host + r.headers['location']
r = requests.get(session_url, headers=headers,auth=HTTPKerberosAuth())
r.json()
```



### Execute sample code
```
statements_url = session_url + '/statements'
data = {'code': textwrap.dedent("""print "hi" """)}
r = requests.post(statements_url, data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
r.json()
```

### Poll for the result
```
statement_url = host + r.headers['location']
r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
pprint.pprint(r.json())

```

### Let's calculate value of PI

```
data = {
  'code': textwrap.dedent("""
    import random
    NUM_SAMPLES = 100000
    def sample(p):
      x, y = random.random(), random.random()
      return 1 if x*x + y*y < 1 else 0
    count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
    print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)
    """)}
```
```
r = requests.post(statements_url, data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
pprint.pprint(r.json())
```

### poll for the result
```
statement_url = host + r.headers['location']
r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
pprint.pprint(r.json())
```

### close and delete the session
```
session_url = 'http://ybmaster01.yotabites.com:8998/sessions/19'
requests.delete(session_url, headers=headers,auth=HTTPKerberosAuth())
```


## Batches
```
host = 'host:8998'
data = {'name': 'spark'}
headers = {'Content-Type': 'application/json'}
```
### *Executing SparkPi program through livy batch*

### Passing the required parameters 
```
data = {"file":"hdfs://jars/spark-examples-1.6.0-cdh5.9.2-hadoop2.6.0-cdh5.9.2.jar","className":"org.apache.spark.examples.SparkPi"}
```
**Note**: **The file must be present in `HDFS`**


### Batch post request
```
r = requests.post(host + '/batches', data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
r.json()
```
### Batch get request
```
r = requests.get(host + '/batches', headers=headers,auth=HTTPKerberosAuth())
r.json()
```

### Specifying driverMemory, driverCores, executorMemory, executorCores

**Note**: **The file must be present in `HDFS` only.**
```
data = {"file":"hdfs://jars/spark-examples-1.6.0-cdh5.9.2-hadoop2.6.0-cdh5.9.2.jar",\
				"className":"org.apache.spark.examples.SparkPi","driverMemory":"2g","driverCores":1,"executorMemory":'2g'\
				"executorCores":2}
```
```
r = requests.post(host + '/batches', data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
r.json()
```



-----------------------------------------------------------------
##Pyspark 

### start pyspark Livy Session 
```
data = {'kind': 'pyspark'}
```
```
r = requests.post(host + '/sessions', data=json.dumps(data),auth=HTTPKerberosAuth())
r.json()
```

### calculate value of PI through Pyspark 

```
data = {
'code': textwrap.dedent("""
    import random
    NUM_SAMPLES = 100000
    def sample(p):
      x, y = random.random(), random.random()
      return 1 if x*x + y*y < 1 else 0
    count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
    print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)
    """)
    }
```

```
statements_url=host+'/sessions/29/statements'
r = requests.post(statements_url, data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
pprint.pprint(r.json())
``` 
-----------------------------------------------------------------
##SparkR 

**start SparkR Livy Session **

```
data = {'kind': 'sparkr'}

```
```
r = requests.post(host + '/sessions', data=json.dumps(data),auth=HTTPKerberosAuth())
r.json()
```
**calculate value of PI through SparkR**
```
data = {
'code': textwrap.dedent("""
n <- 100000
piFunc <- function(elem) {
  rands <- runif(n = 2, min = -1, max = 1)
  val <- ifelse((rands[1]^2 + rands[2]^2) < 1, 1.0, 0.0)
      val
    }
    piFuncVec <- function(elems) {
      message(length(elems))
      rands1 <- runif(n = length(elems), min = -1, max = 1)
      rands2 <- runif(n = length(elems), min = -1, max = 1)
      val <- ifelse((rands1^2 + rands2^2) < 1, 1.0, 0.0)
      sum(val)
    }
    rdd <- parallelize(sc, 1:n, slices)
    count <- reduce(lapplyPartition(rdd, piFuncVec), sum)
    cat("Pi is roughly", 4.0 * count / n, "\n")
    """)
    }
```

    r = requests.post(statements_url, data=json.dumps(data), headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())
    
### Explore Livy REST API

**Session POST**

| name | description   | type|
|------|---------------|-----|
|kind  |The session kind (required) |	session kind |
| proxyUser |	User to impersonate when starting the session |	string |
|jars	|jars to be used in this session	|List of string|
|pyFiles	|Python files to be used in this session	|List of string|
|files	|files to be used in this session	|List of string|
|driverMemory	|Amount of memory to use for the driver process	|string|
|driverCores	|Number of cores to use for the driver process	|int|
|executorMemory	|Amount of memory to use per executor process	|string|
|executorCores	|Number of cores to use for each executor	|int|
|numExecutors	|Number of executors to launch for this session	|int|
|archives	|Archives to be used in this session	|List of string|
|queue	|The name of the YARN queue to which submitted	|string|
|name	|The name of this session	|string|
|conf	|Spark configuration properties	|Map of key=val |
|heartbeatTimeoutInSecond	|Timeout in second to which session be orphaned	|int


**Session/{Sessionid}/state**

|name	|description	|type|
|-------|---------------|----|
|id	|Session id	|int|
|state|	The current state of session| string|

**Batch Post**

|file	|File containing the application to execute	|path (required)|
|-----|--------------------------------------------------|------------------|
|proxyUser	|User to impersonate when running the job	|string|
|className|	Application Java/Spark main class	|string|
|args	|Command line arguments for the application	|list of strings|
|jars	|jars to be used in this session	|List of string|
|pyFiles|	Python files to be used in this session|	List of string|
|files	|files to be used in this session	|List of string|
|driverMemory|	Amount of memory to use for the driver process|	string|
|driverCores|	Number of cores to use for the driver process|	int|
|executorMemory|	Amount of memory to use per executor process|	string|
|executorCores|	Number of cores to use for each executor	|int|
|numExecutors|	Number of executors to launch for this session|	int|
|archives|	Archives to be used in this session	|List of string|
|queue|	The name of the YARN queue to which submitted|	string|
|name|	The name of this session	|string|
|conf|	Spark configuration properties|	Map of key=val |

**Batch**

|name	|description|type|
|------------|---------------|------|
|id		|The session id|int|
|appId	|The application id of this session	|String|
|appInfo	|The detailed application info	|Map of key=val |
|log		|The log lines|	list of strings|
|state	|The batch state	|string|



**GET /sessions**

    statement_url = host +"/sessions/?from=0&size=10"
    r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())

**GET /sessions/{sessionId}** 

    statement_url = host +"/sessions/0"
    r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())
    
**GET /sessions/{sessionId}/statements**

    statement_url = host +"/sessions/20/statements"
    r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())

**GET /sessions/{sessionId}/statements/{statementId}**

    statement_url = host +"/sessions/21/statements/1"
    r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())

**GET /batches**

    statement_url = host +"/batches/?from=0&size=10"
    r = requests.get(statement_url, headers=headers,auth=HTTPKerberosAuth())
    pprint.pprint(r.json())
    
**DELETE /sessions/{sessionId}**

    session_url = host+'/sessions/2'
    requests.delete(session_url, headers=headers,auth=HTTPKerberosAuth())
    
**GET batches state**
```
r = requests.get(host + '/batches', headers=headers,auth=HTTPKerberosAuth())
r.json()
```
**GET /batches/batchid**
```
r = requests.get(host + '/batches/1', headers=headers,auth=HTTPKerberosAuth())
r.json()
```
**DELETE /batches/batchid**

```
request.delete(host + '/batches/1', headers=headers,auth=HTTPKerberosAuth())
```

You can find more information @ https://github.com/apache/incubator-livy
