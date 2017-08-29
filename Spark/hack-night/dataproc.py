import os

cluster_name = ""
def getJobDetails():
    print 'Job Types are hadoop | hive | pig | pyspark | spark | spark-sql'
    job = raw_input('Select Type of Job to run: ')
    print job

    flags = ["--archives","--class","--continue-on-failure","--driver-log-levels","--execute","--file ","--files","--jar","--jars","--labels","--params","--properties","--py-files","Additional"]
    fvalues = ['','','','','','','','','','','','','','']
    all_together = {"hadoop" : [0, 1, 3, 6, 7, 8, 9, 11,13], "hive" : [2, 4, 5, 8, 9, 10, 11], "pig" : [2, 3, 4, 5, 8, 9, 10, 11], "pyspark" : [0, 3, 6, 8, 9, 11, 12],"spark" : [0, 1, 3, 6, 7, 8, 9, 11], "sparksql" : [3, 4, 5, 8, 9, 10, 11]}

    if job in all_together:
        for i in all_together[job]:
            fvalues[i] = raw_input( flags[i] + ':' )
    else:
        print "The job you requested is not available"

    cmd = job + ' --cluster=' + cluster_name

    for i in xrange(0,14):
        if fvalues[i] != '':
            if flags[i] == 'Additional':
                cmd += " " + fvalues[i]
            else:
                cmd += " " + flags[i] + " " + fvalues[i]

    print cmd
    return cmd

def create_cluster(cluster_name):
    os.system("gcloud dataproc clusters create "+cluster_name+" --master-machine-type n1-standard-2 --num-workers 3 --worker-machine-type n1-standard-2 ")

def list_cluster():
    os.system("gcloud dataproc clusters list ")

def delete_cluster(cluster_name):
    os.system("gcloud dataproc clusters delete "+cluster_name)

def runjob_cluster():
    set_cluster()
    str = getJobDetails()
    os.system("gcloud dataproc jobs submit "+str)

def set_cluster():
    global cluster_name
    cluster_name = os.popen("gcloud dataproc clusters list| grep RUNNING | awk '{print $1}'").read().rstrip()

ans=True
while ans:
    print("""
    1.Create Cluster
    2.List Cluster
    3.Delete Cluster
    4.Set Cluster
    5.Submit Job
    6.Exit/Quit
    """)
    ans=raw_input("What would you like to do? ")
    if ans=="1":
        cluster_name = raw_input('Cluster Name: ')
        create_cluster(cluster_name)
        print("\nCluster Created")
    elif ans=="2":
        print("\n List of Cluster Running")
        list_cluster()
    elif ans=="3":
        delete_cluster(cluster_name)
        print("\n Cluster Deleted")
    elif ans=="4":
        set_cluster()
        print "\n Cluster set to {}".format(cluster_name)
    elif ans=="5":
        print("\n Running the Job now")
        runjob_cluster()
    elif ans == "6":
        ans = None
    else:
       print("\n Not Valid Choice Try again")
