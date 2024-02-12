const Node = {
  "id": "28b29f81ff636d20",
  "type": "change",
  "z": "b8c8ded2aa4499b8",
  "name": "all good",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "ok",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "statusCode",
      "pt": "msg",
      "to": "200",
      "tot": "num"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 300,
  "y": 120,
  "wires": [
    [
      "28b97cdf7fda5a50"
    ]
  ],
  "_order": 219
}

module.exports = Node;