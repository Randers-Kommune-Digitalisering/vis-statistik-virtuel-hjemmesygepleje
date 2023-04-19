const Node = {
  "id": "ec0ba91d7b60e9ab",
  "type": "template",
  "z": "971a7ae6df987a48",
  "g": "dd6ff76fb5bcc3de",
  "name": "Query",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 1390,
  "y": 1000,
  "wires": [
    [
      "89afaa55ba074b5d"
    ]
  ],
  "_order": 41
}

Node.template = `
SHOW TABLES
`

module.exports = Node;