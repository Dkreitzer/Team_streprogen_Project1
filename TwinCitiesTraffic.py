
# coding: utf-8

# In[1]:


import pandas as pd
import os
import xml.etree.ElementTree as ET
import gzip
import time
import shutil
import requests


# In[2]:


def download():
    
    i = requests.get('http://data.dot.state.mn.us/iris_xml/incident.xml.gz')
    with open('data/XMLs/incidents.xml', 'w') as handle:
        handle.write(gzip.decompress(i.content).decode('utf-8'))
    d = requests.get('http://data.dot.state.mn.us/iris_xml/det_sample.xml.gz')
    with open('data/XMLs/det_sample.xml', 'w') as handle:
        handle.write(gzip.decompress(d.content).decode('ISO-8859-1'))
    s = requests.get('http://data.dot.state.mn.us/iris_xml/stat_sample.xml.gz')
    with open('data/XMLs/stat_sample.xml', 'w') as handle:
        handle.write(gzip.decompress(s.content).decode('ISO-8859-1'))


# In[3]:


def data_check():

        try:
            with open('data/crash_data.csv', 'r') as CD:
                incidents()
        except FileNotFoundError:
                All_Crash_Data = pd.DataFrame(columns=['Name', 'Date', 'DirectionLocation', 'Road', '', 'Event'])
                with open('data/crash_data.csv', 'w') as f:
                    All_Crash_Data.to_csv(f, header=True)
                    incidents()
        try:
            with open('data/detector_data.csv', 'r') as CD:
                detectors()
        except FileNotFoundError:
                Detector_Data = pd.DataFrame(columns=['Sensor', 'Time', 'Occupancy', 'Speed', 'Flow'])
                with open('data/detector_data.csv', 'w') as f:
                    Detector_Data.to_csv(f, header=True)
                    detectors()
        try:
            with open('data/station_data.csv', 'r') as CD:
                stations()
        except FileNotFoundError:
                station_data = pd.DataFrame(columns=['Station', 'Time', 'Occupancy', 'Speed', 'Flow'])
                with open('data/station_data.csv', 'w') as f:
                    station_data.to_csv(f, header=True)
                    stations()


# In[4]:


def stations():
        
        stations = []
        times = []
        flows = []
        occupancies = []
        speeds = []
        
        XMLfile = "data/XMLs/stat_sample.xml"
        parsedXML = ET.parse(XMLfile)
        root = parsedXML.getroot()
        for child in root:
            try:
                stations.append(child.attrib['sensor'])
            except KeyError:
                stations.append("NA")
            try:
                times.append(str(root.attrib['time_stamp']))
            except KeyError:
                times.append("NA")
            try:
                flows.append(child.attrib['flow'])
            except KeyError:
                flows.append("NA")
            try:
                occupancies.append(child.attrib['occ'])
            except KeyError:
                occupancies.append('NA')
            try:
                speeds.append(child.attrib['speed'])
            except KeyError:
                speeds.append("NA")


        DF = pd.DataFrame({"Station" : stations,
                            "Time" : times,
                           "Occupancy": occupancies,
                           "Speed" : speeds,
                           "Flow" : flows})

        print("Station Data Parsed")

        with open('data/station_data.csv', 'a') as f:
            DF.to_csv(f, header=False)
            


# In[5]:


def incidents():

        dates = []
        incident_dirs = []
        roads = []
        locations = []
        names = []
        events = []
        
        XMLfile = "data/XMLs/incidents.xml"
        parsedXML = ET.parse(XMLfile)
        root = parsedXML.getroot()
        for child in root:
            try:
                dates.append(child.attrib['event_date'])
            except KeyError:
                dates.append("NA")
            try:
                names.append(str(child.attrib['name']))
            except KeyError:
                name.append("NA")
            try:
                incident_dirs.append(child.attrib['dir'])
            except KeyError:
                incident_dir.append("NA")
            try:
                roads.append(child.attrib['road'])
            except KeyError:
                roads.append('NA')
            try:
                locations.append(child.attrib['location'])
            except KeyError:
                locations.append("NA")
            try: 
                event = child.attrib['event_type'].split("_", 1)
                events.append(event[1])
            except KeyError:
                events.append("NA")


        DF = pd.DataFrame({"Name" : names,
                           "Date" : dates,
                           "Direction": incident_dirs,
                           "Road" : roads,
                           "Location" : locations,
                           "Event" : events})


        print("Incident Data Parsed")

        with open('data/crash_data.csv', 'a') as f:
            DF.to_csv(f, header=False)
      


