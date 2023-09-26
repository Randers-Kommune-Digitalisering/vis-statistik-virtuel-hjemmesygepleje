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
  "x": 790,
  "y": 460,
  "wires": [
    [
      "ba16d275d6648e99"
    ],
    [
      "bbea64e8179a9b20"
    ]
  ],
  "_order": 117
}

module.exports = Node;