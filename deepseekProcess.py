import json
from openai import OpenAI
from secrets_retrieval import get_APIkey

"""
This class is used to process the prompt.
GPT will parse the user's prompt (Points or Routes)
 and return formatted JSON data
"""

class deepseekProcess(object):
        
    def __init__(self,system_prompt,user_prompt):
        
        self.client = OpenAI(
            api_key=get_APIkey('/Path/to/DeepSeek.txt'),
            base_url="https://api.deepseek.com/v1",
        )

        self.system_prompt = system_prompt

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
    
    def rqtcall_nl(self):

        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}]

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return response.choices[0].message.content
    
    def rqtcall_default(self):

        messages = [{"role": "user", "content": self.user_prompt}]
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return response.choices[0].message.content
    
    

