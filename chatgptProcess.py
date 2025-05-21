import openai
from secrets_retrieval import get_APIkey

openai.api_key = get_APIkey('/home/s2630332/gfs/ApiKeys/OpenAI.txt')

def extract_locations_from_text(text):
    prompt = f"""
你是一位擅长地理信息提取的助手。请从下面文本中提取出每个地名及其对应的坐标（纬度，经度），格式如下：

[
  {{ "name": "地名", "coord": "纬度,经度" }}
]

请仅输出 JSON 数组，不需要其他解释。

文本如下：
---
{text}
---
    """

    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    result = response['choices'][0]['message']['content']
    return result  # 你可以进一步 json.loads(result) 处理为 Python 对象

# 测试用例
sample_text = """
A small hamlet located close to the western boundary of Angus, Newbigging lies a half-mile (1 km) northwest of Newtyle (Angus), 1¼ miles (2 km) east of Ardler and 1½ miles (2.5 km) south of Meigle in Perth and Kinross. Coordinates are 56.5645°N, 3.1617°W.
"""

print(extract_locations_from_text(sample_text))

#models = openai.Model.list()
#print(models)