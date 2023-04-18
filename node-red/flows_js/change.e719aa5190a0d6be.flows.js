const Node = {
  "id": "e719aa5190a0d6be",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "e183203bdc1f7193",
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
  "x": 520,
  "y": 780,
  "wires": [
    [
      "c31471d44a880896"
    ]
  ],
  "_order": 52
}

module.exports = Node;