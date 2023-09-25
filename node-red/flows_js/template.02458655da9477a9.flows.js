const Node = {
  "id": "02458655da9477a9",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 430,
  "y": 640,
  "wires": [
    [
      "55c213b8122a50a2"
    ]
  ],
  "_order": 105
}

Node.template = `
CREATE TABLE IF NOT EXISTS tablet (
  id CHAR(15) NOT NULL,
  sidst_set TIMESTAMP,
  CONSTRAINT tablet_id PRIMARY KEY (id)
);
`

module.exports = Node;