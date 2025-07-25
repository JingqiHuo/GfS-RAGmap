from deepseekProcess import deepseekProcess
from prompt_management import get_prompt

class agent1(object):
    def __init__(self):
        pass

    def agent_json(self,prompt,text):
        self.system_prompt = get_prompt(prompt)
        names = deepseekProcess(self.system_prompt,text).rqtcall()
        return names
    
    def agent_nl(self,prompt,text):
        self.system_prompt = get_prompt(prompt)
        task = deepseekProcess(self.system_prompt,text).rqtcall_nl()
        return task
    
    def agent_default(self,text):

        response = deepseekProcess(None,text).rqtcall_default()
        return response
    
    def qa_test(self, text):
        self.system_prompt = get_prompt("question_generation")
        qaset = deepseekProcess(self.system_prompt,text).rqtcall_nl()
        return qaset