const Node = {
  "id": "5c265e4ca4ab11ea",
  "type": "cronplus",
  "z": "971a7ae6df987a48",
  "d": true,
  "g": "616fd052c81e52cc",
  "name": "Scheduled run",
  "outputField": "payload",
  "timeZone": "",
  "persistDynamic": false,
  "commandResponseMsgOutput": "output1",
  "outputs": 1,
  "options": [
    {
      "name": "schedule1",
      "topic": "topic1",
      "payloadType": "default",
      "payload": "",
      "expressionType": "cron",
      "expression": "0  0  1  1  *  ",
      "location": "",
      "offset": "0",
      "solarType": "all",
      "solarEvents": "sunrise,sunset"
    }
  ],
  "x": 180,
  "y": 140,
  "wires": [
    [
      "ac5e094c99a67b2d"
    ]
  ],
  "_order": 57
}

module.exports = Node;