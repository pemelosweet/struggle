from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import (
    END,
    START,
    StateGraph
)

load_dotenv(override=True)

# 真实的黑名单数据源：U666 在名单里
BLACKLIST = {"U666"}

class  CouponState(TypedDict):
    user_id:str
    amount:float
    passed:bool
    result:str

def check_blacklist(state:CouponState):
    "检查在不在黑名单里"
    passed= state["user_id"]  not in BLACKLIST
    print(f"  [节点] check_blacklist({state['user_id']}) -> {passed}")
    return {
        "passed":passed
    }

def  send_coupon(state:CouponState):
    print(f"  [节点] send_coupon({state['user_id']}, {state['amount']})")
    return {"result": f"已向 {state['user_id']} 发放 {state['amount']} 元代金券"}

def  reject (state:CouponState):
      print(f"  [节点] reject({state['user_id']})")
      return {"result": f"已经进入黑名单了"}
# 路由函数：读 state，返回下一个节点的名字
def route(state: CouponState) -> str:
    # 这就是那段「本该是 if-else」的业务判断，现在它真的是 if-else
    return "send_coupon" if state["passed"] else "reject"

builder = StateGraph(CouponState)
builder.add_node("check_blacklist",check_blacklist)
builder.add_node("send_coupon",send_coupon)
builder.add_node("reject",reject)
builder.add_edge(START,'check_blacklist')
builder.add_conditional_edges(
     'check_blacklist',
     route,
     ["send_coupon", "reject"],
     )
builder.add_edge('send_coupon',END)
builder.add_edge('reject',END)
graph =builder.compile()

out = graph.invoke({"user_id": "U666", "amount": 500, "passed": True})

print("即使输入里硬塞 passed=True：", out["result"])

# 故意只传 user_id，不传 amount，看错误会在哪一步出现
try:
    graph.invoke({"user_id": "U001"})
except KeyError as e:
    # 打印异常类型和缺失的键名，注意这时前两个节点已经跑完了
    print(f"  抛出 {type(e).__name__}: {e}")