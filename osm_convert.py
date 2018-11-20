import pickle
import sys
import xml.etree.ElementTree as et

name = sys.argv[1]

print('Parsing osm.xml file ...')

# Parse osm.xml file
tree = et.parse('osm_maps/%s.osm.xml' % (name))
root = tree.getroot()

print('Creating dictionary of all nodes ...')

# Create dictionary of all nodes in the map (by id)
nodes = {}
for node in root.findall('node'):
    id = node.get('id')
    lat = float(node.get('lat'))
    lon = float(node.get('lon'))
    nodes[id] = (lat, lon)

print('Building streets from OSM ways ...')

# Build all streets from OSM ways
streets = []
for way in root.findall('way'):
    for tag in way.findall('tag'):
        if tag.get('k') == 'highway':
            line = []
            for nd in way.findall('nd'):
                coords = nodes[nd.get('ref')]
                line.append(coords)
            
            speedlimit = 50.0  # Default speed limit if no speed limit is provided by OSM
            for tag in way.findall('tag'):
                if tag.get('k') == 'maxspeed':
                    tag_string = tag.get('v').split(';')[0]
                    try:
                        speedlimit = int(tag_string)
                    except ValueError:
                        if tag_string.endswith('mph'):
                            speedlimit = 1.609 * int(tag_string[:-4])
    
            streets.append({'speedlimit': speedlimit, 'line': line})

print('Writing data to pickle ...')

# Write street data to pickle
with open('osm_maps/streets_%s.pkl' % (name), 'wb') as file:
    pickle.dump(streets, file)

print('Writing data to nested list .data file for BerlinMod ...')

# Write street data to nested list .data file for BerlinMod
with open('berlinmod/streets_%s.data' % (name), 'w') as file:
    file.write('\n')
    file.write('(OBJECT streets \n')
    file.write('    () \n')
    file.write('    (rel \n')
    file.write('        (tuple \n')
    file.write('            (\n')
    file.write('                (Vmax real) \n')
    file.write('                (GeoData line)))) \n')
    file.write('    (')
    
    for street in streets:
        file.write('\n')
        file.write('        (%.1f \n' % (street['speedlimit']))
        file.write('            (')
        
        for i in range(len(street['line']) - 1):
            a = street['line'][i]
            b = street['line'][i + 1]
            file.write(' \n')
            file.write('                (%f %f %f %f)' % (a[1], a[0], b[1], b[0]))
        file.write('))')
        
    file.write('))\n')

    print('...done!')