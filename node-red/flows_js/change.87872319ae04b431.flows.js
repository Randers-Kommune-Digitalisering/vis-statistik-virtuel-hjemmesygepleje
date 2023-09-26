const Node = {
  "id": "87872319ae04b431",
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
  "y": 960,
  "wires": [
    [
      "8db0ab434a99a837"
    ]
  ],
  "_order": 137
}

module.exports = Node;