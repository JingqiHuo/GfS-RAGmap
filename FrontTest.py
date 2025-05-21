import gradio as gr
import folium
from folium.plugins import MarkerCluster
from make_map import make_map
import folium
from retrieval_agent import database_query
from taskentity_agent import agent1
import re


# Search agent initialization
return_intro = database_query()
print("extracting location names...")
test_agent = agent1()
extraction = test_agent.agent_json("entity_extraction",text2)

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
#print(combined_text)
print(task_json)
print(task_nl)
folium_map = make_map()
folium_map.make_map(task_json)