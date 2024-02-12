const Node = {
  "id": "882db9b4a83ac78a",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "konverter skærme data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"enhed\": $.\"Organisation (Niveau 09)\",\t    \"udlaante\": $.\"Udlånt skærm\",\t    \"ledige\": $.\"Ledig skærm\",\t    \"uge\": $flowContext(\"week\")\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 510,
  "y": 500,
  "wires": [
    [
      "1eb2a00dfccb201d"
    ]
  ],
  "_order": 148
}

module.exports = Node;