import json
import datetime
import pandas as pd
import sys


# First, we load the data into memory 
data = [json.loads(line) for line in open('data.txt', 'r')]

# then, we trasnforme the data in json format to dataframe format
# satart a new dataframe only with the variables that we need
dataframe = pd.DataFrame(columns=['time', 'duration'])

# Adding the information into the dataframe
for i in range(0, len(data) ) :  	
    dataframe = dataframe.append({'time' : data[i]['timestamp'], 'duration' : data[i]['duration'],} , ignore_index=True)

# We sort the Dataframe ordering by datetime
dataframe = dataframe.sort_values(by=['time'])

# we get the begning and ending date
firstdate = datetime.datetime.strptime(  dataframe['time'] .iloc[0]  ,  '%Y-%m-%d %H:%M:%S.%f' )
lastdate = datetime.datetime.strptime(  dataframe['time'] .iloc[ len(data) - 1 ]  ,  '%Y-%m-%d %H:%M:%S.%f' )

# we need the ,inute so now we get just the begining and ending date
firstmin = firstdate.minute
lastmin = lastdate.minute

# We get the argument number that willl define the window of the moving average
argument = sys.argv[1]

# we start some variables that we going to need
sum = 0
cnt = 0
arrowup = 0
arrowdown = 0

# we are going to print all the minutes starting from the first to the last  
for i in range(firstmin , lastmin+2) :
    # for the first case, the min is 0
    if (i == firstmin):
        {"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
        print( '{"date":' + str(firstdate.year) + "-" + str(firstdate.month) + "-" + str(firstdate.day) + " " +  str(firstdate.hour) + ":" + str(i)  + ':00 , "average_delivery_time" :' + str(cnt)  + "}")
    
    # for every other case,we add em remove a minute
    else: 
        newmember = 0
        # we just need to add the 'i' minuto value into our cnt and sum 
        while (newmember > -1):
            minuto = datetime.datetime.strptime(  dataframe['time'] .iloc[arrowup+newmember]  ,  '%Y-%m-%d %H:%M:%S.%f' ).minute 
            if(minuto== i-1):
                sum +=  int (dataframe['duration'] .iloc[arrowup+newmember] )
                cnt += 1
                newmember += 1 
                if (arrowup+newmember == len(data)):
                    newmember = -1
            else:
                arrowup = arrowup + newmember
                newmember = -1
                
        
        # now we need to remove the value of the last value (not included in the window when recalculated with the new interaction
		window = i - int ( argument ) 

        # we get the last value that doesnt belong in the window and subtract from our cnt and sum
        newmember = 0
        while (newmember > -1):
            if (datetime.datetime.strptime(  dataframe['time'] .iloc[arrowdown+newmember]  ,  '%Y-%m-%d %H:%M:%S.%f' ).minute== window-1):
                sum -=  int ( dataframe['duration'] .iloc[arrowdown+newmember]  )
                cnt -= 1
                newmember += 1 
            else:
                arrowdown = arrowdown + newmember
                newmember = -1
         
        # for each minutes, we calculate the average included in the window previous calculated
        res = float ( sum )  / float( cnt )
        print( '{"date":' + str(firstdate.year) + "-" + str(firstdate.month) + "-" + str(firstdate.day) + " " +  str(firstdate.hour) + ":" + str(i)  + ':00 , "average_delivery_time" :' + str(res)  + "}")