const Node = {
  "id": "b8439653ef8cb129",
  "type": "template",
  "z": "39989dadda5c9a15",
  "name": "SQL lokation",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 430,
  "y": 700,
  "wires": [
    [
      "1988eae1306cbe10"
    ]
  ],
  "_order": 109
}

Node.template = `
CREATE TABLE IF NOT EXISTS lokation (
  id  MEDIUMINT NOT NULL AUTO_INCREMENT,
  tid TIMESTAMP,
  latitude DECIMAL(8,6),
  longitude DECIMAL(9,6),
  tablet_id CHAR(15),
  CONSTRAINT lokation_id PRIMARY KEY (id),
  FOREIGN KEY (tablet_id) REFERENCES tablet(id)
);
`

module.exports = Node;