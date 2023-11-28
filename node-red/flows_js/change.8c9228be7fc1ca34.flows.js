const Node = {
  "id": "8c9228be7fc1ca34",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5c29b0234ffc82a9",
  "name": "Clean response",
  "rules": [
    {
      "t": "delete",
      "p": "host",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "user",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "password",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "workdir",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 460,
  "y": 380,
  "wires": [
    [
      "ce72a16764e92c83",
      "892a33d0eb11bd12"
    ]
  ],
  "_order": 67
}

module.exports = Node;