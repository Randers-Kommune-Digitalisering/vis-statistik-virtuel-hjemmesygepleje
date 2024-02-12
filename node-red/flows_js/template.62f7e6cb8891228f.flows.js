const Node = {
  "id": "62f7e6cb8891228f",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL district",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 680,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 198
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.district_table}} (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  vitacommDistrict TINYTEXT,
  nexusDistrict TINYTEXT,
  UNIQUE KEY \`unique_nexus\`(vitacommDistrict,nexusDistrict),
  PRIMARY KEY (id)
);
`

module.exports = Node;