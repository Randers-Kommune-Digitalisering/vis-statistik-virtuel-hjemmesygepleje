const Node = {
  "id": "500dcf2064991de6",
  "type": "switch",
  "z": "971a7ae6df987a48",
  "g": "db20f1c3d096597b",
  "name": "Filter out non-CSV",
  "property": "$contains(payload.filename, \".csv\")",
  "propertyType": "jsonata",
  "rules": [
    {
      "t": "false"
    },
    {
      "t": "true"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 470,
  "y": 920,
  "wires": [
    [
      "6cb78c218ecfb35f"
    ],
    [
      "811cb608fa49c298"
    ]
  ],
  "_order": 81
}

module.exports = Node;