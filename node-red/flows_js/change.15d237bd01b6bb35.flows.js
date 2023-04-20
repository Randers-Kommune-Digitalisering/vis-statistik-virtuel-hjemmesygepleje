const Node = {
  "id": "15d237bd01b6bb35",
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
      "p": "currentStatus.status.download_finished",
      "pt": "msg",
      "to": "true",
      "tot": "bool"
    },
    {
      "t": "set",
      "p": "currentStatus.status.download_finished_millis",
      "pt": "msg",
      "to": "$millis()",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "currentStatus.status.download_time",
      "pt": "msg",
      "to": "{\t    \"totalMillis\": $msElapsed := (currentStatus.status.download_finished_millis - currentStatus.status.download_started_millis),\t    \"totalSeconds\": $sElapsed := ($msElapsed / 1000),\t    \t    \t    \"seconds\": $sMod := ($sElapsed % 60),\t    \"minutes\": $mMod := ($sElapsed - $sMod) / 60,\t\t    \"string\": $mMod & \" mintues and \" & $sMod & \" seconds\"\t}",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "currentStatus.status.download_speed",
      "pt": "msg",
      "to": "currentStatus.status.download_time.totalMillis / currentStatus.attrs.size",
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
  "x": 600,
  "y": 1020,
  "wires": [
    [
      "3b6117467b422dc1"
    ]
  ],
  "_order": 92
}

module.exports = Node;