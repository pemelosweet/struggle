from dotenv  import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from  langchain.agents.middleware import PIIMiddleware
load_dotenv(override=True)

@tool
def get_wathers (city):
    """查询指定城市的天气。"""
    return  f"{city}:qingtian"

graph  = create_agent(
    model="deepseek:deepseek-v4-flash",
    tools=[get_wathers],
    middleware=[PIIMiddleware('email',strategy='redact')]
    )

struct =graph.get_graph()

print ('nodes',struct.nodes.keys())
print('------')
for e in struct.edges:
    arrow = '-.->' if e.conditional  else '-->'
    print(f'{e.source:12s} {arrow} {e.target}')
