const Node = {
  "id": "5faef195141dffea",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "set msg.query",
  "rules": [
    {
      "t": "set",
      "p": "startDate",
      "pt": "msg",
      "to": "$replace($substringBefore($fromMillis($.\"startDate\"), \".\"), \":\", \"%3A\")",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "endDate",
      "pt": "msg",
      "to": "$replace($substringBefore($fromMillis($.\"endDate\"), \".\"), \":\", \"%3A\")",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "query",
      "pt": "msg",
      "to": "\"from=\" & $.\"startDate\" & \"&to=\" & $.\"endDate\"",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 560,
  "y": 220,
  "wires": [
    [
      "772be21432250748"
    ]
  ],
  "_order": 175
}

module.exports = Node;