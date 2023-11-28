const Node = {
  "id": "3af2f07e8f8d5e97",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "get test_1",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 420,
  "y": 1280,
  "wires": [
    [
      "7921205c3577f96f"
    ]
  ],
  "_order": 137
}

Node.template = `
SELECT * FROM test_1
`

module.exports = Node;