const Node = {
  "id": "774fa17e921e9658",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "vask svar",
  "rules": [
    {
      "t": "delete",
      "p": "req",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "errMsgUser",
      "pt": "msg"
    },
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "file",
      "tot": "msg"
    },
    {
      "t": "delete",
      "p": "file",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 1060,
  "y": 260,
  "wires": [
    [
      "1c2683a414560e7b"
    ]
  ],
  "_order": 98
}

module.exports = Node;