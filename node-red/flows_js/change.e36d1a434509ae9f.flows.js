const Node = {
  "id": "e36d1a434509ae9f",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "sæt fil, type, dato og tid",
  "rules": [
    {
      "t": "set",
      "p": "file",
      "pt": "msg",
      "to": "msg.req.files[0].buffer.toString()",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "filetype",
      "pt": "msg",
      "to": "req.body.filetype",
      "tot": "msg"
    },
    {
      "t": "set",
      "p": "datetime",
      "pt": "flow",
      "to": "req.body.datetime",
      "tot": "msg"
    },
    {
      "t": "set",
      "p": "week",
      "pt": "flow",
      "to": "req.body.week",
      "tot": "msg"
    },
    {
      "t": "set",
      "p": "errMsgUser",
      "pt": "msg",
      "to": "false",
      "tot": "bool"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 630,
  "y": 180,
  "wires": [
    [
      "5ef7e76e41c4b1fe"
    ]
  ],
  "_order": 93
}

module.exports = Node;