const Node = {
  "id": "eb60ff88c1e1b0af",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop location",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 880,
  "wires": [
    [
      "d2de83e52d3cebc5"
    ]
  ],
  "_order": 108
}

Node.template = `
DROP TABLE {{flow.location_table}}
`

module.exports = Node;