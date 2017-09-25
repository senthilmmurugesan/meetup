# Basics of Spark with Scala

### Install Spark

 * Download the latest version of Spark by visiting the following link [Download Spark](http://spark.apache.org/downloads.html)
 
 * Extract the TAR file,
```bash
 $ tar xvf spark-2.2.0-bin-without-hadoop.tgz  
```
 
 * Open the Spark shell,

```bash
$ spark-2.2.0-bin-without-hadoop/bin/spark-shell
```

* Scala REPL would open if the Spark is installed successfully.


### RDD Hands-on

Let's create an RDD from CSV file and do some transformations and actions on that RDD.

*	Map the CSV schema as indices.

```scala
val NAME = 0
val ROLE = 1
val EXECUTION = 2
val DEATH_SEASON = 3
val DEATH_EPISODE = 4
val DEATHFLASHBACK = 5
val LIKELIHOODOFRETURN_NOTES = 6
val LIKELIHOODOFRETURN = 7
```

*	Create an RDD from CSV file, 

```scala
val rdd = sc.textFile("got_deaths_rdd.csv")
```

*	Using map(), transform the RDD to Names RDD

```scala
val namesRdd = rdd.map(x => x.split(",")(NAME))
```

*	Using filter(), extract only Stark names

```scala
val starkRdd = namesRdd.filter(x => x.contains("Stark"))
```

*	Apply count() on starkRdd

```scala
starkRdd.count()
```

*	To view some samples, use take() action on the RDD

```scala
starkRdd.take(5)
```


### Dataframe Hands-on

##### Create a Dataframe from existing RDD.

*	Create a case class 'Death' with all the members

```scala
case class Death(name: String, role: String, execution: String, death_season: Int, death_episode: Int, deathFlashback: String, likelihoodOfReturn_notes: String, likelihoodOfReturn: String)
```

*	Load the CSV file in RDD

```scala
val rdd = sc.textFile("got_rdd.psv")
```

*	Map the RDD to Death Object

```scala
val ref_rdd = rdd.map(_.split("\\|")).map(x => Death(x(0), x(1), x(2), x(3).toInt, x(4).toInt, x(5), x(6), x(7)))
```

*	Convert the RDD[Death] to Dataframe using toDF()

```scala
val df = ref_rdd.toDF
```

* On successful creation, view the dataset by doing show() on the dataframe object

```scala
df.show()
```

#####	Create a Dataframe from JSON file.

* Define a case class that represents Device data.
```scala
case class DeviceIoTData (
  battery_level: Long,
  c02_level: Long,
  cca2: String,
  cca3: String,
  cn: String,
  device_id: Long,
  device_name: String,
  humidity: Long,
  ip: String,
  latitude: Double,
  longitude: Double,
  scale: String,
  temp: Long,
  timestamp: Long
)
```

* Read the json file and create dataset from the case class DeviceIoTData

```scala
val df = spark.read.json("iot_devices.json").as[DeviceIoTData]
```

* Filter out all devices whose temperature exceed 25 degrees and display the three fields that of interest

```scala
val dfTemp = df.filter(d => d.temp > 25).map(d => (d.temp, d.device_name, d.cca3))
dfTemp.show
```

* Apply higher-level Dataset API methods such as groupBy() and avg(). For temperatures > 25, compute devices' humidity and temperature by country.

```scala
val dfAvgTmp = dfTemp.groupBy($"_3").avg()
dfAvgTmp.show

```

*	Now, let us do the same actions using SQL based API. Using createOrReplaceTempView, register the dataset as a View.

```scala
df.createOrReplaceTempView("iot_device_data")
```

* Run SQL queries on this view,

```scala
val sampleDf = spark.sql("select * from iot_device_data where temperature > 25 limit 10")
sampleDf.show
```

```scala
val resDf = spark.sql("select cca3, avg(humidity), avg(temperature) from iot_device_data where temperature > 25 group by cca3 limit 10")
resDf.show
```
