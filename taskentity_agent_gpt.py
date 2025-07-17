from prompt_management import get_prompt
from chatgptProcess import chatgptProcess

#text1 = """
#Edinburgh is Scotland's capital, celebrated globally for its rich history, stunning architecture, and vibrant cultural scene. Situated on a series of hills between the Firth of Forth to the north and the Pentland Hills to the south, it is home to over 500,000 people. Once known for biscuits, brewing, banking, and books, Edinburgh's economy now thrives in finance, science, tourism, and the professions. It is the UK's second-largest financial hub and Europe's fourth-largest. The city also hosts the Scottish Parliament, reaffirming its role as a political center. Edinburgh's retail scene is dominated by Princes Street and major shopping complexes. Its industries include information technology, renewable energy, and life sciences, epitomized by the Edinburgh BioQuarter. Coordinates: 55.9523°N, 3.1882°W..
#Dingwall is a historic burgh town in Highland Council Area, located at the head of the Cromarty Firth, 10 miles northwest of Inverness. Its name originates from Scandinavian words meaning 'parliament in the valley.' With royal burgh status since 1226, Dingwall has a rich history as a market center and administrative seat. The town gained prominence in the 18th and 19th centuries due to linen spinning, its status as a road and railway junction, and its role in livestock markets. In the 1970s, the North Sea oil boom further fueled its growth. Dingwall hosts the Highland Traditional Music Festival and Highland Games, with landmarks including Tulloch Castle and St Clement's Church. Coordinates: 57.5957°N, 4.4327°W.
#
#Please tell me how to get to Dingwall from Edinburgh.      
#"""
## processor = nlpProcess(text)
## tasks = processor.process()
#text2 = """
#Newbigging (Near Newtyle, Western Angus)Coordinates: 56.5645°N, 3.1617°WThis small hamlet is close to the western boundary of Angus.It lies half a mile (1 km) northwest of Newtyle, 1¼ miles (2 km) east of Ardler, and 1½ miles (2.5 km) south of Meigle in Perth and Kinross.The surrounding landscape is mostly farmland and rolling countryside, with Newtyle being a historically important village in the region.
#Newbigging (Near Monikie, Southeastern Angus)Coordinates: 56.5142°N, 2.8189°WThis village is located 1¼ miles (2 km) south of Monikie and 2 miles (3 km) east-southeast of Wellbank.It grew significantly in the 1950s, when public housing was built, increasing its population.Nearby are the Carlungie and Ardestie souterrains, which are Iron Age underground structures likely used for storage or ritual purposes.Stone quarrying has been an important local industry in the area.
#Newbigging (Near Tealing, Southern Angus)Coordinates: 56.5268°N, 2.9395°WThis hamlet is immediately east of the A90 trunk road, one of Scotland’s main north-south highways.It lies half a mile (1 km) southeast of Tealing and 4 miles (6.5 km) north of Dundee.The surrounding area features agriculture, rural homes, and proximity to Dundee’s outskirts.
#
#Tell me about Newbiggings in Angus
#"""

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
