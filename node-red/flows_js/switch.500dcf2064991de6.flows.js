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
      "t": "eq",
      "v": "true",
      "vt": "jsonata"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 1,
  "x": 190,
  "y": 880,
  "wires": [
    [
      "9ee61206bfc6078c"
    ]
  ],
  "_order": 85
}

module.exports = Node;