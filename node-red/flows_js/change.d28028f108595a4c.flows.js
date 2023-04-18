const Node = {
  "id": "d28028f108595a4c",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5b803f1c3bcb0822",
  "name": "Oprydning i  \\n uaktuelle parametre",
  "rules": [
    {
      "t": "delete",
      "p": "url",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "method",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "headers",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "cronplus",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "manualTrigger",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "scheduledEvent",
      "pt": "msg"
    },
    {
      "t": "set",
      "p": "payload.success",
      "pt": "msg",
      "to": "false",
      "tot": "bool"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 820,
  "y": 520,
  "wires": [
    []
  ],
  "_order": 38
}

module.exports = Node;