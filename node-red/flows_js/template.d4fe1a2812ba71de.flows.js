const Node = {
  "id": "d4fe1a2812ba71de",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get citizen",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 420,
  "y": 1080,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 153
}

Node.template = `
SELECT * FROM {{flow.citizen_table}}
`

module.exports = Node;