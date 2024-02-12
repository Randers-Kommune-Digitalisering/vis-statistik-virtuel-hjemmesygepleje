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
      "to": "video_calls",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "tablet_knox_table",
      "pt": "flow",
      "to": "tablets_knox",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "citizen_table",
      "pt": "flow",
      "to": "citizens",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "tablet_nexus_table",
      "pt": "flow",
      "to": "tablets_nexus",
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
  "x": 400,
  "y": 640,
  "wires": [
    [
      "02458655da9477a9",
      "1067d76987391306",
      "c18499fa36362788",
      "9e4542992d182d44"
    ]
  ],
  "_order": 110
}

module.exports = Node;