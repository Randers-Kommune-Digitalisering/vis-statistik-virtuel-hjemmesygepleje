const Node = {
  "id": "9e4542992d182d44",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL nexus tablets",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 630,
  "y": 720,
  "wires": [
    [
      "d826af94fc94f8bc"
    ]
  ],
  "_order": 146
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.tablet_nexus_table}} (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  enhed TINYTEXT,
  udlaante SMALLINT UNSIGNED,
  ledige SMALLINT UNSIGNED,
  uge TINYTEXT,
  PRIMARY KEY (id)
);
`

module.exports = Node;