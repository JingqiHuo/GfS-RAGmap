from Google_call import ApiMaps
from nlpProcess import nlpProcess
from make_map import make_map
import folium
import pprint
from deepseekProcess import deepseekProcess
from retrieval_agent import database_query
from prompt_management import get_prompt
from taskentity_agent import agent1
import re

#text1 = """
#Edinburgh is Scotland's capital, celebrated globally for its rich history, stunning architecture, and vibrant cultural scene. Situated on a series of hills between the Firth of Forth to the north and the Pentland Hills to the south, it is home to over 500,000 people. Once known for biscuits, brewing, banking, and books, Edinburgh's economy now thrives in finance, science, tourism, and the professions. It is the UK's second-largest financial hub and Europe's fourth-largest. The city also hosts the Scottish Parliament, reaffirming its role as a political center. Edinburgh's retail scene is dominated by Princes Street and major shopping complexes. Its industries include information technology, renewable energy, and life sciences, epitomized by the Edinburgh BioQuarter. Coordinates: 55.9523°N, 3.1882°W..
#Dingwall is a historic burgh town in Highland Council Area, located at the head of the Cromarty Firth, 10 miles northwest of Inverness. Its name originates from Scandinavian words meaning 'parliament in the valley.' With royal burgh status since 1226, Dingwall has a rich history as a market center and administrative seat. The town gained prominence in the 18th and 19th centuries due to linen spinning, its status as a road and railway junction, and its role in livestock markets. In the 1970s, the North Sea oil boom further fueled its growth. Dingwall hosts the Highland Traditional Music Festival and Highland Games, with landmarks including Tulloch Castle and St Clement's Church. Coordinates: 57.5957°N, 4.4327°W.
#
#Please tell me how to get to Dingwall from Edinburgh.      
#"""
## processor = nlpProcess(text)
## tasks = processor.process()
#text2 = """
#Newbigging (Near Newtyle, Western Angus)Coordinates: 56.5645°N, 3.1617°WThis small hamlet is close to the western boundary of Angus.It lies half a mile (1 km) northwest of Newtyle, 1¼ miles (2 km) east of Ardler, and 1½ miles (2.5 km) south of Meigle in Perth and Kinross.The surrounding landscape is mostly farmland and rolling countryside, with Newtyle being a historically important village in the region.
#Newbigging (Near Monikie, Southeastern Angus)Coordinates: 56.5142°N, 2.8189°WThis village is located 1¼ miles (2 km) south of Monikie and 2 miles (3 km) east-southeast of Wellbank.It grew significantly in the 1950s, when public housing was built, increasing its population.Nearby are the Carlungie and Ardestie souterrains, which are Iron Age underground structures likely used for storage or ritual purposes.Stone quarrying has been an important local industry in the area.
#Newbigging (Near Tealing, Southern Angus)Coordinates: 56.5268°N, 2.9395°WThis hamlet is immediately east of the A90 trunk road, one of Scotland’s main north-south highways.It lies half a mile (1 km) southeast of Tealing and 4 miles (6.5 km) north of Dundee.The surrounding area features agriculture, rural homes, and proximity to Dundee’s outskirts.
#
#Tell me about Newbiggings in Angus
#"""

#system_prompt = get_prompt("entity_extraction")
#print(system_prompt)

#print(extraction['place_names'][0])
#rag_processor = database_query(text2)
#rag_prompt = rag_processor.rag_workflow()


#q1 = database_query("Edinburgh")
#print(q1.rag_workflow(1))

text1 = """
how to get to Dingwall from Edinburgh 
"""
text2 = """
Tell me about dingwall and edinburgh
"""

# Search agent initialization
return_intro = database_query()
print("extracting location names...")
test_agent = agent1()
extraction = test_agent.agent_json("entity_extraction",text1)

matched = []
geo_entities = []
for k in extraction['place_names']:
    print(k)

    # keyword match first



    # if nothing matched, fallback to Vector search here
    intro, geo_info = return_intro.rag_workflow(k)
    
    # combine the matched intros and coordinates
    matched.append(intro)
    geo_entities.append(geo_info)

# Append user's query to the rag prompt
matched.append(text2)
geo_entities.append(text2)

print(geo_entities)
#task = test_agent.agent_json("task_idf",geo_entities)

texts = []
for item in matched:
    # 正则提取括号内的引号内容，或直接保留纯文本
    match = re.search(r'"\s*(.*?)\s*"', item)
    if match:
        texts.append(match.group(1))
    elif item.strip():  # 添加非空的用户问题等部分
        texts.append(item.strip())

# 2. 整合为一段自然语言
combined_text = " ".join(texts)
combined_geo = " ".join(geo_entities)
print(combined_geo)
#print(combined_text)

# Tell the task type
# If task is nothing with routing or other special tasks, just call the points
task_json = test_agent.agent_json("task_idf", combined_geo)
task_nl = test_agent.agent_nl("info_integration", combined_text)
print(combined_text)
print(task_json)
print(task_nl)


            