const Node = {
  "id": "c18499fa36362788",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "65dc7d0c31d8b4a7",
  "name": "SQL citizens",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 760,
  "wires": [
    [
      "d826af94fc94f8bc"
    ]
  ],
  "_order": 151
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.citizen_table}} (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  enhed TINYTEXT,
  borgere SMALLINT UNSIGNED,
  uge TINYTEXT,
  PRIMARY KEY (id)
);
`

module.exports = Node;