const Node = {
  "id": "0d69f3fa27c5e44c",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5b803f1c3bcb0822",
  "name": "Hent id på seneste fil",
  "rules": [
    {
      "t": "set",
      "p": "package_id",
      "pt": "msg",
      "to": "payload.result.resources[0].id",
      "tot": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 820,
  "y": 440,
  "wires": [
    []
  ],
  "_order": 35
}

module.exports = Node;