from dotenv  import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    PIIMiddleware,
    SummarizationMiddleware
)
from langchain.tools import tool

load_dotenv(override=True)


@tool
def get_wather (city):
  "查询天气用的"
  return f"{city},天气晴朗" 
@tool
def refund(order_id: str, amount: float) -> str:
    """给指定订单退款。"""
    # 演示用的假实现，真实场景这里会调支付网关
    return f"订单 {order_id} 已退款 {amount} 元"

def show (name,graph):
 """打印一个 Agent 的图结构。"""
 struct =graph.get_graph()
 print(f"\n=== {name} ===")
 print("nodes:", list(struct.nodes.keys()))
 print ('链接',f"{struct.draw_mermaid()}")

 for e in struct.edges :
   arrow = "-.->" if e.conditional else "-->"
   print(f"   {e.source} {arrow} {e.target}")
    
 
graph =create_agent(
   model="deepseek:deepseek-v4-flash",
   tools=[get_wather],
   middleware=[
     PIIMiddleware('email',strategy='redact'),
     SummarizationMiddleware(
       # 摘要本身也要用模型来写，所以这里也要传 model
        model="deepseek:deepseek-v4-flash", trigger={"tokens": 500}
     ),
     HumanInTheLoopMiddleware(interrupt_on={"refund": True}),
   ]
  )
# 复用上一节定义的 show 函数
show("三个 middleware 叠加", graph)
graph.get_graph().draw_ascii