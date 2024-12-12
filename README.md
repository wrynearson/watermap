# Water Map

https://wrynearson.github.io/watermap/

Drinking water, plus toilets and benches, on a 3D map using data from [OpenStreetMap](https://www.openstreetmap.org/). For more information, see [this post](https://wrynearson.github.io/watermap-project/).

<img width="1818" alt="image" src="https://github.com/user-attachments/assets/5970608d-1ee6-42f9-a4c7-986019b9a29e">

_Water and toilets are currently limited to Europe, and benches are currently limited to Switzerland_.

## Features
1. See drinking water, toilets and benches easily
2. (optional) show your location on the map, to see nearby data points
3. Enable terrain data to see these data points in 3D.
4. Click on any point to see its OSM ID.

## Motivation

When traveling or hiking, I often look for fountains to refill my water bottle. I didn't find a map or app to quickly find drinking water sources near me, so I decided to build one.

Nature also sometimes calls at inopportune times, so toilets are also displayed. Having a nice bench to sit on is also nice, so those were added as well.

Seeing this data in 3D is helpful when hiking or doing outdoor sports.

I wanted this to be entirely open source, and free to build/maintain. More about this below.

## Data Sources
1. Basemap – [OpenFreeMap](https://openfreemap.org/)
2. Mapping Library – [MapLibre](https://maplibre.org/)
3. Terrain Data – [Tilezen (and sources)](https://github.com/tilezen/joerd/blob/master/docs/attribution.md)
4. Data – OpenStreetMap (via [Geofabrik](https://www.geofabrik.de/en/index.html))

## Process
_This could be improved. Feel free to reach out if you have any suggestions!_

1. OSM .pbf data is downloaded from [Geofabrik](https://www.geofabrik.de/en/index.html) (currently only for Switzerland, but will likely be expanded).
2. Relevant data is extracted from .pbf using [Osmium](https://osmcode.org/osmium-tool/) and the relevant OSM tags.
    - Water: `drinking_water = yes`, `amenity = drinking_water`
    - Toilets: `building = toilets`, `amenity = toilets`
    - Benches: `amenity = bench`, `leisure = picnic_table`
3. Extracted data is converted to .geojson files in https://github.com/wrynearson/watermap/blob/main/data_exploration/osm.ipynb
    - Each extracted .pbf (e.g., drinking_water.pbf) has its geometry types, stored as layers (['points', 'lines', 'multilinestrings', 'multipolygons']), are extracted and processed in a geodataframe.
    - Each geodataframe's geometry and OSM ID (currently only relevant for points) are saved in a .geojson. One per geometry type and per data type (e.g., drinking_water_points.geojson, drinking_water_multipolygons.geojson, etc.)
4. Each geojson is "tiled" using [tippecanoe](https://github.com/felt/tippecanoe).
    - All geometry types for each data type are combined into a tileset, resulting in one tileset per data type (drinking_water, toilets, benches)
5. Data is visualized using pure javascript (currently all in index.html)
6. Site is deployed using Github pages
