const Node = {
  "id": "1067d76987391306",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL video calls",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 620,
  "y": 640,
  "wires": [
    [
      "d826af94fc94f8bc"
    ]
  ],
  "_order": 105
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.call_table}} (
  id CHAR(36) NOT NULL,
  enhed TINYTEXT,
  besvaret TINYINT(1),
  tidspunkt TIMESTAMP,
  uge TINYTEXT,
  varighed TIME,
  fra ENUM('borger', 'medarbejder'),
  til ENUM('borger', 'medarbejder'),
  navn TINYTEXT,
  PRIMARY KEY (id)
);
`

module.exports = Node;