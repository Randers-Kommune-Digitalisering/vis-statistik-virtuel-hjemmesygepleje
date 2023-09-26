const Node = {
  "id": "892a33d0eb11bd12",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5c29b0234ffc82a9",
  "name": "Set fileList + loop count",
  "rules": [
    {
      "t": "set",
      "p": "fileList",
      "pt": "flow",
      "to": "payload",
      "tot": "msg",
      "dc": true
    },
    {
      "t": "set",
      "p": "fileList",
      "pt": "flow",
      "to": "$flowContext(\"fileList\") ~> | $ | ({\t    \"status\":\t    {\t        \"download_started\": false,\t        \"download_started_millis\": 0,\t        \"download_finished\": false,\t        \"download_finished_millis\": 0,\t        \"download_time\": {},\t        \"download_speed\": 0\t    }\t}\t)|",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "loop",
      "pt": "flow",
      "to": "{\t    \"fileCount_total\": $flowContext(\"fileList\") ~> $count(),\t    \"fileCount_current\": 0\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 750,
  "y": 380,
  "wires": [
    [
      "17b1bf0db2361f97"
    ]
  ],
  "_order": 73
}

module.exports = Node;