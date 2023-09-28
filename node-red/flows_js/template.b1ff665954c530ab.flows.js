const Node = {
  "id": "b1ff665954c530ab",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 410,
  "y": 900,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 122
}

Node.template = `
DROP TABLE {{flow.tablet_table}}
`

module.exports = Node;