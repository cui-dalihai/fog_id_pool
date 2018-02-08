# from datetime import datetime
# from flask import request
# from flask import Flask
# from bson import ObjectId
# import json
# from flask.ext.pymongo import PyMongo
# app = Flask(__name__)
# app.config["MONGO_DBNAME"] = "FOG_ID"
# app.config["MONGO_HOST"] = '127.0.0.1'
# app.config["MONGO_PORT"] = 27017
# mongo = PyMongo(app, config_prefix="MONGO")
# from config import mongo, app
# from db import FogDB
#
#
# @app.route('/upload_batch', methods=['POST'])
# def upload_batch():
#     """
#     批量上传
#     fog_id : 格式{"fog_id":[{"fog_id": "111111"},
#                            {"fog_id": "222222"},
#                            {"fog_id": "333333"},
#                            {"fog_id": "444444"},
#                            {"fog_id": "555555"},
#                            {"fog_id": "666666"},
#                            {"fog_id": "777777"},
#                            {"fog_id": "998776"}]}
#
#     结果:
#         {
#         "_id" : ObjectId("5a7a5f539e8d7e306c540de3"),
#         "fog_id" : "998776",
#         "State" : "available",
#         "CreateTime" : ISODate("2018-02-07T02:07:15.463Z")
#         }
#
#     :return:
#     """
#     fog_id_data = request.get_data()
#     if not fog_id_data:
#         return "1", "no fog_id"
#     data_dict = json.loads(fog_id_data.decode(encoding="utf-8", errors="strict"))
#     fog_id_list = data_dict['fog_id']  # 这个列表在实际使用时会很大，最好使用生成器传递
#     FogDB.create_many(fog_id_list)     # 最多同时可以插入多少数据
#
#     return "0"
#
#
# @app.route('/get_batch', methods=['POST'])
# def get_batch():
#     """
#     批量领用  {"clientid": "hifdshi34",
#                 "clientname": "mxchip",
#                 "quantity": "2",
#                 "system": "fog"}
#
#     结果：
#         {
#         "_id" : ObjectId("5a7a5f539e8d7e306c540de0"),
#         "fog_id" : "555555",
#         "State" : "used",
#         "CreateTime" : ISODate("2018-02-07T02:07:15.463Z"),
#         "ClientID" : "hifdshi34",
#         "ClientName" : "mxchip",
#         "System" : "fog",
#         "UsedTime" : ISODate("2018-02-07T02:08:27.605Z")
#         }
#
#     :return: 0 成功
#              1 失败, 失败原因
#     """
#     # 使用query = {'state': 'available'}获取quantity个
#     get_batch_data = request.get_data()
#     if not get_batch_data:
#         return "1", "no request data"
#     data_dict = json.loads(get_batch_data.decode(encoding="utf-8", errors="strict"))
#
#     clientid = data_dict["clientid"]
#     clientname = data_dict['clientname']
#     quantity = int(data_dict['quantity'])
#     system = data_dict['system']
#
#     query_list = FogDB.find_many({"State": "available"}, quantity)  # 只有State是available时是可以领用的
#
#     if query_list.count() < quantity:  # 请求的数量获取不足
#         return "fog id is not enough: %s left" % query_list.count()
#
#     for i in query_list:
#         FogDB.use_one(query={"_id": ObjectId(i["_id"])},
#                       system=system,
#                       client_id=clientid,
#                       client_name=clientname)
#
#     return "0"
#
#
# @app.route('/getid', methods=['POST'])  # 先请求一个fog_id
# def get_one():
#     """
#     请求格式：{"client_id": "hifdshi34",
#              "burn_device": "deviceid09idesa",
#              "burn_file_id": "asdfl343"
#                 }
#
#     结果：
#         {
#         "_id" : ObjectId("5a7a5f539e8d7e306c540ddc"),
#         "fog_id" : "111111",
#         "State" : "used",
#         "CreateTime" : ISODate("2018-02-07T02:07:15.463Z"),
#         "ClientID" : "hifdshi34",
#         "ClientName" : "mxchip",
#         "System" : "fog",
#         "UsedTime" : ISODate("2018-02-07T02:08:27.595Z"),
#         "BurnDevice" : "deviceid09idesa",
#         "BurnFileID" : "asdfl343"
#         }
#
#     burn_device: 设备id
#     burn_file_id: 固件id
#     """
#     fog_id = "not found"
#
#     get_batch_data = request.get_data()
#     if not get_batch_data:
#         return "1", "no request data"
#     data_dict = json.loads(get_batch_data.decode(encoding="utf-8", errors="strict"))
#
#     client_id = data_dict["client_id"]
#     burn_device = data_dict["burn_device"]
#     burn_file_id = data_dict["burn_file_id"]
#
#     query_list = FogDB.request_one({"ClientID": client_id, "State": "used"}, burn_device, burn_file_id)
#     print(query_list)
#     if not query_list:
#         return "fog_id for this client_id is out of use"
#
#     for k in query_list.keys():
#         if k.startswith("fog_id"):
#             fog_id = query_list[k]
#
#     return fog_id
#
#
# @app.route('/burn/<fog_id>', methods=['GET'])  # 烧写先请求一个fog_id
# def burn(fog_id):
#     """
#     fog_id烧写时要请求，将fog_id的状态改为burn
#     /burn/11111
#
#     :return:
#     """
#     ret = FogDB.burn_one({"fog_id": fog_id, "State": "used"})
#     print("=====", ret)
#     return str(ret['ok'])
#
#
# @app.route('/activate/<fog_id>', methods=['GET'])  # 激活
# def activate(fog_id):
#     """
#     携带fog_id请求后，该fog_id的状态更新为activated
#     :param fog_id:
#     :return:
#     """
#     ret = FogDB.activate_one({"fog_id": fog_id, "State": "burned"})
#     print("=====", ret)
#     return str(ret['ok'])


