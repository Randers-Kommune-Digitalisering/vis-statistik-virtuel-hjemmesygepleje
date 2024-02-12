const Node = {
  "id": "383496fb3ba25770",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get call",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 420,
  "y": 1040,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 129
}

Node.template = `
SELECT * FROM {{flow.call_table}}
`

module.exports = Node;