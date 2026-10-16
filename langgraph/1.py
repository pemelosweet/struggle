# 从 .env 文件读取 API Key 的工具函数
from dotenv import load_dotenv
# LangChain 提供的 Agent 快捷构造函数，也就是前面各章一直在用的驾驭层（harness）
from langchain.agents import create_agent
# 把普通 Python 函数变成 Agent 可调用工具的装饰器
from langchain.tools import tool
# 从 langgraph 里导入「编译后的状态图」类型，稍后用它做类型判断
from langgraph.graph.state import CompiledStateGraph

# override=True 表示 .env 里的值覆盖系统已有的同名环境变量，避免读到旧 Key
load_dotenv(override=True)

# 用 @tool 装饰，函数就成了一个工具；函数名是工具名，docstring 是给模型看的说明
@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    # 演示用的假数据，真实场景这里会调天气 API
    return f"{city}：晴，26℃"

# 造一个最普通的 Agent：一个模型 + 一个工具，什么额外配置都不加
graph = create_agent(model="deepseek:deepseek-v4-flash", tools=[get_weather])

# 打印它的真实类型
print("type:", type(graph))
# 打印完整继承链，只取类名让输出简洁
print("MRO:", [c.__name__ for c in type(graph).__mro__])
# isinstance 判断它是否真的是 LangGraph 的编译图
print("是 LangGraph 的编译图吗:", isinstance(graph, CompiledStateGraph))