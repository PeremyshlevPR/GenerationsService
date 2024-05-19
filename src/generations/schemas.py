from typing import List, Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    role: Literal['user', 'assistant', 'system']

class GenerationRequest(BaseModel):
    request_id: str
    issuer: str
    pipeline_name: str
    messages: List[Message]
    streaming_mode: bool = False

class TextMiningAssistantRequest(GenerationRequest):
    document_ids: List[str]    


class GenerationResponse(BaseModel):
    request_id: str
    status: Literal['on_token', 'finished', 'started', 'failed']

class TokenResult(GenerationResponse):
    text: str

class GeneraionStartedResonse(GenerationResponse):
    pipeline_name: str

class GenerationFinishedResponse(GenerationResponse):
    text: Optional[str]
    time_spent_sec: int 

class GeneraionFailedResponse(GenerationResponse):
    error: str
    message: str
    