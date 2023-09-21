const Node = {
  "id": "4a39b3af874858ce",
  "type": "switch",
  "z": "971a7ae6df987a48",
  "g": "db20f1c3d096597b",
  "name": "More files?",
  "property": "$flowContext(\"loop.fileCount_current\") < $flowContext(\"loop.fileCount_total\")",
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
  "x": 250,
  "y": 500,
  "wires": [
    [
      "8a8a76f130f7e507"
    ],
    [
      "9e830dc68e4251a3"
    ]
  ],
  "_order": 60
}

module.exports = Node;