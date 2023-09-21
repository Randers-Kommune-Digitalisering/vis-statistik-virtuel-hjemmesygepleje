const Node = {
  "id": "e36d1a434509ae9f",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "sæt fil og filnavn",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "msg.req.files[0].buffer.toString()",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "name",
      "pt": "msg",
      "to": "req.files[0].originalname",
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
  "x": 600,
  "y": 180,
  "wires": [
    [
      "5ef7e76e41c4b1fe"
    ]
  ],
  "_order": 81
}

module.exports = Node;