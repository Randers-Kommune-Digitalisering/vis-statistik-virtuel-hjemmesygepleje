const Node = {
  "id": "637e87263e2f6129",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "name": "move data",
  "rules": [
    {
      "t": "move",
      "p": "payload.name",
      "pt": "msg",
      "to": "name",
      "tot": "msg"
    },
    {
      "t": "move",
      "p": "payload.data",
      "pt": "msg",
      "to": "payload",
      "tot": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 690,
  "y": 380,
  "wires": [
    [
      "165f6f4d27172e90"
    ]
  ],
  "_order": 184
}

module.exports = Node;