const Node = {
  "id": "ec0ba91d7b60e9ab",
  "type": "template",
  "z": "971a7ae6df987a48",
  "name": "Query",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 960,
  "y": 720,
  "wires": [
    [
      "89afaa55ba074b5d"
    ]
  ],
  "_order": 39
}

Node.template = `
SHOW TABLES
`

module.exports = Node;