#traverse through all directories
#do other and
#percentage of requests

#save to data/comparisons
import os
import csv

#final csvs format


servers = {"apache/php":"Apache with php",
           "nginx/php":"Nginx with php",
           "nginx/python":"Nginx with python socket server",
           "apache/python":"Apache with python socket server",
           "node.js":"Node server",
           "Rust":"Http Rust server",
           "Go":"Http golang server",
           "Python":"Http python server built with sockets"
    }

dst = "./data/comparisons"

dirs = [{"path":os.path.join("./data",i),"server":i} for i in servers.keys()]


#TODO
#put measures that have same unit together

connectionconnect = os.path.join(dst,"connectionconnect.csv")
connectionprocessing = os.path.join(dst,"connectionprocessing.csv")
connectionwaiting = os.path.join(dst,"connectionwaiting.csv")
connectiontotal = os.path.join(dst,"connectiontotal.csv")
#other = os.path.join(dst,"other.csv")
#done
#time taken for tests is done
# time per requests (ms) , time per request(ms mean)
requests = os.path.join(dst,"requests.csv")
# requests per second(#/sec) and transfer rate(kbytes/sec)
time_per_requests = os.path.join(dst,"time_per_requests.csv")

time_taken_for_tests = os.path.join(dst,"timetaken.csv")
served = os.path.join(dst,"served.csv")

for d in dirs:
    print(d)
    
if not os.path.isdir(dst):
    os.makedirs(dst)

time_taken_rows = []
requests_rows = []
time_per_requests_rows = []

connectionconnectrows = []
connectionprocessingrows = []
connectionwaitingrows = []
connectiontotalrows =[]

with open(served,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(['Percentage of requests']+[i for i in servers.keys()])
    rows = [[] for i in range(9)]
    for d in dirs:
        served_path = os.path.join(d["path"],"served.csv") 
        if os.path.isfile(served_path):
            with open(served_path,"r") as f:
                reader = csv.reader(f,delimiter=",")
                next(reader)
                for i,row in enumerate(reader):
                    print(i,row)
                    rows[i] = row if rows[i] == [] else rows[i] +[row[1]]
        other_path = os.path.join(d["path"],"other.csv")
        
        if os.path.isfile(other_path):
            
            with open(other_path,"r") as f:
                print("Reading {}".format(other_path))
                reader = csv.reader(f,delimiter=",")
                request_row = [d["server"]]
                time_per_request_row = [d["server"]]
                for i,row in enumerate(reader):
                    #time taken for tests
                    if i==0:
                        time_taken_rows.append([d["server"],row[1]])
                    #requests per second
                    elif i>1 and i <4:
                        request_row.append(row[1])
                    else:
                        time_per_request_row.append(row[1])
                requests_rows.append(request_row)    
                time_per_requests_rows.append(time_per_request_row)
        connection_path = os.path.join(d["path"],"Connectiontimes.csv")
        if os.path.isfile(connection_path):

            with open(connection_path,"r") as f:
                reader = csv.reader(f,delimiter=",")
                next(reader)
                connectionconnectrow = [d["server"]]
                connectionprocessingrow = [d["server"]]
                connectionwaitingrow = [d["server"]]
                connectiontotalrow = [d["server"]]
                for i,row in enumerate(reader):
                    if i<5:
                        connectionconnectrow.append(row[2])
                    elif i<10:
                        connectionprocessingrow.append(row[2])
                    elif i<15:
                        connectionwaitingrow.append(row[2])
                    else:
                        connectiontotalrow.append(row[2])
                        
                connectionconnectrows.append(connectionconnectrow)
                connectionprocessingrows.append(connectionprocessingrow)
                connectionwaitingrows.append(connectionwaitingrow)
                connectiontotalrows.append(connectiontotalrow)
    for row in rows:
        writer.writerow(row)

print(time_taken_rows)
with open(time_taken_for_tests,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","Time taken for tests"])
    for row in time_taken_rows:
        writer.writerow(row)
    
with open(requests,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","Time per request (ms) (mean)","Time per request (ms) (mean, across all concurrent requests)"])
    for row in requests_rows:
        writer.writerow(row)

with open(time_per_requests,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","Requests per second (#/sec)","Transfer rate (Kbytes/sec)"])
    for row in time_per_requests_rows:
        writer.writerow(row)



with open(connectionconnect,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","min","mean","[+/-sd]","median","max"])
    for row in connectionconnectrows:
        writer.writerow(row)

with open(connectionprocessing,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","min","mean","[+/-sd]","median","max"])
    for row in connectionprocessingrows:
        writer.writerow(row)
with open(connectionwaiting,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","min","mean","[+/-sd]","median","max"])
    for row in connectionwaitingrows:
        writer.writerow(row)
with open(connectiontotal,"w") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Server","min","mean","[+/-sd]","median","max"])
    for row in connectiontotalrows:
        writer.writerow(row)

##with open(connectiontimes,"w") as f:
##    writer = csv.writer(f,delimiter=",")
    



    
            
        
    
    
    


