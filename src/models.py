from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Request(BaseModel):
    request_id: str
    issuer: str

class GetDocumentsRequest(Request):
    pass

class Message(BaseModel):
    text: str
    role: Literal['user', 'assistant', 'system']

class GenerationRequest(Request):
    messages: List[Message]
    streaming_mode: bool = False
    document_ids: List[str]        

class GenerationResponse(BaseModel):
    request_id: str
    status: Literal['on_token', 'finished', 'started', 'failed']

class GenerationResult(BaseModel):
    text: str

class OnTokenResponse(GenerationResponse):
    result: GenerationResult

class GeneraionStartedResponse(GenerationResponse):
    streaming_mode: bool

class GenerationFinishedResponse(GenerationResponse):
    result: Optional[GenerationResult]
    time_spent_sec: int 

class GeneraionFailedResponse(GenerationResponse):
    error: str
    message: str
    