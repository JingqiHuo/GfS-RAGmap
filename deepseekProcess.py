import json
from openai import OpenAI
from secrets_retrieval import get_APIkey

"""
This class is used to process the prompt.
GPT will parse the user's prompt (Points or Routes) and return formatted JSON data
"""

class deepseekProcess(object):
        
    def __init__(self,system_prompt,user_prompt):
        
        self.client = OpenAI(
            api_key=get_APIkey('/home/s2630332/gfs/ApiKeys/DeepSeek.txt'),
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
