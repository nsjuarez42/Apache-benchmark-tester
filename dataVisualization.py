import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./data/csvs/results.csv")

print(pd.DataFrame({"Time"}))

print(df.iloc[:,1])
print(df)
#print(df.sort_values(by=,axis=0))

def plot_connection_times():
    fig,axes = plt.subplots(ncols=2,nrows=2)
    #fig2,axes2 = plt.subplots(ncols=1,nrows=2)
    
    
    cdf = pd.read_csv("./data/csvs/Connect.csv")
    wdf = pd.read_csv("./data/csvs/Waiting.csv")

    pdf= pd.read_csv("./data/csvs/Processing.csv")
    tdf = pd.read_csv("./data/csvs/Total.csv")

    
    cdf = pd.DataFrame({"min":list(cdf.iloc[:,1]),
                        "mean":list(cdf.iloc[:,2]),
                        "[+/-sd]":list(cdf.iloc[:,3]),
                        "median":list(cdf.iloc[:,4]),
                        "max":list(cdf.iloc[:,5])},index=cdf["Server"])
    cdf = cdf.plot.bar(rot=0,ax=axes[0,0])
    cdf.set_xlabel("Server")
    cdf.set_ylabel("Connect times (ms)")
    cdf.set_title("Connection times (ms)")
    

    wdf = pd.DataFrame({"min":list(wdf.iloc[:,1]),
                        "mean":list(wdf.iloc[:,2]),
                        "[+/-sd]":list(wdf.iloc[:,3]),
                        "median":list(wdf.iloc[:,4]),
                        "max":list(wdf.iloc[:,5])},index=wdf["Server"])
    wdf = wdf.plot.bar(rot=0,ax=axes[1,0])
    wdf.set_xlabel("Server")
    wdf.set_ylabel("Waiting times (ms)")
    wdf.set_title("Waiting times (ms)")

    pdf = pd.DataFrame({"min":list(pdf.iloc[:,1]),
                        "mean":list(pdf.iloc[:,2]),
                        "[+/-sd]":list(pdf.iloc[:,3]),
                        "median":list(pdf.iloc[:,4]),
                        "max":list(pdf.iloc[:,5])},index=pdf["Server"])
    pdf = pdf.plot.bar(rot=0,ax=axes[0,1])
    pdf.set_xlabel("Server")
    pdf.set_ylabel("Processing times (ms)")
    pdf.set_title("Processing times (ms)")

    tdf = pd.DataFrame({"min":list(tdf.iloc[:,1]),
                        "mean":list(tdf.iloc[:,2]),
                        "[+/-sd]":list(tdf.iloc[:,3]),
                        "median":list(tdf.iloc[:,4]),
                        "max":list(tdf.iloc[:,5])},index=tdf["Server"])
    tdf = tdf.plot.bar(rot=0,ax=axes[1,1])
    tdf.set_xlabel("Server")
    tdf.set_ylabel("Total times (ms)")
    tdf.set_title("Total times (ms)")

print("iloc 0")
print(df.iloc[:,0])
for i in range(1,6):
    print("Iloc {}".format(i))
    print(df.iloc[:,i].sort_values())



plot_connection_times()

rdf = pd.DataFrame({"Time taken for tests ": list(df.iloc[:,1])},index=df['Server'])
rdf.plot.bar(rot=0)

ndf = pd.DataFrame({"Requests per second": list(df.iloc[:,2]),
                   "Transfer rate (kbytes/sec)":list(df.iloc[:,5])},
                   index=df["Server"])
ndf.plot.bar(rot=0)

xdf = pd.DataFrame({"Time per request (ms)":list(df.iloc[:,3])
                    ,"Time per request (ms, concurrent)":list(df.iloc[:,4])},
                   index=df["Server"])
xdf.plot.bar(rot=0)

#works for current data
line_chart_df = pd.read_csv("./data/csvs/Served.csv")
print(line_chart_df)
print(line_chart_df.sort_values(by="Percentage of requests"))
line_chart_df.plot(x="Percentage of requests",
                   y=[i for i in line_chart_df.columns if "Percentage of requests" not in i],
                   figsize=(10,5))


#processing of data saved using pandas
#parse through and do mean of csvs

plt.show()