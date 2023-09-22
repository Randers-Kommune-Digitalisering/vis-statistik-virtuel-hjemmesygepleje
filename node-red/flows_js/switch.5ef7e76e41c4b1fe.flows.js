const Node = {
  "id": "5ef7e76e41c4b1fe",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "tjek for fejl",
  "property": "errMsgUser",
  "propertyType": "msg",
  "rules": [
    {
      "t": "nempty"
    },
    {
      "t": "false"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 850,
  "y": 200,
  "wires": [
    [
      "1e4aeaccfecdb01d"
    ],
    [
      "e1643981.20d7c8"
    ]
  ],
  "_order": 93
}

module.exports = Node;