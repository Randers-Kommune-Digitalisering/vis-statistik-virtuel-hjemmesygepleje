const Node = {
  "id": "37e7a50781e54f2b",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "move time",
  "rules": [
    {
      "t": "set",
      "p": "startDate",
      "pt": "msg",
      "to": "startTime",
      "tot": "msg"
    },
    {
      "t": "set",
      "p": "endDate",
      "pt": "msg",
      "to": "endTime",
      "tot": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 390,
  "y": 220,
  "wires": [
    [
      "5faef195141dffea"
    ]
  ],
  "_order": 203
}

module.exports = Node;