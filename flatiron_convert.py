import xml.etree.ElementTree as ET
tree = ET.parse('Flatiron.osm')
root = tree.getroot()
import pandas as pd
df = pd.DataFrame()
idd =[]
lat = []
lon = []
for child in root.findall('node'):
    idd.append(int(child.attrib['id']))
    lat.append(float(child.attrib['lat']))
    lon.append(float(child.attrib['lon']))
df['nodeid'] =idd
df['lat'] =lat
df['lon'] =lon
df['nodeid'] = df['nodeid'].astype(int)
df.sort_values('lon')
df.to_csv('flatiron.csv', index = False)
