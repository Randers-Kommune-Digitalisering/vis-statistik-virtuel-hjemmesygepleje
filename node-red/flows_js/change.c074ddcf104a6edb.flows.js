const Node = {
  "id": "c074ddcf104a6edb",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "name": "move data and set table",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.screenservice",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "table",
      "pt": "msg",
      "to": "screenservice_table",
      "tot": "flow"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 790,
  "y": 500,
  "wires": [
    [
      "141a9ccf8e318faf"
    ]
  ],
  "_order": 210
}

module.exports = Node;