# In[6]:


def detectors():
        
        sensors = []
        times = []
        flows = []
        occupancies = []
        speeds = []
        
        XMLfile = "data/XMLs/det_sample.xml"
        parsedXML = ET.parse(XMLfile)
        root = parsedXML.getroot()
        for child in root:
            try:
                sensors.append(child.attrib['sensor'])
            except KeyError:
                sensors.append("NA")
            try:
                times.append(str(root.attrib['time_stamp']))
            except KeyError:
                times.append("NA")
            try:
                flows.append(child.attrib['flow'])
            except KeyError:
                flows.append("NA")
            try:
                occupancies.append(child.attrib['occ'])
            except KeyError:
                occupancies.append('NA')
            try:
                speeds.append(child.attrib['speed'])
            except KeyError:
                speeds.append("NA")



        DF = pd.DataFrame({"Sensor" : sensors,
                            "Time" : times,
                           "Occupancy": occupancies,
                           "Speed" : speeds,
                           "Flow" : flows})

        print("Detector Data Parsed")

        with open('data/detector_data.csv', 'a') as f:
            DF.to_csv(f, header=False)
      


# In[7]:


def config():
    
        decription = []
        station = []
        lats = []
        lngs = []
        
        XMLfile = "data/XMLs/station_config.xml"
        parsedXML = ET.parse(XMLfile)
        root = parsedXML.getroot()
        
        for child in root:
            try:
                lats.append(child.attrib['lat'])
            except KeyError:
                continue
            try:
                lngs.append(child.attrib['lon'])
            except KeyError:
                continue
            
            try:
                decription.append(child.attrib['description'])
            except KeyError:
                    decription.append("error")

        
            try:
                station.append(child.attrib['name'])
            except KeyError:
                station.append("error")                
                
                ### NODE NAMES ARE FOUND IN CHILD[0][X]#####
            
      
        DF = pd.DataFrame({"Label" : decription,
                           "Sensor" : station,
                           "Lat": lats,
                           "Lng" : lngs})
        
        DF = DF.dropna(thresh=2)

        with open('data/station_config.csv', 'a') as f:
            DF.to_csv(f, header=False)


# In[8]:


c = requests.get('http://data.dot.state.mn.us/iris_xml/metro_config.xml.gz')
with open('data/XMLs/station_config.xml', 'w') as handle:
    handle.write(gzip.decompress(c.content).decode('utf-8'))


# In[9]:


def Route_Summary():
    try:
        with open('station_config.csv', 'r') as CD:
            config()
    except FileNotFoundError:
            Station_Data = pd.DataFrame(columns=['Label', 'Detectors', 'Lat', 'Lng'])
            with open('data/station_config.csv', 'w') as f:
                Station_Data.to_csv(f, header=True)
                config()
    All_Station_Data = pd.read_csv('data/station_data.csv')
    All_Station_Data = All_Station_Data[["Station", "Time", "Occupancy", "Speed", "Flow"]]
    All_Station_Data = All_Station_Data.set_index('Station')
    # Route_Name = input("  Name Your Route")
    Route = [584,567,583,568,582,569,570,581,580,571,579,572,578,573,577,587]
    Route_Summary = []
    for station in Route:
            Route_Summary.append(All_Station_Data.loc['S'+ str(station), ['Time', 'Occupancy', 'Speed', 'Flow']])
    # for Summary in Route_Summary:
        ## WHAT ARE WE DOING WITH THESE?##
    print(Route_Summary[0])


# In[ ]:


while True:
    download()
    data_check()
    print("Parsing Complete, sleeping 30s")
    print("First Sensor In Route Summary")
    Route_Summary()
    time.sleep(30)

