const Node = {
  "id": "74029abf9e94f1ee",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "tablet opdateret?",
  "property": "payload.affectedRows",
  "propertyType": "msg",
  "rules": [
    {
      "t": "lt",
      "v": "1",
      "vt": "num"
    },
    {
      "t": "gt",
      "v": "0",
      "vt": "num"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 930,
  "y": 420,
  "wires": [
    [
      "926fec043050794d"
    ],
    [
      "7fb8cc5227d440e6"
    ]
  ],
  "_order": 124
}

module.exports = Node;