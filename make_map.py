import folium

"""
This class is used to add elements to the map
according to the GeoJSON received from Google_call.py
"""

class make_map(object):

    def __init__(self):

        pass



    def make_map(self,tasks):

        first = tasks['features'][0]['geometry']['coordinates']
        m = folium.Map(location=[first[1], first[0]], zoom_start=10)

        folium.GeoJson(
            tasks,
            name="geojson",
            tooltip=folium.GeoJsonTooltip(fields=["Name"]),
            popup=folium.GeoJsonPopup(fields=["Introduction"])
        ).add_to(m)

        return m._repr_html_()