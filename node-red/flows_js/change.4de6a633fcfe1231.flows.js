const Node = {
  "id": "4de6a633fcfe1231",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "sæt fejl",
  "rules": [
    {
      "t": "set",
      "p": "error",
      "pt": "msg",
      "to": "Unknown filetype",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "errMsgUser",
      "pt": "msg",
      "to": "Ukendt filtype",
      "tot": "str"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 460,
  "y": 460,
  "wires": [
    [
      "5a906997cafee489"
    ]
  ],
  "_order": 111
}

module.exports = Node;