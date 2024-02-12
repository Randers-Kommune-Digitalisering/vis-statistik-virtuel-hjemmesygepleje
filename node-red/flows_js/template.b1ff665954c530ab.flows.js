const Node = {
  "id": "b1ff665954c530ab",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop knox tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 440,
  "y": 960,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 125
}

Node.template = `
DROP TABLE {{flow.tablet_knox_table}}
`

module.exports = Node;