const Node = {
  "id": "a4d97228d2a046e3",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL calls",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 620,
  "y": 560,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 193
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.call_table}} (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  startTime DATETIME,
  endTime DATETIME,
  calleeCpr TINYTEXT,
  calleeName TINYTEXT,
  calleeRole TINYTEXT,
  calleeDistrictId MEDIUMINT UNSIGNED NOT NULL,
  duration INT,
  callerRole TINYTEXT,
  callerDistrictId MEDIUMINT UNSIGNED NOT NULL,
  endReason TINYTEXT,
  yearWeek TINYTEXT,
  PRIMARY KEY (id),
  UNIQUE \`unique_call\`(calleeName,calleeCpr,startTime),
  CONSTRAINT \`fk_callee_district\` FOREIGN KEY (calleeDistrictId) REFERENCES {{flow.district_table}} (id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT \`fk_caller_district\` FOREIGN KEY (callerDistrictId) REFERENCES {{flow.district_table}} (id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
);
`

module.exports = Node;