import json
from openai import OpenAI
from secrets_retrieval import get_APIkey
"""
This class is used to process the prompt.
GPT will parse the user's prompt (Points or Routes) and return formatted JSON data
"""


class deepseekProcess(object):
        
    def __init__(self,user_prompt):
        
        self.client = OpenAI(
            api_key=get_APIkey('E:\GfS-RAG-Map-Return\ApiKeys\DeepSeek.txt'),
            base_url="https://api.deepseek.com/v1",
        )

        self.system_prompt = """
You are a precise geographic data extraction assistant.

Your task is to:
1. Analyze whether the user wants a route (i.e. direction/path between points).
2. Extract all location coordinates in decimal format and assign names according to the sentence.
3. Return a structured JSON array of features (points, polylines, polygons) depending on the user's intent.
4. Output MUST be a pure JSON array (no outer object like "locations")
Format your output EXACTLY as a JSON array and same as EXAMPLES. Each object must contain:
- 'type': one of ['point', 'polyline', 'polygon']
- 'name': e.g., "Place1", "Place2", "Route1", etc.
- 'description': description of the place, extract directly from prompt
- For 'point', use 'coord': "<lat>,<long>"
- For 'polyline', use 'origin' and 'destination'
- For 'polygon', use 'coords': [ "<lat>,<long>", ... ] (should be a closed ring)

EXAMPLES:

(If only coordinates are present):
[
  {"type": "point", "name": "Place1", "description": "description of Place1", "coord": "56.5645,-3.1617"},
  {"type": "point", "name": "Place2", "description": "description of Place2", "coord": "56.5142,-2.8189"}
]

(If a route is implied or requested):
[
  {"type": "point", "name": "Place1", "coord": "56.5645,-3.1617"},
  {"type": "point", "name": "Place2", "coord": "56.5142,-2.8189"},
  {"type": "polyline", "origin": "56.5645,-3.1617", "destination": "56.5142,-2.8189"}
]

Now process this input:
"""

        self.user_prompt = user_prompt
    
    def rqtcall(self):

        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}]

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )

        #print(json.loads(response.choices[0].message.content))
        return json.loads(response.choices[0].message.content)
    
    def extract_features(self):
        """
        Extract the 'features' array from the model returns (if exsits), or directly return the array
        Make sure to return a pure list
        """

        model_output=self.rqtcall()

        if isinstance(model_output, str):
            model_output = json.loads(model_output)

        if isinstance(model_output, dict) and 'features' in model_output:
            return model_output['features']

        if isinstance(model_output, list):
            return model_output

        # Error handling
        raise ValueError("Output format error!")
