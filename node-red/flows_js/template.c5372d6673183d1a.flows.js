const Node = {
  "id": "c5372d6673183d1a",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "create database",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 440,
  "y": 1200,
  "wires": [
    [
      "5e1e4d7e79bc9386"
    ]
  ],
  "_order": 133
}

Node.template = `
CREATE DATABASE IF NOT EXISTS testDB;
`

module.exports = Node;