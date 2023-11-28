const Node = {
  "id": "ce75e98f5fc2f4cc",
  "type": "switch",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "",
  "property": "statusCode",
  "propertyType": "msg",
  "rules": [
    {
      "t": "eq",
      "v": "200",
      "vt": "str"
    },
    {
      "t": "else"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 110,
  "y": 280,
  "wires": [
    [
      "7c6cb2f23d9b0956"
    ],
    []
  ],
  "_order": 171
}

module.exports = Node;