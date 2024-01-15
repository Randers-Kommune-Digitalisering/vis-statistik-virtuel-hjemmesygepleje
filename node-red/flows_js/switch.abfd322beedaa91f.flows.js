const Node = {
  "id": "abfd322beedaa91f",
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
  "x": 830,
  "y": 120,
  "wires": [
    [
      "192134936134d85e"
    ],
    []
  ],
  "_order": 176
}

module.exports = Node;