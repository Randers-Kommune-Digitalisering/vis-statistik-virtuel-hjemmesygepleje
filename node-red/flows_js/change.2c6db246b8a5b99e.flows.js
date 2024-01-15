const Node = {
  "id": "2c6db246b8a5b99e",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "db20f1c3d096597b",
  "name": "Update status",
  "rules": [
    {
      "t": "set",
      "p": "currentStatus",
      "pt": "msg",
      "to": "$flowContext(\"fileList\")[(($flowContext(\"loop.fileCount_current\") ~> $number()) - 1)]",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "currentStatus.status.download_started",
      "pt": "msg",
      "to": "true",
      "tot": "bool"
    },
    {
      "t": "set",
      "p": "currentStatus.status.download_started_millis",
      "pt": "msg",
      "to": "$millis()",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "currentStatus",
      "pt": "msg",
      "to": "currentStatus",
      "tot": "msg",
      "dc": true
    },
    {
      "t": "delete",
      "p": "currentStatus",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 200,
  "y": 660,
  "wires": [
    [
      "f003f933e402e403"
    ]
  ],
  "_order": 85
}

module.exports = Node;