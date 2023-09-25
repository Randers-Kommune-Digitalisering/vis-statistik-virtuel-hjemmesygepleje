const Node = {
  "id": "1067d76987391306",
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
  "y": 580,
  "wires": [
    [
      "1988eae1306cbe10"
    ]
  ],
  "_order": 104
}

Node.template = `
CREATE TABLE IF NOT EXISTS opkald (
  id CHAR(36) NOT NULL,
  enhed TINYTEXT,
  besvaret TINYINT(1),
  varighed INT UNSIGNED,
  fra ENUM('borger', 'medarbejder'),
  til ENUM('borger', 'medarbejder'),
  CONSTRAINT opkald_id PRIMARY KEY (id)
);
`

module.exports = Node;