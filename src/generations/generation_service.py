from typing import AsyncGenerator, List, Dict, Any

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph
from . import AbstractGeneraionsService
from .. import models


class LangGraphGeneraionsService(AbstractGeneraionsService):
    def __init__(self, graph: CompiledStateGraph):
        self._graph = graph
    
    def _as_lc_message(self, message: models.Message) -> BaseMessage:
        role_to_class = {
            'user': HumanMessage,
            'assistant': AIMessage,
            'system': SystemMessage
        }
        MessageClass = role_to_class[message.role]:
        return MessageClass(message.text)
    
    def _to_lc_messages(self, messages: List[models.Message]) -> List[BaseMessage]:
        return [self._as_lc_message(message) for message in messages]

    def _get_state(self, request: models.GenerationRequest) -> Dict[str, Any]:
        return {
            'document_ids': request.document_ids,
            'messages': self._to_lc_messages(request.messages)
        }
    
    def _parse_output(self, state: dict) -> models.GenerationResult:
        return models.GenerationResult(text=state["messages"][-1])

    async def ainvoke(self, request: models.GenerationRequest, debug_mode=False) -> models.GenerationResult:
        state = self._get_state(request)
        state = await self._graph.ainvoke(state, debug=debug_mode)
        return self._parse_output(state)

    async def astream(self, request: models.GenerationRequest, debug_mode=False) -> AsyncGenerator[models.GenerationResult, None, None]:
        state = self._get_state(request)

        async for output in self._graph.astream_log(state, include_types=["llm"]):
            for op in output.ops:
                if op["path"].startswith("/logs/") and op["path"].endswith(
                    "/streamed_output/-"
                ):
                    print(op["value"].content, end="|")
                    yield models.GenerationResult(text=op["value"].content)
