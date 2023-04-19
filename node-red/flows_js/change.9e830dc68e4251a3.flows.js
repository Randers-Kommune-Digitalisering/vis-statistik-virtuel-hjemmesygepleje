const Node = {
  "id": "9e830dc68e4251a3",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5c29b0234ffc82a9",
  "name": "Clean after split",
  "rules": [
    {
      "t": "delete",
      "p": "payload.longname",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "payload.attrs",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "parts",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 800,
  "y": 740,
  "wires": [
    [
      "17b1bf0db2361f97"
    ]
  ],
  "_order": 78
}

module.exports = Node;