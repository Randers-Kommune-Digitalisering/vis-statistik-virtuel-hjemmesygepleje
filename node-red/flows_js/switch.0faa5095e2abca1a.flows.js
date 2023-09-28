const Node = {
  "id": "0faa5095e2abca1a",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
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
  "x": 290,
  "y": 400,
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
  "_order": 109
}

module.exports = Node;