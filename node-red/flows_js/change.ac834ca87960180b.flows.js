const Node = {
  "id": "ac834ca87960180b",
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
  "y": 880,
  "wires": [
    [
      "e3c3454244dea4a0"
    ]
  ],
  "_order": 106
}

module.exports = Node;