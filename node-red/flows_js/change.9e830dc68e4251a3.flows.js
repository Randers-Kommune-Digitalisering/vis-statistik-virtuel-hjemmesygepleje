const Node = {
  "id": "9e830dc68e4251a3",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "db20f1c3d096597b",
  "name": "Next file",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "$flowContext(\"fileList\")[$flowContext(\"loop.fileCount_current\") ~> $number()]",
      "tot": "jsonata"
    },
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload",
      "tot": "msg",
      "dc": true
    },
    {
      "t": "delete",
      "p": "payload.longname",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "payload.attrs",
      "pt": "msg"
    },
    {
      "t": "delete",
      "p": "parts",
      "pt": "msg"
    },
    {
      "t": "set",
      "p": "loop.fileCount_current",
      "pt": "flow",
      "to": "$flowContext(\"loop.fileCount_current\") +1",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 260,
  "y": 560,
  "wires": [
    [
      "500dcf2064991de6"
    ]
  ],
  "_order": 52
}

module.exports = Node;