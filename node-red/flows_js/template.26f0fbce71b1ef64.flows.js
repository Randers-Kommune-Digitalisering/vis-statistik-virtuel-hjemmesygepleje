const Node = {
  "id": "26f0fbce71b1ef64",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL service",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 720,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 212
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.service_table}} (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  visits SMALLINT UNSIGNED,
  name TINYTEXT,
  yearWeek TINYTEXT,
  districtId MEDIUMINT UNSIGNED NOT NULL,
  UNIQUE KEY \`unique_service\`(yearWeek,districtId,name),
  CONSTRAINT \`fk_service_district\` FOREIGN KEY (districtId) REFERENCES {{flow.district_table}} (id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  PRIMARY KEY (id)
);
`

module.exports = Node;