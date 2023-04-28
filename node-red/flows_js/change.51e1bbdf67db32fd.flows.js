const Node = {
  "id": "51e1bbdf67db32fd",
  "type": "change",
  "z": "971a7ae6df987a48",
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
      "p": "path",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 1620,
  "y": 480,
  "wires": [
    [
      "43ac65d570e6eb3e"
    ]
  ],
  "_order": 69
}

module.exports = Node;