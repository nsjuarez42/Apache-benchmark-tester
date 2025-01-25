import os
import subprocess
import csv
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def series_mean_to_float(lst):
    return float(pd.Series(lst).mean())

def to_csvs(data,directory):
    server = data["server"]
    del data["server"]
    means = {}
    prst= "Percentage of the requests served within a certain time (ms)"
    ctms = "Connection Times (ms)"
    for k,v in data.items():
        print(k,v)
        if 'amounts' in v.keys():
            means[k] = {'mean':series_mean_to_float(v['amounts']),'unit':v['unit']}
        elif k == prst:
            served = {}
            for percentage,values in v.items():
                served[percentage] = series_mean_to_float(values)
            means[prst] = served
        elif k == ctms:
            connection_times = {}
            for connection_type,measures in v.items():
                print("Connection {} measures {}".format(connection_type,measures))
                connection_times[connection_type] ={"min":series_mean_to_float(measures['min']),
                       "mean":series_mean_to_float(measures['mean']),
                       "median":series_mean_to_float(measures['median']),
                       'max':series_mean_to_float(measures['max']),
                       '[+/-sd]':series_mean_to_float(measures['[+/-sd]'])
                       }
            means[ctms]=connection_times
    folder = os.path.join(directory,"csvs")
    if not os.path.isdir(folder):
        os.makedirs(folder)

    for k,v in means.items():
        print(k,v)

    connection_types = ["Connect","Waiting","Total","Processing"]
    connection_filepaths = [os.path.join(folder,i+".csv") for i in connection_types]
    for path in connection_filepaths:
        print(path)
        columns = ["Server","min","mean","[+/-sd]","median","max"]
        if not os.path.isfile(path):
            #write empty file
            with open(path,"w",newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                conn_type = [i for i in connection_types if i in path][0]
                row = [server,
                       means[ctms][conn_type]["min"],
                       means[ctms][conn_type]["mean"],
                       means[ctms][conn_type]["[+/-sd]"],
                       means[ctms][conn_type]["max"]]
                writer.writerow(row)
                
                #write the columns server and all data in order
        else:
            with open(path,"a",newline='') as f:
                writer = csv.writer(f)
                conn_type = [i for i in connection_types if i in path][0]
                row = [server,
                       means[ctms][conn_type]["min"],
                       means[ctms][conn_type]["mean"],
                       means[ctms][conn_type]["[+/-sd]"],
                       means[ctms][conn_type]["max"]]
                writer.writerow(row) 
            #read and write file
    results_file_path = os.path.join(folder,"Results.csv")
    print(results_file_path)
    results_columns = ["Server","Time taken for tests","Requests per second","Time per request","Time per request (concurrent)","Transfer rate"]
    if not os.path.isfile(results_file_path):
        with open(results_file_path,"w",newline='') as f:
            writer =csv.writer(f)
            writer.writerow(results_columns)
            row= [
                server,
                *[means[i]['mean'] for i in results_columns[1:]]
            ]
            writer.writerow(row)

    else:
        with open(results_file_path,"a",newline='') as f:
            writer =csv.writer(f)
            row= [
                server,
                *[means[i]['mean'] for i in results_columns[1:]]
            ]
            writer.writerow(row)
    requests_served_path = os.path.join(folder,"Served.csv")
    #write columns instead of rows
    if not os.path.isfile(requests_served_path):
        with open(requests_served_path,"w",newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Percentage of requests",server])
            for k,v in means[prst].items():
                writer.writerow([k.replace("%",""),v])
        
    else:
        file_contents = []
        with open(requests_served_path,"r",newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                file_contents.append(row)
        print(file_contents)
        with open(requests_served_path,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([*file_contents[0],server])
            for i,value in enumerate(means[prst].values()):
                writer.writerow([*file_contents[i+1],value])

    for k,v in means.items():
        print(k,v)
    
    #get mean 
    #csvs 
    #results 
    #and pass to csvs
    #dont do join csvs
    pass

def run_tests(amount,n,c,dst,server,path):

    #make a series for each data point 
    # and then add the mean to final 

    #ab -n {} -c {} -e {}.csv -g {}.tsv {} 
    
    command = "ab -n {} -c {} {}".format(n,c,dst)

    data = {"server":server}

    for i in range(amount):
        output = subprocess.check_output(command,shell=True,text=True)
        print("output #{}".format(i))
        #save apache output in plain text to verify results
        folder = os.path.join(path)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(os.path.join(folder,'test{}.txt'.format(i)),"wt") as f:
            f.write(output)

        output = output.split("\n")

        output = [i for i in output[[z for z,x in enumerate(output) if "Time taken for tests" in x][0]:] if i !=""]

        def to_number(string):
            if string.find(".") != - 1:
                return float(string)
            else:
                return int(string)
       
        connection_times_i,served_i = [i for i,v in enumerate(output) if "Connection Times (ms)" in v or "Percentage of the requests" in v]

        for line in output[:connection_times_i]:
            measure,amount = line.split(":")
            amount = amount.strip().split(" ")
            amount,unit = to_number(amount[0])," ".join(amount[1:])
            print("Measure {} amount {} unit {}".format(measure,amount,unit))
          
            if measure == "Time per request" and unit != "[ms] (mean)":
                measure = "Time per request (concurrent)"
            
            if measure not in data.keys():
                data[measure] = {"amounts":[amount],"unit":unit}
            else:
                data[measure]['amounts'].append(amount)
        for line in output[connection_times_i+2:served_i]:
            print("Connection line",line)
            k= "Connection Times (ms)"
            connection_type,measures = line.split(":")
            print("Connection_type {} measures {}".format(connection_type,measures))
            measures = re.findall(r'[0-9]+[.]*[0-9]*',measures.strip())
         
            min,mean,sd,median,maximum = [to_number(i) for i in measures]
            times = {"min":[min],"mean":[mean],"[+/-sd]":[sd],"median":[median],"max":[maximum]}

            if k not in data.keys():
                data[k] = {connection_type:times}
            else:
                if connection_type not in data[k]:
                    data[k][connection_type] = times 
                else:
                    data[k][connection_type]['min'].append(min)
                    data[k][connection_type]['mean'].append(mean)
                    data[k][connection_type]['[+/-sd]'].append(sd)
                    data[k][connection_type]['median'].append(median)
                    data[k][connection_type]['max'].append(maximum)
        for line in output[served_i+1:]:
            k = "Percentage of the requests served within a certain time (ms)"
            print("get percentage from",line)
            percentage,amount = line.strip().replace(" ","").split("%")
            if k not in data.keys():
                data[k] = {percentage+"%":[to_number(amount)]}
            else:
                if percentage == "100":
                    amount = amount.replace("(longestrequest)","")
                amount = to_number(amount)
                if percentage+"%" not in data[k].keys():
                    data[k][percentage+"%"] = [amount]
                else:
                    print(data[k][percentage+"%"])
                    data[k][percentage+"%"].append(amount)
    return data
        #do means and pass data to csvs

#arguments from command line
#-s server_name
#-n amount of requests
#-c concurrency level
#-a amount of tests to run
#-s mandatory
#if -s is not in servernames display server names to test

servers = {"apache/php/fpm":"Apache with php",
           "nginx/php":"Nginx with php",
           "apache/php":"Apache with python socket server",
           "apache":"Apache server",
           "nginx":"Nginx with python socket server",
           "node.js":"Node server",
           "rust":"Http Rust server",
           "go":"Http golang server",
           "python":"Http python server built with sockets"
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
        
    #if data folder does not exist create it
    #find server in server_names
    paths = {"apache/php/fpm":"./data/outputs/apache_php_fpm",
           "nginx/php":"./data/outputs/nginx_php",
           "apache/php":"./data/outputs/apache_php",
           "apache":"./data/outputs/apache",
           "nginx":"./data/outputs/nginx",
           "node.js":"./data/outputs/node",
           "rust":"./data/outputs/rust",
           "go":"./data/outputs/go",
           "python":"./data/outputs/python"
    }

    tests_directory = paths[server_name]
    results_directory = "./data"

    to_csvs(run_tests(5,n,c,IP,server_name,tests_directory),results_directory)

        
    
