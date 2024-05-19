import json
import asyncio
from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from generations.generation_service import GeneraionsService 
from generations import schemas


class KafkaGateway:
    def __init__(self,
                 producer: AIOKafkaProducer,
                 consumer: AIOKafkaConsumer,
                 generations_serivce: GeneraionsService):
        self._producer = producer
        self._consumer = consumer
        self._generations_service = generations_serivce

        self._generations = dict()

    async def start(self):
        await self._producer.start()
        await self._consumer.start()

        await self._process_generaion_results()

    async def process_requsets(self):
        async for request in self._consumer:
            try:
                request = json.loads(request)

                request = schemas.GenerationRequest(**request)
                generation_task = asyncio.create_task(
                        self._process_request(request)
                    )
                self._generations[request.request_id] = {
                    "request": request,
                    "task": generation_task,
                    "created_at": datetime.now(tz=timezone.utc)
                }
            except:
                raise
            finally:
                await self._consumer.stop()

    async def _process_request(self, request: schemas.GenerationRequest):
        await self._produce_ack_message(request)

        try:
            if request.streaming_mode:
                async for token in self._generations_service.stream(request):
                    self._send_response(token)
            else:
                response = await self._generations_service.ainvoke(request)
                self._send_response(token)
            
        except Exception as e:
            response = schemas.GeneraionFailedResponse(
                request_id=request.request_id,
                status='failed',
                error=str(e),
                message=e.message if hasattr(e, "message") else ''                
            )
            await self._send_response(response)

    async def _produce_ack_message(self, request: schemas.GenerationRequest):
        response = schemas.GeneraionStartedResonse(
            request_id=request.request_id,
            status='started',
            pipeline_name=request.pipeline_name
        )
        await self._send_response(response)
        
    async def _send_response(self, response: schemas.GenerationResponse):
        self._producer.send(
            response.model_dump_json()
        )
        await self._producer.flush()
