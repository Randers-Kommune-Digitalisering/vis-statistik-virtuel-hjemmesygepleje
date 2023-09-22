const Node = {
  "id": "0d1d8f61580ad039",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "sæt fejlbesked",
  "rules": [
    {
      "t": "set",
      "p": "errMsgUser",
      "pt": "msg",
      "to": "Flere filer valgt, Man kan kun uploade én fil ad gangen.",
      "tot": "str"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 600,
  "y": 260,
  "wires": [
    [
      "5ef7e76e41c4b1fe"
    ]
  ],
  "_order": 90
}

module.exports = Node;