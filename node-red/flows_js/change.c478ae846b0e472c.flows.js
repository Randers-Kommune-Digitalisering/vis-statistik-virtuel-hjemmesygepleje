const Node = {
  "id": "c478ae846b0e472c",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "konverter borgere data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"enhed\": $.\"Organisation (Niveau 09)\",\t    \"borgere\": $.\"Antal borgere (i)\",\t    \"uge\": $flowContext(\"week\")\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 500,
  "y": 460,
  "wires": [
    [
      "ab0ecb25a4c2a9d9"
    ]
  ],
  "_order": 141
}

module.exports = Node;