const Node = {
  "id": "b6ba397b24cd5811",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 510,
  "y": 1020,
  "wires": [
    []
  ],
  "_order": 107
}

Node.template = `
DROP TABLE lokation
`

module.exports = Node;