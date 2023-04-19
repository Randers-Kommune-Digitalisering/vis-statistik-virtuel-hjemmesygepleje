const Node = {
  "id": "811cb608fa49c298",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "db20f1c3d096597b",
  "name": "Generate new request",
  "rules": [
    {
      "t": "set",
      "p": "host",
      "pt": "msg",
      "to": "VIEWCARE_SFTP_URL",
      "tot": "env"
    },
    {
      "t": "set",
      "p": "user",
      "pt": "msg",
      "to": "VIEWCARE_SFTP_USER",
      "tot": "env"
    },
    {
      "t": "set",
      "p": "password",
      "pt": "msg",
      "to": "VIEWCARE_SFTP_PASS",
      "tot": "env"
    },
    {
      "t": "set",
      "p": "workdir",
      "pt": "msg",
      "to": "Randers",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "payload.filename",
      "pt": "msg",
      "to": "workdir & \"/\" & payload.filename",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 200,
  "y": 920,
  "wires": [
    [
      "f003f933e402e403"
    ]
  ],
  "_order": 75
}

module.exports = Node;