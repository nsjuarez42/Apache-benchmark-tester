#run ab
import os
import subprocess
import re
import csv
import argparse
#use argv
#which server is being tested choose from list
#standardize
#amount of tests
#menu with options

#write files with -e option
#parse through and do mean of csvs
#use csvs files for requests served percentage
#-l #Do not report errors if the length of the responses is not constant. This can be useful for dynamic pages.

#output in json file

#on data folder goes final results
#only keep certain data on csv instead of all of it
#create csv with connection Times and with percentage of requests
#create csv with other data k,v



units = {"Time taken for tests":"(seconds)",
             "Requests per second":"(#/sec)",
             "transferred":"(bytes)",
             "Transfer rate":"(Kbytes/sec)",
             "Time per request":"(ms)"}

def trunc_num(num):
    decimal = re.findall(r"[0-9]+[.]{1}[0-9]{2}",str(num))
    if len(decimal) == 0:
        return num
    else:
        return decimal[0]

def set_data_objects(data,objects):
    #specific data format
    #key value: value
    name = objects[0].split()[0]
    data[name] = {}
    for obj in objects:
        type_of_value=obj.split()[1]
        
        value = obj.split(":")[1].strip()
        data[name][type_of_value] = value

def set_data_objects_reverse(data,objects):
    #data format
    #value key : value
    #invert and send to set_data objects
    for i,obj in enumerate(objects):
        k,v = obj.split(":")
        objects[i] = " ".join(reversed(k.split()))+":"+v
    set_data_objects(data,objects)

def set_data(data,obj):
    #regular key: val code
    
    k,v = [i.strip() for i in obj.split(":")]
    if k in units.keys():
        unit = units[k]
        if k == "Time per request":
            k+= " "+unit +" " +" ".join(v.split()[2:])
        else:
            k+= " "+unit
    data[k] = v

def show_data(data):
    #takes data object and visualizes it properly
    for k,v in data.items():
        if type(v) != dict:
            print(k,v)
        else:
            print(k)
            for kk,vv in v.items():
                if type(vv) != dict:
                    print("-",kk,vv)
                else:
                    print("-",kk)
                    for kkk,vvv in vv.items():
                        print("--",kkk,vvv)
                    
    pass

def traverse_data(data):
    
    pass

def get_mean(data_list,amount):
    #compare the data that i get to the transformed one in initial mean value
    mean = {}
    units = {"Time taken for tests":"(seconds)",
             "Requests per second":"(#/sec)",
             "transferred":"(bytes)",
             "Transfer rate":"(Kbytes/sec)"
        }
    float_regex = r'[0-9]+[.]{1}[0-9]+'
    int_regex = r'[0-9]+'
    #for units when changed here keys differ from data and mean
    #set them first and get here with just numbers on value
    for k,v in data_list[0].items():
        if type(v) is not dict:
            #print("{} is not a dict".format(k))
            #print("Setting {} to {}".format(k,v))
            #Time taken for tests seconds
            #Requests per second #/sec (mean)
            #Transfer rate 194.21 [Kbytes/sec] received
            if k in units.keys():
                unit = units[k]
                k+= " "+unit
            if len(re.findall(float_regex,v)) > 0:
                mean[k] = float(re.findall(float_regex,v)[0])
            elif len(re.findall(int_regex,v)) > 0:
                mean[k]=int(re.findall(int_regex,v)[0])
        else:
            
            for kk,vv in v.items():
                if k not in mean.keys():
                    mean[k] = {}
                    
                if type(vv) is not dict:
                    #requests[Complete] requests["Failed"]
                    #transferred[Total] bytes transferred["HTML"] bytes
                    if kk in units:
                        unit = units[kk]
                        kk += " "+unit
                    if len(re.findall(float_regex,vv)) > 0:
                        mean[k][kk] = float(re.findall(float_regex,vv)[0])
                    elif len(re.findall(int_regex,vv)) > 0:
                        mean[k][kk] = int(re.findall(int_regex,vv)[0])
                    print(mean)
                else:
                    if kk not in mean[k].keys():
                        mean[k][kk] = {}
                    for kkk,vvv in vv.items():
                        #Connection Times ms
                        #Percentage of the requests served within a certain time
                        #check if they are all ints dont do extra code below
                        if len(re.findall(float_regex,vvv)) > 0:
                            mean[k][kk][kkk] = float(re.findall(float_regex,vvv)[0])
                        elif len(re.findall(int_regex,vvv)) >0:
                            mean[k][kk][kkk] = int(re.findall(int_regex,vvv)[0])
    #show_data(mean)
    #set all keys to 0
    for data in data_list:
        for k,v in data.items():
            if type(v) is not dict:
                #print("{} is not a dict".format(k))
                #print("Setting {} to {}".format(k,v))
                #Time taken for tests seconds
                #Requests per second #/sec (mean)
                #Transfer rate 194.21 [Kbytes/sec] received
