const Node = {
  "id": "42ba182088ec60bf",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "name": "move data and set table",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.service",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "table",
      "pt": "msg",
      "to": "service_table",
      "tot": "flow"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 790,
  "y": 460,
  "wires": [
    [
      "141a9ccf8e318faf"
    ]
  ],
  "_order": 211
}

module.exports = Node;