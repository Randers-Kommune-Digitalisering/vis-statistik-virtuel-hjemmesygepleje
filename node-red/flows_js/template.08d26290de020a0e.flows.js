const Node = {
  "id": "08d26290de020a0e",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL opkald",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 1110,
  "y": 400,
  "wires": [
    []
  ],
  "_order": 111
}

Node.template = `
INSERT INTO opkald
VALUES {{payload}}
`

module.exports = Node;