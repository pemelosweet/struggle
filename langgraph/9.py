from  typing  import TypedDict
from  dotenv import  load_dotenv
from langchain.agents import create_agent
from  langgraph.graph  import (
    START,
    END,
    StateGraph
)
load_dotenv(override=True)
BLACKLIST = {"U666"}


inner_agent  =create_agent(
    model="deepseek:deepseek-v4-flash",
    tools=[],
    system_prompt="你是营销文案助手，用一句话写一条发券通知，不超过 30 字。",
)

class  FlowState (TypedDict):
    user_id:str
    amount:float
    passed:bool
    reply:str

def risk_check (state:FlowState):
   # 仍然是集合查询，零成本零随机性
   passed = state['user_id']  not in  BLACKLIST
   return {
       "passed":passed
   }

def draft  (state:FlowState):
    r =inner_agent.invoke(
        {"messages": [{
            "role": "user",
            "content": f"给用户{state['user_id']}发了{state['amount']}元券"}]}
    )
    return {"reply": f"{state['user_id']}：{r['messages'][-1].content}"}


def reject (state:FlowState):
     return {"reply": f"{state['user_id']} 命中黑名单，不发券"}

def router (state:FlowState):
       return "draft" if state["passed"] else "reject"

builder =StateGraph(FlowState)
builder.add_node('risk_check',risk_check)
builder.add_node('draft',draft)
builder.add_node('reject',reject)
builder.add_edge(START,'risk_check')
builder.add_conditional_edges(
     'risk_check',
      router,
      ['draft','reject']
)
builder.add_edge('draft',END)
builder.add_edge('reject',END)
graph = builder.compile()

# 正常用户：走 Agent 节点，文案由模型生成
print("正常用户 ->", graph.invoke({"user_id": "U001", "amount": 50})["reply"])
# 黑名单用户：连模型都不会被调用，直接拒绝，省钱又安全
print("黑名单用户 ->", graph.invoke({"user_id": "U666", "amount": 50})["reply"])