##            if k in units.keys():
##                unit = units[k]
##                k+= " "+unit
                if len(re.findall(float_regex,v)) > 0:
                    mean[k] += float(re.findall(float_regex,v)[0])
                elif len(re.findall(int_regex,v)) > 0:
                    mean[k]+=int(re.findall(int_regex,v)[0])
            else:
                for kk,vv in v.items():
                    if type(vv) is not dict:
                        #requests[Complete] requests["Failed"]
                        #transferred[Total] bytes transferred["HTML"] bytes
##                        if kk in units:
##                            unit = units[kk]
##                            kk += " "+unit
                        if len(re.findall(float_regex,vv)) > 0:
                            mean[k][kk] += float(re.findall(float_regex,vv)[0])
                        elif len(re.findall(int_regex,vv)) > 0:
                            mean[k][kk] += int(re.findall(int_regex,vv)[0])
                    else:
                        for kkk,vvv in vv.items():
                            #Connection Times ms
                            #Percentage of the requests served within a certain time
                            if len(re.findall(float_regex,vvv)) > 0:
                                mean[k][kk][kkk] += float(re.findall(float_regex,vvv)[0])
                            elif len(re.findall(int_regex,vvv)) >0:
                                mean[k][kk][kkk] += int(re.findall(int_regex,vvv)[0])


    #show_data(mean)
    #divide by amount
    #trunc decimal
    for k,v in mean.items():
        if type(v) is not dict:
            if len(re.findall(float_regex,str(v))) > 0:
                mean[k] /= amount
                mean[k] = trunc_num(mean[k])
            elif len(re.findall(int_regex,str(v))) > 0:
                mean[k] //=amount
                mean[k] = trunc_num(mean[k])
        else:
            for kk,vv in v.items():
                if type(vv) is not dict:
                    if len(re.findall(float_regex,str(vv))) > 0:
                        mean[k][kk] /= amount
                        mean[k][kk] = trunc_num(mean[k][kk])
                    elif len(re.findall(int_regex,str(vv))) > 0:
                        mean[k][kk] //= amount
                        mean[k][kk] = trunc_num(mean[k][kk])
                else:
                    for kkk,vvv in vv.items():
                        #Connection Times ms
                        #Percentage of the requests served within a certain time
                        if len(re.findall(float_regex,str(vvv))) > 0:
                            mean[k][kk][kkk] /= amount
                            mean[k][kk][kkk] = trunc_num(mean[k][kk][kkk])
                        elif len(re.findall(int_regex,str(vvv))) >0:
                            mean[k][kk][kkk] /= amount
                            mean[k][kk][kkk] = trunc_num(mean[k][kk][kkk])
    #divide all by amount and change units
    show_data(mean)
    return mean
    #reformat data

def format_data(data,server_name):
    print(data)
    #takes server
    #three csv
    #if path is not dir
    folder = os.path.join(".\\data",server_name)
    if not os.path.isdir(folder):
        os.makedirs(folder)

    
    #make folder for each case
    
    #Percentage of the requests served within a certain time (ms)
    
    with open(os.path.join(folder,"served.csv"),"w",newline='') as f:
        writer = csv.writer(f,delimiter=",")
        
        writer.writerow(["Percentage of requests","Time (ms)"])
        for k,v in data["Percentage of the requests served within a certain time (ms)"].items():
            writer.writerow([k.replace("%",""),v])
    #Connection Times (ms)
    #type,measure,value
    with open(os.path.join(folder,"Connectiontimes.csv"),"w",newline="") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow(["Type","Measure","Value"])
        for t,d in data["Connection Times (ms)"].items():
            for k,v in d.items():
                writer.writerow([t,k,v])
                
            
            
    
    

    other_data_keys = ["Requests per second (#/sec)",
                       "Time per request (ms) (mean)",
                       "Time per request (ms) (mean, across all concurrent requests)",
                       "Transfer rate (Kbytes/sec)",
                       "Time taken for tests (seconds)"
                       ]
    other_data = [ [i,data[i]] for i in data.keys() if i in other_data_keys]
    with open(os.path.join(folder,"other.csv"),"w",newline='') as f:
        writer = csv.writer(f,delimiter=",")
        for d in other_data:
            writer.writerow(d)
        

    #other data
    #could output to json or plain text as dict
    
        
    
    
    
    pass
    #already finished data 
  
def run_tests(amount,n,c,dst):
    
    command = "ab -n {} -c {} {}".format(n,c,dst)

    data_list = []

    final_data = {}
    #parse output by name of result instead of index due to optional arguments appearing
    

    for i in range(amount):
        result =subprocess.check_output(command,shell=True,text=True)
        result = [i for i in result.split("\n") if i != ""]
        result = result[0:1] + result[4:]
        data = {}

