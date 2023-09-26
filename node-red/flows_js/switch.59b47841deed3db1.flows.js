const Node = {
  "id": "59b47841deed3db1",
  "type": "switch",
  "z": "971a7ae6df987a48",
  "g": "616fd052c81e52cc",
  "name": "Tjek om der køres \\n i udviklermiljø",
  "property": "DEV_ENVIROMENT",
  "propertyType": "env",
  "rules": [
    {
      "t": "eq",
      "v": "false",
      "vt": "str"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 1,
  "x": 430,
  "y": 80,
  "wires": [
    [
      "8f35b8f426ac7542"
    ]
  ],
  "_order": 53
}

module.exports = Node;