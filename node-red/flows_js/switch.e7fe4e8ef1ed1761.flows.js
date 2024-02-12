const Node = {
  "id": "e7fe4e8ef1ed1761",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "filtype",
  "property": "req.files[0].mimetype",
  "propertyType": "msg",
  "rules": [
    {
      "t": "eq",
      "v": "text/csv",
      "vt": "str"
    },
    {
      "t": "else"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 430,
  "y": 200,
  "wires": [
    [
      "e36d1a434509ae9f"
    ],
    [
      "b4c6c3093f7697c8"
    ]
  ],
  "_order": 95
}

module.exports = Node;