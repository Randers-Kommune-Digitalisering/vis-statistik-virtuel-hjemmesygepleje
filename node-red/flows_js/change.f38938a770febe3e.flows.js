const Node = {
  "id": "f38938a770febe3e",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "name": "filter data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.nexus.\t{\t    \"district\": $.\"Organisation (Niveau 09)\",\t    \"citizens\": $.\"Antal borgere (i)\",\t    \"citizensPlannedScreen\": $.\"Antal borgere planlagt(i)(skærm)\",\t    \"citizensDeliveredScreen\": $.\"Antal borgere leveret(i)(skærm)\",\t    \"timePlanned\": $round($.\"Planlagt tid (timer)\" * 3600),\t    \"timeDelivered\": $round($.\"Leveret tid (timer)\" * 3600),\t    \"timePlannedScreen\": $round($.\"Planlagt tid (timer)(skærm)\" * 3600),\t    \"timeDeliveredScreen\": $round($.\"Leveret tid (timer)(skærm)\" * 3600),\t    \"screensAvailable\": $.\"Ledig skærm\" = null ? 0 : $.\"Ledig skærm\",\t    \"screensOnloan\": $.\"Udlånt skærm\"= null ? 0 : $.\"Udlånt skærm\"\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 740,
  "y": 420,
  "wires": [
    [
      "8c007f8cdabe607c"
    ]
  ],
  "_order": 187
}

module.exports = Node;