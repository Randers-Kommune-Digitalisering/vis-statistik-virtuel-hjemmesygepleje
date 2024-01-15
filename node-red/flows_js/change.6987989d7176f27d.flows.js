const Node = {
  "id": "6987989d7176f27d",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "set auth",
  "rules": [
    {
      "t": "set",
      "p": "auth",
      "pt": "msg",
      "to": "payload.access_token",
      "tot": "msg"
    },
    {
      "t": "set",
      "p": "auth",
      "pt": "msg",
      "to": "\"bearer \" & $.auth",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 380,
  "y": 120,
  "wires": [
    [
      "29162c9198ec13b3"
    ]
  ],
  "_order": 166
}

module.exports = Node;