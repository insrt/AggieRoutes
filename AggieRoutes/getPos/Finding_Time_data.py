from urllib.request import urlopen
import numpy as np
import bs4 as bs
import pandas as pd 
import json

route = ["12","15",'22','25','26','27','31','34','35','36','40','47','N15','01','01-04','02','03','03-05','04','05','06','07','08'] # list of buss routs 
path = "C:\\Users\\ripti\\Desktop\\Stock_proj\\running_bus_data" # save path for your computer (saves .csv for every route)
Data_Frame_List = [] # list of dataframes that have time data in them
def TimeData(Bus_route):
    #print("STARTING SEARCH") 
    search_url = "https://transport.tamu.edu/busroutes/Routes.aspx?r="+Bus_route # path to wevsight wiht changeable route

    html = urlopen(search_url).read() # reads the html file
    soup = bs.BeautifulSoup(html,"lxml") # gets all data
    table = soup.find("div", {"id":"TimeTable"}) # finda locaion for time table in list

    # initalises the list that will hold data
    header = []
    dataList = []

    head =  table.findAll("th")# finds headers
    data =  table.findAll("td")# finds data  
    
    for i in head: # adds head to list as a string only keeping informa as "text"
        header.append(str(i.text))
 
    for i in data:# adds data to list as a string only keeping informa as "text"
        dataList.append(str(i.text))     
    
    if header[0][0] !="L": # breaks for no time data for route
        #print(dataList[0] +" on Bus Route: "+ Bus_route)
        return 0


    if dataList[0] != "\xa0": # takes out random spaces
        header = header[2:] # deleates first bit of text
        dataList= dataList[0:-2] # deleats un readable end characters
    else:
        header = header[2:] # deleates first bit of text
        dataList= dataList[2:] # deleats un readable end characters
 

    def divide_chunks(l,n):  # brakes long string into a matrix
    
        # looping till length l 
        for i in range(0, len(l),n):  
            yield l[i:i + n] 
    def twenty_four(l):# convertes to 24 hour time
        
        for i in range(len(l)):# handles AM
            if l[i][-1] == 'A' or l[i][:2] == "12" :
                l[i] = l[i][:-1] # excludes "A"
            else:# handles PM
                l[i] = l[i][:-1] #excludes the lase letter "P" (AM/PM)
                time = l[i].split(":") # splits at ":"
                time[0] = str(int(time[0]) + 12) # adds 12 to make 24 hour time
                if time[0] == 24:# sets time to "00:xx"
                    time[0] == '00' 
                l[i] = ':'.join(time) # joins and adds ":"
        return l # returns new list 
            
    New = twenty_four(dataList) # converts data to 24 hour time
  
    n = len(header) # number of stops
    PF_data = list(divide_chunks(New,n)) # properly formats the data

    pandaTit = pd.DataFrame(header).transpose() # transposes the header so it is a row instad of a colomb

    pandadat = pd.DataFrame(PF_data) # creates a dataframe for the data
    df = pd.concat([pandaTit, pandadat]).reset_index(drop = True)  # concatanates the lists
    
    row = df[0].count()# finds the number of rows for identifyign time and busrouts
    df2 = df.assign(bus = [Bus_route for i in range(row)]) # adds buss data
    #print(df2)
    
    Data_Frame_List.append(df2) # appends buss route list with dataframe of time information 
  

    
num_routes = str(len(route))# total number of 

for i in range(len(route)): # runs though all data (buss routes)

    #string = str(i+1)+"/"+num_routes+" |"+route[i]+"| " # formats the start of the search so the 
    #print(string, end="") # shows the bus route number
    TimeData(route[i]) # Sends route data to be found


with open(path+".json", 'w') as outfile:# opens a file path to dump the .jason file
        outfile.write(json.dumps([df.to_dict() for df in Data_Frame_List])) # creats a dictionry of the informaiot then dumps into a .jason