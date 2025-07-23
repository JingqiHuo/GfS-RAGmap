from openai import OpenAI
from secrets_retrieval import get_APIkey
import json
class chatgptProcess(object):
        
    def __init__(self,system_prompt,user_prompt):
        
        self.client = OpenAI(
            api_key=get_APIkey('/Path/to/OpenAI.txt')
            
        )

        self.system_prompt = system_prompt

        self.user_prompt = user_prompt
    
    def rqtcall(self):

        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}]

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        #print(response)
        return json.loads(response.choices[0].message.content)
    
    def rqtcall_nl(self):

        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt}]

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content
    
    def rqtcall_default(self):

        messages = [{"role": "user", "content": self.user_prompt}]
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content
    
    
