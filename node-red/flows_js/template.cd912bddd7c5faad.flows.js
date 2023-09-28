const Node = {
  "id": "cd912bddd7c5faad",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 420,
  "y": 940,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 124
}

Node.template = `
SELECT * FROM {{flow.tablet_table}}
`

module.exports = Node;