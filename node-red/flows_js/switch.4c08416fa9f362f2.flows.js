const Node = {
  "id": "4c08416fa9f362f2",
  "type": "switch",
  "z": "aa5f3f9006d25110",
  "name": "",
  "property": "payload",
  "propertyType": "msg",
  "rules": [
    {
      "t": "hask",
      "v": "nexus",
      "vt": "str"
    },
    {
      "t": "hask",
      "v": "service",
      "vt": "str"
    },
    {
      "t": "hask",
      "v": "screenservice",
      "vt": "str"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 3,
  "x": 590,
  "y": 460,
  "wires": [
    [
      "f38938a770febe3e"
    ],
    [
      "42ba182088ec60bf"
    ],
    [
      "c074ddcf104a6edb"
    ]
  ],
  "_order": 209
}

module.exports = Node;