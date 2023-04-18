const Node = {
  "id": "36696035aee1c3c1",
  "type": "change",
  "z": "971a7ae6df987a48",
  "name": "",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "$keys(payload) @$key . {\t    \"key\": $key,\t    \"header\": payload[0]\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 880,
  "y": 1040,
  "wires": [
    []
  ],
  "_order": 56
}

module.exports = Node;