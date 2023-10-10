const Node = {
  "id": "cd912bddd7c5faad",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get knox tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 440,
  "y": 1000,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 121
}

Node.template = `
SELECT * FROM {{flow.tablet_knox_table}}
`

module.exports = Node;