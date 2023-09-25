const Node = {
  "id": "7dfbef958f6a74e2",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 1110,
  "y": 360,
  "wires": [
    []
  ],
  "_order": 110
}

Node.template = `
INSERT INTO table_name (column1, column2, column3,...columnN)  
VALUES (value1, value2, value3,...valueN);
`

module.exports = Node;