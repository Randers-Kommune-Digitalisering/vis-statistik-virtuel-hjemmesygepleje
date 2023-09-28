const Node = {
  "id": "43ff0e524b17db13",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "sæt tabelnavne",
  "rules": [
    {
      "t": "set",
      "p": "call_table",
      "pt": "flow",
      "to": "opkald",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "tablet_table",
      "pt": "flow",
      "to": "tablet",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "setup",
      "pt": "msg",
      "to": "true",
      "tot": "bool"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 420,
  "y": 580,
  "wires": [
    [
      "1067d76987391306",
      "02458655da9477a9"
    ]
  ],
  "_order": 104
}

module.exports = Node;