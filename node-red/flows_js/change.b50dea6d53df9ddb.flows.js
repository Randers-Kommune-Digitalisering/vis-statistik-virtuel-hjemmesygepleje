const Node = {
  "id": "b50dea6d53df9ddb",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "filter data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "$.payload.resultValue.deviceList.{\t    \"id\": deviceId,\t    \"imei\": imei,\t    \"status\": deviceStatus,\t    \"lastSeen\": $fromMillis(lastConnectionDate.time),\t    \"updated\": $now()\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 1100,
  "y": 120,
  "wires": [
    [
      "41a388cca184d9d6"
    ]
  ],
  "_order": 177
}

module.exports = Node;