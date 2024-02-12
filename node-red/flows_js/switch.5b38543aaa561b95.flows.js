const Node = {
  "id": "5b38543aaa561b95",
  "type": "switch",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
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
  "y": 120,
  "wires": [
    [
      "f92a3c165d8717bd"
    ],
    []
  ],
  "_order": 165
}

module.exports = Node;