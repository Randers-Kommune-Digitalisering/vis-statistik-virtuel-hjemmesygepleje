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
  "x": 220,
  "y": 620,
  "wires": [
    [
      "c09b6726931f8437",
      "2c6db246b8a5b99e"
    ]
  ],
  "_order": 66
}

module.exports = Node;