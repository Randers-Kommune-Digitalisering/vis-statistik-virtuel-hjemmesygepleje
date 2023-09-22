const Node = {
  "id": "f5bfde136b50bdfc",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "antal filer",
  "property": "req.files.length",
  "propertyType": "msg",
  "rules": [
    {
      "t": "eq",
      "v": "1",
      "vt": "num"
    },
    {
      "t": "else"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 280,
  "y": 220,
  "wires": [
    [
      "e7fe4e8ef1ed1761"
    ],
    [
      "0d1d8f61580ad039"
    ]
  ],
  "_order": 87
}

module.exports = Node;