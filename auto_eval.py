import cx_Oracle
from secrets_retrieval import get_password
import json
import random
import re
import json
from main_eval import processing
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision
)
from taskentity_agent import agent1



##############################################################
#               PART I Data Preparation                      #
##############################################################
def data_prep(row_num):
    # 1. Construct Answer set (randomly pick 50 entries)
    print("Connecting to Oracle database...")
    password = get_password('/home/s2630332/gfs/ApiKeys/database.txt')
    conn = cx_Oracle.connect(user="s2630332", password=password, dsn="geosgen")
    cursor = conn.cursor()
    print('Successfully connected to Oracle database.')
    cursor.execute("""
                   SELECT NAME, INTRODUCTION FROM ops$scotgaz.towns 
                   WHERE INTRODUCTION IS NOT NULL AND LENGTH(INTRODUCTION)
                    > 20 AND LENGTH(INTRODUCTION) < 500
                   """)
    rows = cursor.fetchall()
    print('Successfully get metadata from gazetteer.')
    sampled_entries = random.sample(rows,row_num)
    #print(sampled_entries)

    # 2. call an LLM to generate questions and answers
    # Prepare several lists
    count = 1
    qa_agent = agent1()
    questions = []
    contexts = []
    answers = []
    entries = []
    pattern = re.compile(r"Q:\s*(.*?)\s*A:\s*(.*)", re.DOTALL)
    for i in sampled_entries:
        print(count)
        print(i)
        combined_i = f"{i[0]}.{i[1]}"
        print(combined_i)
        response = qa_agent.qa_test(combined_i)
        match = pattern.search(response)
        if match:
            q = match.group(1).strip()
            a = match.group(2).strip()
            questions.append(q)
            answers.append(a)
            contexts.append(i[1])

        count+=1

    # 3. Construct JSON
    for q, a, ctx in zip(questions, answers, contexts):
        entry = {
            "query": q,
            "answer":a,
            "context": ctx
        }
        entries.append(entry)
    print(entries)
    # 4. Save to JSON
    json_str = json.dumps(entries, indent=2)
    print(json_str)

    standarized_data = []
    json_data = json.loads(json_str)
    for item in json_data:
        standarized_data.append(
            {
                "query": item["query"],
                "ground_truths": [item["answer"]],
                "contexts": [item["context"]],
            }
        )

    with open("rageval_qaset.json","w") as f:
        json.dump(standarized_data, f, indent = 2)

##############################################################
#               PART II Answer Generation (RAG)              #
##############################################################
def ans_gen(path_to_qaset):
    with open(path_to_qaset,"r") as f:
        qaset = json.load(f)

    for item in qaset:
        text_ans,retrieved = processing(item["query"])
        print(text_ans)
        item["predicted_answer"] = text_ans
        item["retrieved"] = retrieved
    
    with open("qa_with_pred.json", "w", encoding="utf-8") as f:
        json.dump(qaset, f, indent=2, ensure_ascii=False)

##############################################################
#               PART III Post-integration                    #
##############################################################
def integrate():
    # 1. Load QA set (reference) and prediction set
    with open("rageval_qaset.json", "r", encoding="utf-8") as f:
        qaset = json.load(f)

    with open("qa_with_pred.json", "r", encoding="utf-8") as f:
        qa_withpred = json.load(f)

    # 2. format
    eval_map = {item["query"]: item for item in qa_withpred}

    # 3. integrate into a dictionary, which ragas need
    combined = []
    for item in qaset:
        query = item["query"]
        if query in eval_map:
            entry = eval_map[query]
            
            combined.append({
                "user_input": query,
                "reference": " ".join(entry["ground_truths"]),
                "retrieved_contexts": entry.get("retrieved"),  
                "answer": entry.get("predicted_answer")
            })

    # 4. save as json file
    with open("eval_ready.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Integration complete, {len(combined)} entries written into eval_ready.json")

##############################################################
#               PART IV evaluation                          #
##############################################################
def eval():
    # load json
    data = json.load(open("eval_ready.json", encoding="utf-8"))
    ds = Dataset.from_list(data)

    # execute evaluation
    results = evaluate(
        ds,
        metrics=[faithfulness, answer_relevancy, context_recall, context_precision],
        raise_exceptions=False
    )

    df = results.to_pandas()
    df.to_csv("eval_results.csv", index=False)


#data_prep(50)
ans_gen("rageval_qaset.json")
integrate()
eval()