const Node = {
  "id": "b8439653ef8cb129",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL lokation",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 700,
  "wires": [
    [
      "9be36ce2a03bc27d"
    ]
  ],
  "_order": 102
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.location_table}} (
  id  MEDIUMINT NOT NULL AUTO_INCREMENT,
  tid TIMESTAMP,
  latitude DECIMAL(8,6),
  longitude DECIMAL(9,6),
  tablet_id CHAR(15),
  PRIMARY KEY (id),
  FOREIGN KEY (tablet_id) REFERENCES tablet(id)
)
`

module.exports = Node;