# class FogDB(object):
#
#     @staticmethod
#     def find_many(query, quantity):
#         return mongo.db['fog_id'].find(query, limit=quantity)
#
#     @staticmethod
#     def find_one(query):
#         return mongo.db['fog_id'].find_one(query)
#
#     @staticmethod
#     def create_many(fog_id_list):
#         """
#         批量上传时,fog_id的状态应该是available，
#         创建时的字段：
#         fog_id
#         create_time
#         state
#         """
#         for item in fog_id_list:
#             item['State'] = 'available'
#             item['CreateTime'] = datetime.utcnow()
#         return mongo.db['fog_id'].insert_many(fog_id_list)
#
#     @staticmethod
#     def create_one(fog_id):
#         return mongo.db['fog_id'].insert_one({
#             'FogId': fog_id,
#             'CreateTime': datetime.utcnow(),
#             'State': 'available',
#             'Extend': [],
#         })
#
#     @staticmethod
#     def request_one(query, burn_device, burn_file_id):
#         # get_one({"ClientID": client_id, "State": "used"}, burn_device, burn_file_id)
#         """
#         领用,
#         """
#         # {"_id": ObjectId(i["_id"])
#         print(query, burn_device, burn_file_id)
#         s = mongo.db['fog_id'].find_one(query)
#         mongo.db['fog_id'].update(
#             {'_id': ObjectId(s['_id'])},
#             {
#                 '$set': {
#                     'State': 'used',
#                     'BurnDevice': burn_device,
#                     'BurnFileID': burn_file_id
#                 }
#
#             }
#         )
#         print("----", s)
#         return s
#
#     @staticmethod
#     def use_one(query, system, client_id, client_name):
#         """
#         领用,
#         """
#         print(query, system, client_id, client_name)
#         s = mongo.db['fog_id'].update(
#             query,
#             {
#                 '$set': {
#                     'State': 'used',
#                     'UsedTime': datetime.utcnow(),
#                     'ClientID': client_id,
#                     'ClientName': client_name,
#                     'System': system
#                 }
#
#             }
#         )
#         print(s)
#         return s
#
#     @staticmethod
#     def burn_one(query):
#         """
#         烧写
#         :param query:
#         :param burn_device:
#         :param burn_file_id:
#         :return:
#         """
#         return mongo.db['fog_id'].update(
#             query,
#             {
#                 '$set': {
#                     'State': 'burned',
#                     'BurnTime': datetime.utcnow(),
#                 }
#             }
#         )
#
#     @staticmethod
#     def activate_one(query):
#         return mongo.db['fog_id'].update(
#             query,
#             {
#                 '$set': {
#                     'State': 'activated',
#                     'ActivateTime': datetime.utcnow()
#                 }
#             }
#         )

from views import app

if __name__ == '__main__':
    app.run(debug=True)



