const Node = {
  "id": "75764ec5855f3ac1",
  "type": "template",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "SQL device",
  "field": "sql",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 610,
  "y": 600,
  "wires": [
    [
      "f32f7c1f820353f3"
    ]
  ],
  "_order": 193
}

Node.template = `
CREATE TABLE IF NOT EXISTS {{flow.device_table}} (
  id CHAR(32) NOT NULL,
  imei CHAR(15) NOT NULL,
  status CHAR(1),
  lastSeen TIMESTAMP,
  updated TIMESTAMP,
  PRIMARY KEY (id)
);
`

module.exports = Node;