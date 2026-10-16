from dotenv  import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
load_dotenv(override=True)

@tool
def get_wathers (city):
    """查询指定城市的天气。"""
    return  f"{city}:qingtian"

graph  = create_agent(model="deepseek:deepseek-v4-flash",tools=[get_wathers])

struct =graph.get_graph()

print("nodes",list(struct.nodes.keys()))
print("edges")
for e in struct.edges:
    arrow = "-.->" if e.conditional else "-->"
    print(f"    {e.source:12s} {arrow} {e.target}")
print("nodes")
for  name,node  in struct.nodes.items():
    print(f"    {name:12s} data={type(node.data).__name__}")
print("draw_mermaid")
print (f"{struct.draw_mermaid()}")
print(struct.draw_ascii())