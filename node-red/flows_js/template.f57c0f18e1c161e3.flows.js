const Node = {
  "id": "f57c0f18e1c161e3",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL nexus",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 640,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 196
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.nexus_table}} (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  citizens SMALLINT UNSIGNED,
  citizensPlannedScreen SMALLINT UNSIGNED,
  citizensDeliveredScreen SMALLINT UNSIGNED,
  screensAvailable SMALLINT UNSIGNED,
  screensOnloan SMALLINT UNSIGNED,
  yearWeek TINYTEXT,
  timePlanned INT UNSIGNED,
  timeDelivered INT UNSIGNED,
  timePlannedScreen INT UNSIGNED,
  timeDeliveredScreen INT UNSIGNED,
  districtId MEDIUMINT UNSIGNED NOT NULL,
  UNIQUE KEY \`unique_nexus\`(yearWeek,districtId),
  CONSTRAINT \`fk_nexus_district\` FOREIGN KEY (districtId) REFERENCES {{flow.district_table}} (id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  PRIMARY KEY (id)
);
`

module.exports = Node;