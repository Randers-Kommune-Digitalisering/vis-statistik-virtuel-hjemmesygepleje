const Node = {
  "id": "8f0e62bd9d24e259",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL screenservice",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 590,
  "y": 760,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 210
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.screenservice_table}} (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  visits SMALLINT UNSIGNED,
  name TINYTEXT,
  yearWeek TINYTEXT,
  districtId MEDIUMINT UNSIGNED NOT NULL,
  UNIQUE KEY \`unique_service\`(yearWeek,districtId,name),
  CONSTRAINT \`fk_screenservice_district\` FOREIGN KEY (districtId) REFERENCES {{flow.district_table}} (id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  PRIMARY KEY (id)
);
`

module.exports = Node;