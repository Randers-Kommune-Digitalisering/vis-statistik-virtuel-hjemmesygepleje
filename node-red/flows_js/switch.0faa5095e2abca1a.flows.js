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
      "t": "eq",
      "v": "borgere",
      "vt": "str"
    },
    {
      "t": "eq",
      "v": "skærme",
      "vt": "str"
    },
    {
      "t": "else"
    }
  ],
  "checkall": "false",
  "repair": false,
  "outputs": 5,
  "x": 290,
  "y": 460,
  "wires": [
    [
      "ba72219c15417867"
    ],
    [
      "f516441356147238"
    ],
    [
      "c478ae846b0e472c"
    ],
    [
      "882db9b4a83ac78a"
    ],
    [
      "4de6a633fcfe1231"
    ]
  ],
  "_order": 107
}

module.exports = Node;