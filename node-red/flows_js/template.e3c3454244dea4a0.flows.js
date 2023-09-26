const Node = {
  "id": "e3c3454244dea4a0",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop call",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 600,
  "y": 840,
  "wires": [
    [
      "d2de83e52d3cebc5"
    ]
  ],
  "_order": 107
}

Node.template = `
DROP TABLE {{flow.call_table}}
`

module.exports = Node;