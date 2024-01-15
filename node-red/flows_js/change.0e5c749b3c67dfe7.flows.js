const Node = {
  "id": "0e5c749b3c67dfe7",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "eb678f5d548bb82e",
  "name": "Create data obj",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "{\t    \"fileData\": payload,\t    \"fileMeta\": $flowContext(\"fileList\")[(($flowContext(\"loop.fileCount_current\") ~> $number()) - 1)]\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 360,
  "y": 780,
  "wires": [
    [
      "87f5ac2e106cf827"
    ]
  ],
  "_order": 83
}

module.exports = Node;