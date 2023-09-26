const Node = {
  "id": "8db0ab434a99a837",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 920,
  "wires": [
    [
      "d2de83e52d3cebc5"
    ]
  ],
  "_order": 109
}

Node.template = `
DROP TABLE {{flow.tablet_table}}
`

module.exports = Node;