const Node = {
  "id": "0faa5095e2abca1a",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "name": "",
  "property": "filetype",
  "propertyType": "msg",
  "rules": [
    {
      "t": "eq",
      "v": "knox",
      "vt": "str"
    },
    {
      "t": "eq",
      "v": "vitacomm",
      "vt": "str"
    },
    {
      "t": "else"
    }
  ],
  "checkall": "false",
  "repair": false,
  "outputs": 3,
  "x": 330,
  "y": 380,
  "wires": [
    [
      "ba72219c15417867"
    ],
    [
      "179ebe244cb51d47"
    ],
    [
      "4de6a633fcfe1231"
    ]
  ],
  "_order": 99
}

module.exports = Node;