# [{"FogID": "111111"},
# {"FogID": "222222"},
# {"FogID": "333333"},
# {"FogID": "444444"},
# {"FogID": "555555"},
# {"FogID": "666666"},
# {"FogID": "777777"},
# {"FogID": "998776"}]
import json
fog_id = list()

for i in range(1000000):
    fog_id.append({'FogID': str(i)})

with open('fog_id.json', "w") as f:
    json.dump(fog_id, f)

# with open('fog_id.json', "r") as f:
#     t = json.load(f)

# print(type(t))


