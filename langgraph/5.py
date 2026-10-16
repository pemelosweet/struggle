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
   tools=[refund],
   middleware=[
     HumanInTheLoopMiddleware(interrupt_on={"refund": True}),
     PIIMiddleware('email',strategy='redact'),
   ]
  )
out={}
for e in  graph.get_graph().edges:
 out.setdefault(e.source, []).append(e.target)
 path, cur, seen = [], "model", set()
while cur and cur not in seen:
  seen.add(cur)
  path.append(cur)
  next =[t for t in out.get(cur,[]) if t not in('__end__','tools')]
  cur = next[0] if next else None

print(f"声明顺序 PIIMiddleware,HumanInTheLoopMiddleware: {' → '.join(path)}")

#  PIIMiddleware,HumanInTheLoopMiddleware: model → HumanInTheLoopMiddleware.after_model → PIIMiddleware[email].after_model → PIIMiddleware[email].before_model
#  PIIMiddleware,HumanInTheLoopMiddleware: model → PIIMiddleware[email].after_model → HumanInTheLoopMiddleware.after_model → PIIMiddleware[email].before_model

