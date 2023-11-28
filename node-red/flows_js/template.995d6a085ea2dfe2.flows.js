const Node = {
  "id": "995d6a085ea2dfe2",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "drop test_1",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 430,
  "y": 1320,
  "wires": [
    [
      "7921205c3577f96f"
    ]
  ],
  "_order": 140
}

Node.template = `
DROP TABLE test_1
`

module.exports = Node;