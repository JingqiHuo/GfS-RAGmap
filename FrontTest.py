import gradio as gr
import folium
from folium.plugins import MarkerCluster
from make_map import make_map
import folium
from retrieval_agent import database_query
from taskentity_agent import agent1
import re
import json
import time
def processing(user_input):
    start_idf = time.perf_counter()
    test_agent = agent1()
    task_html= None
    intention_json = test_agent.agent_json("1st_idf", user_input)
    #print(intention_json)
    end_idf = time.perf_counter()

    #intention = json.loads(intention_json)
    query_type = intention_json["retrieval"]
    print(f"RAG? {query_type}")
    if query_type == 'no':
        start_nl = time.perf_counter()
        task_nl = test_agent.agent_default(user_input)
        end_nl = time.perf_counter()
    else:
        # Search agent initialization
        return_intro = database_query()
        print("extracting location names...")

        extraction = intention_json["places"]

        matched = []
        geo_entities = []
        if matched:
            for k in extraction:
                print(k)

                # keyword match
                intro, geo_info = return_intro.rag_workflow(k,user_input)

                # combine the matched intros and coordinates
                matched.append(intro)
        else:
            k=''
            intro, geo_info = return_intro.rag_workflow(k,user_input)
            matched = intro
        if isinstance(geo_info,list):
            for i in geo_info:
                geo_entities.append(i)                     
        else:

            geo_entities.append(geo_info)

        # Append user's query to the rag prompt
        matched.append(user_input)
        geo_entities.append(user_input)

        # Strings processing, extract texts and append to list
        texts = []
        for item in matched:
            match = re.search(r'"\s*(.*?)\s*"', item)
            if match:
                texts.append(match.group(1))
            elif item.strip():  
                texts.append(item.strip())

        # 2. Integrate as NL
        combined_text = " ".join(texts)
        #print(geo_entities)
        combined_geo = " ".join(geo_entities)
        #print(combined_geo)
        #print(combined_text)

        # Tell the task type
        # If task is nothing with routing or other special tasks, just call the points\
        start_json = time.perf_counter()
        task_json = test_agent.agent_json("task_idf", combined_geo)
        end_json = time.perf_counter()
        
        start_integrate = time.perf_counter()
        task_nl = test_agent.agent_nl("info_integration", combined_text)
        end_integrate = time.perf_counter()
        #print(combined_text)
        print(task_json)
        print(task_nl)
        start_map = time.perf_counter()
        folium_map = make_map()
        task_html = folium_map.make_map(task_json)
        end_map = time.perf_counter()
        print(f"task identification: {end_idf-start_idf:.6f}s")
        print(f"JSON output: {end_json-start_json:.6f}s")
        print(f"Info integration: {end_integrate-start_integrate:.6f}s")
        print(f"Map making: {end_map-start_map:.6f}s")
    return task_nl, task_html

with gr.Blocks() as demo:

    # Gradio frontend component
    gr.Markdown("Demo")
    user_input = gr.Textbox(label="Please enter your question")
    btn = gr.Button("Submit")
    output_text = gr.Textbox(label="Answer")
    output_map = gr.HTML(label="Map Display")

    btn.click(fn=processing, inputs=user_input, outputs=[output_text, output_map])

demo.launch(share=True)


    