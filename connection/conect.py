import hashlib
import exceptions
from datetime import datetime
from pymongo.errors import DuplicateKeyError
# noinspection PyProtectedMember
from motor.motor_asyncio import AsyncIOMotorCollection

class Flow:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
        # noinspection PyTypeChecker
        # self.valid_status = list(map(lambda x: x.value, LogStatus))
        # self.valid_status.remove('pending')
        # self.valid_status.remove('processing')

    async def add(self, **kwargs) -> str:
        flow_id = hashlib.sha256((str(kwargs)).encode()).hexdigest()
        document = {'_id': flow_id, 'status_modified_at': datetime.utcnow(), **kwargs}
        try:
            await self.collection.insert_one(document)
            return FlowMessages.FlowAddSuccessfully
        except DuplicateKeyError:
            raise exceptions.FlowAlreadyExists(flow_id)

class FlowMessages:
    FlowAddSuccessfully = 'Flow added successfully.'
    FlowFinishedSuccessfully = 'Flow finished successfully.'

        