##        for i,line in enumerate(result):
##            print(i,line)

        #sequence
        if i == 0:
            #set to final data
            #since this arguments dont change throughout the test
            #apache data 0
            apache_version,apache_revision = result[0].split(",")[1].strip().split("<$")
            avk,avv = apache_version.split()
            final_data[avk] = avv
            apache_revision = apache_revision.replace("$>","")
            set_data(final_data,apache_revision)
            
            #server info, software, hostname, port 1 2 3
            #document path document length 4 5
            set_data_objects(final_data,result[1:6])
        
        #time taken for tests 7
        set_data(data,[i for i in result if "Time taken for tests" in i][0])
        #complete and failed requests 8 9
        set_data_objects_reverse(data,[i for i in result if "Complete requests" in i or "Failed requests" in i])
        #Total transferred 10
        #HTML transferred 11
        #set here then take to module
        #transferred
        #transferred(bytes)
        #-HTML
        #-Total
        data["Transferred (bytes)"] = {}
        for item in [i for i in result if "transferred" in i]:
            k,v = [i.strip() for i in item.split(":")]
            data["Transferred (bytes)"][k.split()[0]] = v.split()[0]
                
            
##        #set_data_objects_reverse(data,result[10:12])

##        #requests per second 12
##        set_data(data,result[12])
##        #time per request 13
##        #time per request 14
##        set_data(data,result[13])
##        set_data(data,result[14])
##        

        #transfer rate 15
##        set_data(data,result[15])
        requests_data = ["Requests per second","Time per request","Transfer rate"]
        for i in [x for x in result if x.split(":")[0] in requests_data]:
            set_data(data,i)
     

        #turn to csv
        #connection times 16
        #Columns 17
        #connect
        #processing
        #waiting
        #total
        connection_times_i = result.index("Connection Times (ms)")
        connection_times = result[connection_times_i]
        data[connection_times] = {}
        cols = ["min","mean","[+/-sd]","median","max"]
        for row in result[connection_times_i+2:connection_times_i+1+ len(cols)]:
            print(row)           
            k,v =  row.split(":")
            data[connection_times][k] = {}
            v = v.split()
            for i,col in enumerate(cols):
                data[connection_times][k][col] = v[i].strip()

        #Percentage of
        #the requests served within a certain time (ms)
        requests_percentage_i = result.index("Percentage of the requests served within a certain time (ms)")
        requests_percentage = result[requests_percentage_i].strip()
        data[requests_percentage] = {}
        for row in result[requests_percentage_i+1:requests_percentage_i+10]:
            k,v = row.strip().split() if "100%" not in row else row.replace("(longest request)","").strip().split()
            data[requests_percentage][k] = v
        

        data_list.append(data)
    return get_mean(data_list,amount)
    #final data return mean of all data in a readable form
    #see what data is relevant for http web server benchmarking
    #which assets to use in benchmarking for static and which website to use for dynamic
            
#arguments from command line
#-s server_name
#-n amount of requests
#-c concurrency level
#-a amount of tests to run
#-s mandatory
#if -s is not in servernames display server names to test

servers = {"apache/php":"Apache with php",
           "nginx/php":"Nginx with php",
           "nginx/python":"Nginx with python socket server",
           "apache/python":"Apache with python socket server",
           "node.js":"Node server",
           "Rust":"Http Rust server",
           "Go":"Http golang server",
           "Python":"Http python server built with sockets"
    }
def show_available_servers():
    print("-"*20)
    for k,v in servers.items():
        print("|{}:{}|".format(k,v))
    print("-"*20)
parser = argparse.ArgumentParser()
parser.add_argument("-s","--server_name",help="Server name to benchmark")
parser.add_argument("-n","--requests",help="Amount of requests to perform using apache benchmark")
parser.add_argument("-c","--concurrency",help="Concurrency level")
parser.add_argument("-a","--tests",help="Amount of tests to run")
parser.add_argument("-d","--default",help="Use default config file")
parser.add_argument("-dst","--ip",help="IP of server to benchmark")
#parser.add_argument("-h","--help",help="Display help about CLI")

args = parser.parse_args()

a = 0
c = 0
n = 0
server_name = ""
print(args.default)
if(args.default == "y"):
    with open("./benchmark.conf","rt") as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            if row[0] == "n":
                n = int(row[1])
            elif row[0] == "c":
                c = int(row[1])
            elif row[0] == "a":
                a = int(row[1])
    #set values to default config file
    
else:
    #set values
    #if any of these is none
    

    if not args.requests or not args.concurrency or not args.tests:
        print("Error, missing parameters")
        exit()
        
    n= int(args.requests)
    c= int(args.concurrency)
    a=int(args.tests)
    
    pass
    
print(n,c,a)

if not args.server_name:
    print("Error, did not specify server name")
    exit()
    #error and show message
else:
    server_name = args.server_name
    if server_name not in servers.keys():
        print("Error, server name not found")
        
        #print server names available
        show_available_servers()
        exit()

if not args.ip:
    print("Error ip not provided")
else:
    IP = args.ip
        
    #find server in server_names

    paths= {"apache/php":"index.php",
               "nginx/php":"index.php",
               "nginx/python":"",
               "apache/python":"",
               "node.js":"",
               "Rust":"",
               "Go":"",
                "Python":""}



    #specify dest in
    #IP = "192.168.1.147"
    #PATH =paths[server_name]
    format_data(run_tests(a,n,c,IP),server_name)

        
    
