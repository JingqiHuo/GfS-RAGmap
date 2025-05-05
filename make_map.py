from Google_call import ApiMaps    
import folium

"""
This class is used to add elements to the map
according to the GeoJSON received from Google_call.py
"""

class make_map(object):

    def __init__(self,api_key):
        # Construct Apimaps instance
        self.maps = ApiMaps(api_key=api_key)



    def make_map(self,tasks):

        
        # Allocate methods for tasks
        self.maps.process_tasks(tasks)

        # Get the full FeatureCollection
        geojson_all = self.maps.get_feature_collection()

        # Show the map
        # Decide the center location
        first = geojson_all['features'][0]['geometry']['coordinates']
        m = folium.Map(location=[first[1], first[0]], zoom_start=10)

        for feature in geojson_all['features']:
            coords = feature['geometry']['coordinates']
            props = feature['properties']
            gtype = feature['geometry']['type']

            if gtype == "Point":
                folium.Marker(
                    location=[coords[1], coords[0]],
                    popup=folium.Popup(f"<b>{props['name']}</b></br>{props['description']}", max_width=200),
                    tooltip=props['name']
                ).add_to(m)

            elif gtype == "LineString":
                folium.PolyLine(
                    locations=[[lat, lng] for lng, lat in coords],
                    
                    weight=4,
                    popup=folium.Popup(f"Route: {props.get('distance', 'duration')}", max_width=200)
                ).add_to(m)
        return m