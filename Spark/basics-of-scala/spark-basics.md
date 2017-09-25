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

