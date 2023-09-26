const Node = {
  "id": "bbea64e8179a9b20",
  "type": "switch",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "",
  "property": "sql_lokation",
  "propertyType": "msg",
  "rules": [
    {
      "t": "empty"
    },
    {
      "t": "nempty"
    }
  ],
  "checkall": "true",
  "repair": false,
  "outputs": 2,
  "x": 950,
  "y": 480,
  "wires": [
    [
      "ba16d275d6648e99"
    ],
    [
      "7fb8cc5227d440e6"
    ]
  ],
  "_order": 118
}

module.exports = Node;