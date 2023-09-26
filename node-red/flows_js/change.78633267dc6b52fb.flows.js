const Node = {
  "id": "78633267dc6b52fb",
  "type": "change",
  "z": "39989dadda5c9a15",
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
      "p": "location_table",
      "pt": "flow",
      "to": "lokation",
      "tot": "str"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 400,
  "y": 920,
  "wires": [
    [
      "eb60ff88c1e1b0af"
    ]
  ],
  "_order": 135
}

module.exports = Node;