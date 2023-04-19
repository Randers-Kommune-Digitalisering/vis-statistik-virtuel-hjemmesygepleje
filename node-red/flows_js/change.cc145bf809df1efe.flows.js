const Node = {
  "id": "cc145bf809df1efe",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "3ba1151908a2dc5c",
  "name": "Byg dataobjekt",
  "rules": [
    {
      "t": "set",
      "p": "data",
      "pt": "msg",
      "to": "{\t   \"Month\" : payload.Month,\t   \"Industrycode_DE35\": payload.Industrycode_DE35,\t   \"TotalConsumption\": payload.TotalCon\t}\t",
      "tot": "jsonata"
    },
    {
      "t": "delete",
      "p": "payload",
      "pt": "msg"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 480,
  "y": 1300,
  "wires": [
    [
      "9855edb28573cd20"
    ]
  ],
  "_order": 56
}

module.exports = Node;