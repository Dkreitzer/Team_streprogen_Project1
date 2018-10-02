
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
    with open('incidents.xml', 'w') as handle:
        handle.write(gzip.decompress(i.content).decode('utf-8'))
    d = requests.get('http://data.dot.state.mn.us/iris_xml/det_sample.xml.gz')
    with open('det_sample.xml', 'w') as handle:
        handle.write(gzip.decompress(d.content).decode('ISO-8859-1'))


# In[3]:


def data_check():
        XMLfile = "incident.xml"
        try:
            with open('crash_data.csv', 'r') as CD:
                incidents()
        except FileNotFoundError:
                All_Crash_Data = pd.DataFrame(columns=['Name', 'Date', 'Direction', 'Road', 'Location', 'Event'])
                with open('crash_data.csv', 'w') as f:
                    All_Crash_Data.to_csv(f, header=True)
                    incidents()
        XMLfile = "det_sample.xml"
        try:
            with open('detector_data.csv', 'r') as CD:
                detectors()
        except FileNotFoundError:
                Detector_Data = pd.DataFrame(columns=['Sensor', 'Time', 'Occupancy', 'Speed', 'Flow'])
                with open('detector_data.csv', 'w') as f:
                    Detector_Data.to_csv(f, header=True)
                    detectors()


# In[4]:


def incidents():
        XMLfile = "incidents.xml"


        dates = []
        incident_dirs = []
        roads = []
        locations = []
        names = []
        events = []

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

        print(DF)

        print("Incident Data Parsed")

        with open('crash_data.csv', 'a') as f:
            DF.to_csv(f, header=False)


# In[11]:


def detectors():
        
        sensors = []
        times = []
        flows = []
        occupancies = []
        speeds = []
        XMLfile = "det_sample.xml"

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
                flows.append(child.attrib['sample flow'])
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

        print(DF)
        print("Detector Data Parsed")

        with open('detector_data.csv', 'a') as f:
            DF.to_csv(f, header=False)


# In[6]:


def stations():
        XMLfile = "stat_config.xml"

        decription = []
        times = []
        detectors = []
        lats = []
        lngs = []

        parsedXML = ET.parse(XMLfile)
        root = parsedXML.getroot()
#         print(root.findall("./time_stamp"))
        for child in root:
            try:
                decription.append(child.attrib['description'])
            except KeyError:
                decription.append("NA")
            try:
                times.append(str(root.attrib['tms_config_time_stamp']))
            except KeyError:
                times.append("NA")
            try:
                detectors.append(child.attrib['name'])
            except KeyError:
                detectors.append("NA")
            try:
                lats.append(child.attrib['lat'])
            except KeyError:
                lats.append('NA')
            try:
                lngs.append(child.attrib['lon'])
            except KeyError:
                lngs.append("NA")



        DF = pd.DataFrame({"Label" : decription,
                           "Sensor" : detectors,
                            "Time" : times,
                           "Lat": lats,
                           "Lng" : lngs})
        
        DF = DF.dropna(thresh=2)
        print(DF)


        with open('stat_config.csv', 'a') as f:
            DF.to_csv(f, header=False)


# In[7]:


s = requests.get('http://data.dot.state.mn.us/iris_xml/metro_config.xml.gz')
with open('stat_config.xml', 'w') as handle:
    handle.write(gzip.decompress(s.content).decode('utf-8'))

XMLfile = "stat_config.xml"
try:
    with open('stat_config.csv', 'r') as CD:
        stations()
except FileNotFoundError:
        Station_Data = pd.DataFrame(columns=['Label', 'Time', 'Detectors', 'Lat', 'Lng'])
        with open('stat_config.csv', 'w') as f:
            Station_Data.to_csv(f, header=True)
            stations()


# In[9]:


while True:
    download()
    print("download complete")
    data_check()
    print("Parsing Complete, sleeping 30s")
    time.sleep(30)

