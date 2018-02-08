from config import mongo
from datetime import datetime
from bson import ObjectId


class FogDB(object):

    @staticmethod
    def find_many(query):
        return mongo.db['fog_id'].find(query)

    @staticmethod
    def find_one(query):
        return mongo.db['fog_id'].find_one(query)

    @staticmethod
    def create_many(fog_id_list):
        """
        批量,state是available，
        """
        for item in fog_id_list:
            item['State'] = 'available'
            item['CreateTime'] = datetime.utcnow()
            item['Extend'] = []
        return mongo.db['fog_id'].insert_many(fog_id_list)

    @staticmethod
    def use_many(query, system, client_id, client_name):
        """
        批量领用, state由available变为used
        """
        return mongo.db['fog_id'].update_many(
            query,
            {
                '$set': {
                    'State': 'used',
                    'UsedTime': datetime.utcnow(),
                    'ClientID': client_id,
                    'ClientName': client_name,
                    'System': system
                }

            }
        )

    @staticmethod
    def burn_one(query, burn_device, burn_file_id):
        """
        烧写反馈, state变为burned
        FogDB.burn_one({"fog_id": fog_id, "State": "used"}, burn_device, burn_file_id)
        """
        s = mongo.db['fog_id'].find_one(query)   # todo find_update?
        return mongo.db['fog_id'].update(
            {'_id': ObjectId(s['_id'])},
            {
                '$set': {
                    'State': 'burned',
                    'BurnDevice': burn_device,
                    'BurnFileID': burn_file_id
                }

            }
        )

    @staticmethod
    def activate_one(query):
        """
        激活反馈
        """
        return mongo.db['fog_id'].update(
            query,
            {
                '$set': {
                    'State': 'activated',
                    'ActivateTime': datetime.utcnow()
                }
            }
        )
