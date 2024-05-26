from abc import ABC, abstractmethod
from typing import List, Iterator

from .. import models

class AbstractGeneraionsService(ABC):
    @abstractmethod
    async def ainvoke(self, request: models.GenerationRequest) -> models.GenerationResult:
        raise NotImplementedError('Method is not implemented')
    
    @abstractmethod
    async def astream(self, request: models.GenerationRequest) -> Iterator[models.GenerationResult]:
        raise NotImplementedError('Method is not implemented')
    