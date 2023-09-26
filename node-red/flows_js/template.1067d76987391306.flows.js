const Node = {
  "id": "1067d76987391306",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL opkald",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 580,
  "wires": [
    [
      "d826af94fc94f8bc"
    ]
  ],
  "_order": 100
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.call_table}} (
  id CHAR(36) NOT NULL,
  enhed TINYTEXT,
  besvaret TINYINT(1),
  tidspunkt TIMESTAMP,
  varighed INT UNSIGNED,
  fra ENUM('borger', 'medarbejder'),
  til ENUM('borger', 'medarbejder'),
  PRIMARY KEY (id)
);
`

module.exports = Node;