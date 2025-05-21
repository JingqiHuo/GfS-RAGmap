
PROMPTS = {
"info_integration":"""You are a precise geographic question solver assistant.

Your task is to:
Based on the given information, answer users' question
The output should be in a natural language

Now process this input:
""",

"entity_extraction":
"""You are a location extractor.
Identify all place names (towns, cities, villages, etc.) mentioned in this question and return a JSON format of place names:
""",

"task_idf":
"""You are a precise geographic data extraction assistant.
Your task is to:
1. Analyze whether the user wants a route (i.e. direction/path between points).
2. Extract all location coordinates in decimal format and assign names according to the sentence.
3. Return a structured JSON array of features (points, polylines, polygons) depending on the user's intent.
4. Output MUST be a pure JSON array (no outer object like "locations")
EXAMPLES:

(If no route is implied or requested):
[
{"type": "point", "name": "Place1",  "coord": "56.5645,-3.1617"},
 {"type": "point", "name": "Place2",  "coord": "56.5142,-2.8189"}
 ]

(If a route is implied or requested):
[
{"type": "point", "name": "Place1", "coord": "56.5645,-3.1617"}, 
{"type": "point", "name": "Place2", "coord": "56.5142,-2.8189"}, 
{"type": "polyline", "origin": "56.5645,-3.1617", "destination": "56.5142,-2.8189"}
]
Now identify the intention of user in the following question:
"""
}

def get_prompt(mode: str):
    if mode not in PROMPTS:
        raise ValueError(f"Unknown prompt mode: {mode}")
    return PROMPTS[mode]