from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import generatesyntheticdata
import tunewithlogdata
import evaluateModel
class LogTrain(TypedDict):
   messages: Annotated[list, add_messages]
   trainer: list[str]
   finished: bool
graph: StateGraph = StateGraph(state_schema=LogTrain)

def createSyntheticLogFile(state:LogTrain):
   generatesyntheticdata.generateSyntheticData()
def trainModel(state):
   tunewithlogdata.trainData()
def evaluateModel(state):
   evaluateModel.evaluateTrainedModel()

graph.add_node("createSyntheticLogFile", createSyntheticLogFile)
graph.add_node("trainModel", trainModel)
graph.add_node("evaluateModel", evaluateModel)
graph.add_edge(START, "createSyntheticLogFile")
graph.add_edge("createSyntheticLogFile","trainModel")
graph.add_edge("trainModel","evaluateModel")
graph.add_edge("evaluateModel",END)
graph_compiled = graph.compile()
config = {"recursion_limit": 100}
state=graph_compiled.invoke({"messages": []}, config)