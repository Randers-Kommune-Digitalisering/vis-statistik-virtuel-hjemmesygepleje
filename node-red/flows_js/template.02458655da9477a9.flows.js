const Node = {
  "id": "02458655da9477a9",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL knox tablets",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 630,
  "y": 680,
  "wires": [
    [
      "d826af94fc94f8bc"
    ]
  ],
  "_order": 106
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.tablet_knox_table}} (
  id CHAR(15) NOT NULL,
  sidst_set TIMESTAMP,
  latitude DECIMAL(8,6),
  longitude DECIMAL(9,6),
  tid_sidste_lokation TIMESTAMP,
  PRIMARY KEY (id)
);
`

module.exports = Node;