import json
import calendar
from datetime import datetime
from pyproj import Proj, transform

# Path where the input file is located
path_input_file = 'manzanas_pob.JSON'

# Input and output coordinates format
inpProj = Proj(init='epsg:25830')
outProj = Proj(init='epsg:4326')

# Read input file
print ("Reading input file...")

with open(path_input_file,"r") as input_file:
    data = json.load(input_file)

# Converting coordinates format
print("Converting coordinates format...")

result = {}
result['type'] = data['type']
result['crs'] = data['crs']
result['features'] = []

for feature in data['features']:
    coordinates = []
    for coordinate in feature['geometry']['coordinates'][0]:
        x1, y1 = coordinate[0], coordinate[1]
        x2, y2 = transform(inpProj, outProj, x1, y1)
        coordinates.append([x2, y2])
    feature['geometry']['coordinates'] = [coordinates]
    result['features'].append(feature)    

# Change CRS to indicate the new coordinates format 
result['crs']['properties']['name'] = "urn:ogc:def:crs:EPSG::4326" 

# Write output file
print('Writting output file...')

date = str(datetime.now())
date = date.replace("-", "")
date = date.replace(":", "")
date = date.replace(".", "")
date = date.replace(" ", "")

path_output_file = 'manzanas_pob_'+date+'.JSON'

with open(path_output_file, "w") as output_file:
    json.dump((result), output_file, indent=3)

# Ready
print("Ready")

    
