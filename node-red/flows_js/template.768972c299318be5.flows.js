const Node = {
  "id": "768972c299318be5",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get nexus tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 440,
  "y": 1120,
  "wires": [
    [
      "ca08390b5b96b796"
    ]
  ],
  "_order": 153
}

Node.template = `
SELECT * FROM {{flow.tablet_nexus_table}}
`

module.exports = Node;