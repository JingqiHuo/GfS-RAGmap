import requests
import polyline

"""
This class is used to call Google map API and return
 formatted GeoJSON data in order to map a map
"""

class ApiMaps:
    def __init__(self,api_key):
        self.api_key = api_key
        self.features = []  # dynamically collect Feature

    def draw_polyline(self, origin, destination):

        # Construct api and send request
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data['routes']:
            raise Exception("Route not found!")

        # Decode the returned json data
        encoded_polyline = data['routes'][0]['overview_polyline']['points']
        coords = polyline.decode(encoded_polyline)

        # Construct feature data (structured)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[lng, lat] for lat, lng in coords]
            },
            "properties": {
                "origin": origin,
                "destination": destination,
                "distance": data['routes'][0]['legs'][0]['distance']['text'],
                "duration": data['routes'][0]['legs'][0]['duration']['text']
            }
        }

        # Append the current feature to the feature list
        self.features.append(feature)
        return feature

    def draw_point(self, name, descr, coord_str):
        """
        Draw Points according to the coordinates in the format of string
        """
        # Decode the string coordinates
        try:
            lat_str, lng_str = coord_str.split(",")
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
        except Exception as e:
            raise ValueError(f"Coordinates format error, should be: 'lat,lng', currently: {coord_str}") from e

        # Construct feature data (structured)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]  # GeoJSON 为 [lng, lat]
            },
            "properties": {
                "name": name,
                "description": descr
            }
        }

        # Append the current feature to the feature list
        self.features.append(feature)
        return feature



    def draw_polygon(self, name, coord_list):
        """
        Recieve multiple strings, and generate Polygon Feature
        """

        # Decode the string coordinates
        coordinates = []
        for coord_str in coord_list:
            lat, lng = map(float, coord_str.split(","))
            coordinates.append([lng, lat])  # GeoJSON 用 [lng, lat]
        
        # Construct feature data (structured)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]  
            },
            "properties": {
                "name": name
            }
        }

        # Append the current feature to the feature list
        self.features.append(feature)
        return feature


    def get_feature_collection(self):
        """
        get complete FeatureCollection
        """
        
        return {
            "type": "FeatureCollection",
            "features": self.features
        }
    



    def process_tasks(self, task_list):
        """
        Loop over the task list and automatically select the right method
        """

        for task in task_list:
            if task["type"] == "point":
                self.draw_point(task["name"], task["description"], task["coord"])
            elif task["type"] == "polyline":
                self.draw_polyline(task["origin"], task["destination"])
            elif task["type"] == "polygon":
                self.draw_polygon(task["name"], task["coords"])
            else:
                print(f"Unknown task type: {task['type']}")

    