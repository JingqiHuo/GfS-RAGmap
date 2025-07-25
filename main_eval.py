from retrieval_agent import database_query
from taskentity_agent import agent1
from taskentity_agent_gpt import agent2
import time
from config.config import *

def processing(user_input):
    start_idf = time.perf_counter()

    # choose agent1 for deepseek/ agent2 for chatgpt
    if LLM == 'agent1':
        test_agent = agent2()
    elif LLM == 'agent2':
        test_agent = agent2()
    intention_json = test_agent.agent_json("1st_idf", user_input)
    print(intention_json)
    end_idf = time.perf_counter()

    query_type = intention_json["retrieval"]
    print(f"RAG? {query_type}")
    retrieved = []
    if query_type == 'no':
        start_nl = time.perf_counter()
        task_nl = test_agent.agent_default(user_input)
        end_nl = time.perf_counter()
    else:
        # Search agent initialization
        return_intro = database_query()
        print("extracting location names...")

        extraction = intention_json["places"]
        vector = False
        matched = ''
        if extraction:
            for k in extraction:
                #print(k)

                # keyword match
                intro = return_intro.rag_workflow(k,user_input)
                if intro != '[] []':
                    matched = f"{matched} \n {intro}"
                #print(intro)
                elif intro =='[] []':
                    vector = True
                
        print(matched)
        # vector search
        if vector:
            k=''
            intro = return_intro.rag_workflow(k,user_input)
            matched = f"{matched} \n {intro}"
        
        retrieved = [matched]
        # Append user's query to the rag prompt
        matched = f"{matched} \n {user_input}"
        print(type(matched))
        print(matched)

        # Tell the task type
        # If task is nothing with routing or other special tasks, just call the points\
        start_json = time.perf_counter()
        end_json = time.perf_counter()

        start_integrate = time.perf_counter()
        task_nl = test_agent.agent_nl("info_integration", matched)
        end_integrate = time.perf_counter()
        print(task_nl)
        start_map = time.perf_counter()
        end_map = time.perf_counter()
        print(f"task identification: {end_idf-start_idf:.6f}s")
        print(f"JSON output: {end_json-start_json:.6f}s")
        print(f"Info integration: {end_integrate-start_integrate:.6f}s")
        print(f"Map making: {end_map-start_map:.6f}s")
    return task_nl,retrieved