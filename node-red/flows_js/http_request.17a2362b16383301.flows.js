const Node = {
  "id": "17a2362b16383301",
  "type": "http request",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "device list",
  "method": "POST",
  "ret": "txt",
  "paytoqs": "ignore",
  "url": "https://eu08.manage.samsungknox.com/emm/oapi/device/selectDeviceList?{{{query}}}",
  "tls": "",
  "persist": false,
  "proxy": "",
  "insecureHTTPParser": false,
  "authType": "",
  "senderr": false,
  "headers": [
    {
      "keyType": "other",
      "keyValue": "Content-Type",
      "valueType": "other",
      "valueValue": "application/x-www-form-urlencoded"
    },
    {
      "keyType": "other",
      "keyValue": "Authorization",
      "valueType": "msg",
      "valueValue": "auth"
    }
  ],
  "x": 700,
  "y": 120,
  "wires": [
    [
      "abfd322beedaa91f"
    ]
  ],
  "_order": 165
}

module.exports = Node;