const Node = {
  "id": "79cef13fb5d0e6cc",
  "type": "http request",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "token",
  "method": "POST",
  "ret": "txt",
  "paytoqs": "ignore",
  "url": "https://eu08.manage.samsungknox.com/emm/oauth/token?{{{query}}}",
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
  "x": 890,
  "y": 60,
  "wires": [
    [
      "5b38543aaa561b95"
    ]
  ],
  "_order": 159
}

module.exports = Node;