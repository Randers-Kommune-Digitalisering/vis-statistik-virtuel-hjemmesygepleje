const Node = {
  "id": "6d829990ca57f628",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop call",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 420,
  "y": 920,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 119
}

Node.template = `
DROP TABLE {{flow.call_table}}
`

module.exports = Node;