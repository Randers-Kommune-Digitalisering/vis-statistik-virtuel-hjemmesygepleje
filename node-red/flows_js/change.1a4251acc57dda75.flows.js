const Node = {
  "id": "1a4251acc57dda75",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "",
  "rules": [
    {
      "t": "set",
      "p": "auth",
      "pt": "msg",
      "to": "\"basic \" & $.auth",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 570,
  "y": 60,
  "wires": [
    [
      "49f0bc82a7289c93"
    ]
  ],
  "_order": 162
}

module.exports = Node;