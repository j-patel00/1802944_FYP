import time
import datetime
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pandas as pd#Used to make dataframe from txt files which is in CSV format

import numpy as np

from matplotlib import pyplot as plt
import matplotlib as mpl

import getpass


#######################################################################
#Below you can change directory to store log file, and the files name
completeName = (os.path.join("/var/www/html", "log.txt"))#Sets directory to path, file called log.txt
#######################################################################

file = open(completeName, "a")#Opens filename in set directory, appends to file named
df = pd.read_csv ('log.txt',  header=None, names=['Date','Time','Event','Location','Username'])#creates datafram with each column having the following names

print (df)#shows initial data structure before launch of live monitoring
####################################################################################
#Event frquency bar graph
event_freq = df['Event'].value_counts().plot(kind='bar', title='Most common event type', xlabel='Events', fontsize=18)
event_freq.set_xlabel("Event Type")
plt.xticks(rotation=30)
fig = event_freq.get_figure()
fig.savefig("event_frequency.png", pad_inches=0.3, dpi=300, bbox_inches='tight')
plt.close()

#event pie chart
event_pie = df['Event'].value_counts().plot(kind='pie')
fig2 = event_pie.get_figure()
fig2.savefig("event_pie.png", pad_inches=0.3)
plt.close()

#most active users
user_act = df['Username'].value_counts().plot(kind='bar', title='Active Users', xlabel='Users', fontsize=18)
plt.xticks(rotation=30)
fig3 = user_act.get_figure()
fig3.savefig("user_active.png", pad_inches=0.3, dpi=300, bbox_inches='tight')
plt.close()
####################################################################################

class Watcher:#Monitor for events

    def __init__(self, directory, handler=FileSystemEventHandler()):
             
        self.observer = Observer()
        self.handler = handler
        ######################################################################
        #Point to directory you want to monitor
        self.directory = (r"/home/Files/")#Directory to monitor
        ######################################################################

    def run(self):
        
        self.observer.schedule(
            self.handler, self.directory, recursive=True)#Recursive=True includes all subfolders, False will ignore subfolers
        self.observer.start()
        
        print("\nWatcher Running in {}\n".format(self.directory))#Shell outputs script is running and monitoring location
        
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):#What to do in response to event

    def on_any_event(self, event): #type = ['created', 'deleted', 'modified', 'moved', 'closed']
                                   #These are the event types which can be monitored

            #print date, time, event type, event location to shell
            #prints as a csv

            #for debugging to console#
            print(f'{datetime.datetime.now().strftime("%d-%b-%Y,(%H:%M:%S)")},{event.event_type},{event.src_path},{os.getlogin()}')
            
            #On any event type write to log file with date and time, event type, event path
            file.write(f'{datetime.datetime.now().strftime("%d-%b-%Y,%H:%M:%S")},{event.event_type},{event.src_path},{os.getlogin()}\n')
            file.flush()#Empties buffer by writing to file

            #Example of custom responses to an event
            #if event.event_type == "deleted": 
            #    print("Oh no! It's gone!")

if __name__=="__main__":
    w = Watcher(".", MyHandler())
    w.run()





