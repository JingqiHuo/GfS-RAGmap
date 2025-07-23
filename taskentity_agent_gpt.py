from prompt_management import get_prompt
from chatgptProcess import chatgptProcess

class agent2(object):
    def __init__(self):
        pass

    def agent_json(self,prompt,text):
        self.system_prompt = get_prompt(prompt)
        names = chatgptProcess(self.system_prompt,text).rqtcall()
        return names
    
    def agent_nl(self,prompt,text):
        self.system_prompt = get_prompt(prompt)
        task = chatgptProcess(self.system_prompt,text).rqtcall_nl()
        return task
    
    def agent_default(self,text):

        response = chatgptProcess(None,text).rqtcall_default()
        return response
    
    def qa_test(self, text):
        self.system_prompt = get_prompt("question_generation")
        qaset = chatgptProcess(self.system_prompt,text).rqtcall_nl()
        return qaset
