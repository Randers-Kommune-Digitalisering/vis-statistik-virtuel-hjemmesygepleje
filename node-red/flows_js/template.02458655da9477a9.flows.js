const Node = {
  "id": "02458655da9477a9",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL tablet",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 640,
  "wires": [
    [
      "55c213b8122a50a2"
    ]
  ],
  "_order": 109
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.tablet_table}} (
  id CHAR(15) NOT NULL,
  sidst_set TIMESTAMP,
  CONSTRAINT tablet_id PRIMARY KEY (id)
);
`

module.exports = Node;