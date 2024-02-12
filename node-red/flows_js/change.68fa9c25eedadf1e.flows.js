const Node = {
  "id": "68fa9c25eedadf1e",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "b09eaaaca527ddf5",
  "name": "set table names",
  "rules": [
    {
      "t": "set",
      "p": "call_table",
      "pt": "flow",
      "to": "videocall",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "device_table",
      "pt": "flow",
      "to": "device",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "nexus_table",
      "pt": "flow",
      "to": "nexus",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "district_table",
      "pt": "flow",
      "to": "district",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "service_table",
      "pt": "flow",
      "to": "service",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "screenservice_table",
      "pt": "flow",
      "to": "screenservice",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "setup",
      "pt": "msg",
      "to": "true",
      "tot": "bool"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 360,
  "y": 560,
  "wires": [
    [
      "8f0e62bd9d24e259",
      "62f7e6cb8891228f",
      "f57c0f18e1c161e3",
      "75764ec5855f3ac1",
      "a4d97228d2a046e3",
      "26f0fbce71b1ef64"
    ]
  ],
  "_order": 195
}

module.exports = Node;