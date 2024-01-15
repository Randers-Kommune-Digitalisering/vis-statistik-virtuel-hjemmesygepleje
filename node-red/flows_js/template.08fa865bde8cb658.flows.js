const Node = {
  "id": "08fa865bde8cb658",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL opkald",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 430,
  "y": 1240,
  "wires": [
    [
      "7921205c3577f96f"
    ]
  ],
  "_order": 135
}

Node.template = `
CREATE TABLE IF NOT EXISTS test_1 (
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