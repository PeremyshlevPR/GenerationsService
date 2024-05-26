import abc

class AbstractCommunicationService(abc.ABC):
    
    @abc.abstractmethod
    async def process_requsets(self):
        raise NotImplementedError('Method is not implemented')
    