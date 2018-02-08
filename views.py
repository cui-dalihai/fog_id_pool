from flask import request
from config import app
from db import FogDB
from pymongo.errors import BulkWriteError
import json


@app.route('/upload', methods=['POST'])
def upload_batch():  # 10W 10s

    fog_id_data = request.get_data()
    if not fog_id_data:
        return "no fog_id in request data"
    data_list = json.loads(fog_id_data.decode(encoding="utf-8", errors="strict"))
    try:
        FogDB.create_many(data_list)
    except BulkWriteError:
        return "fog_id contained in request already exist"

    return "0"


@app.route('/getbatch', methods=['POST'])
def get_batch():   # 8W 2.5min

    get_batch_data = request.get_data()
    if not get_batch_data:
        return "no request data"
    data_dict = json.loads(get_batch_data.decode(encoding="utf-8", errors="strict"))

    client_id = data_dict["ClientID"]
    client_name = data_dict['ClientName']
    quantity = int(data_dict['Quantity'])
    system = data_dict['System']

    query_list = FogDB.find_many({"State": "available"})  # 只有State是available时是可以领用的

    if query_list.count() < quantity:
        return "fog id is not enough: %s left" % query_list.count()

    FogDB.use_many({"State": "available"}, system, client_id, client_name)

    return "0"


@app.route('/getone/<client_id>', methods=['GET'])
def get_one(client_id):

    query = {"ClientID": client_id, "State": "used"}
    single_id = FogDB.find_one(query)

    if not single_id:
        return "fog_id for this client_id is out of use"

    return single_id["FogID"]


@app.route('/burn', methods=['POST'])
def burn():
    """
    {
        "FogID": "adswe2",
        "burnDevice": "sdifasd",
        "burnFileID": "435etr"
    }
    """
    get_burn_data = request.get_data()
    if not get_burn_data:
        return "no request data"
    data_dict = json.loads(get_burn_data.decode(encoding="utf-8", errors="strict"))

    fog_id = data_dict["FogID"]
    burn_device = data_dict["burnDevice"]
    burn_file_id = data_dict["burnFileID"]
    query = {"FogID": fog_id, "State": "used"}  # 领用状态下的fog_id是可以被烧写的

    query_single = FogDB.find_one(query)
    if not query_single:
        return "%s can not been burned" % fog_id

    FogDB.burn_one(query, burn_device, burn_file_id)

    return "0"


@app.route('/activate/<fog_id>', methods=['GET'])
def activate(fog_id):

    query = {"FogID": fog_id, "State": "burned"}  # 烧写后的fog_id是可以被激活的
    query_single = FogDB.find_one(query)
    if not query_single:
        return "%s can not been activated" % fog_id

    FogDB.activate_one({"FogID": fog_id, "State": "burned"})

    return "0"
