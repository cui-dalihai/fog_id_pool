# FogID池管理接口

## 批量上传
**接口地址**

> POST /upload
 
 **请求参数示例**
```
   [{"fog_id": "111111"},
    {"fog_id": "222222"},
    {"fog_id": "333333"},
    {"fog_id": "444444"},
    {"fog_id": "555555"},
    {"fog_id": "666666"},
    {"fog_id": "777777"},
    {"fog_id": "998776"}]
```

**返回参数**
```
"0" 表示成功
"原因短语"

```

## 批量领用

**接口地址**

> POST /getbatch

**请求参数示例**
```
{
    "ClientID": "4562fr2",
    "ClientName": "wer345tw",
    "Quantity": "10000",    # 批量申领的数量
    "System": "fog"
}
```
**返回参数**
```
"0" 表示成功
"原因短语"
```

## 获取单个fog_id

**接口地址**
> GET /getone/<client_id>
**请求示例**
```
GET /getone/hf234r4
```
**返回参数**
```
"111111"  成功直接返回string格式的fog_id
"失败原因短语"
```

## 烧写反馈

**接口地址**
> POST /burn

**请求示例**
```
GET /burn

{
    "FogID": "adswe2",
    "burnDevice": "sdifasd",
    "burnFileID": "435etr"
}
```

**返回参数**
```
"0" 表示成功
"原因短语"
```

## 激活反馈

**接口地址**
> GET /activate/<fog_id>

**请求示例**
```
GET /activate/34iu8943
```

**返回参数**
```
"0" 表示成功
"原因短语"
```
