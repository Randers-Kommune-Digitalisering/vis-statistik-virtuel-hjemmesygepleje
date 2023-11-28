const Node = {
  "id": "70411acef988f8c1",
  "type": "inject",
  "z": "971a7ae6df987a48",
  "g": "5c29b0234ffc82a9",
  "name": "",
  "props": [
    {
      "p": "host",
      "v": "VIEWCARE_SFTP_URL",
      "vt": "env"
    },
    {
      "p": "user",
      "v": "VIEWCARE_SFTP_USER",
      "vt": "env"
    },
    {
      "p": "password",
      "v": "VIEWCARE_SFTP_PASS",
      "vt": "env"
    },
    {
      "p": "workdir",
      "v": "Randers",
      "vt": "str"
    },
    {
      "p": "payload"
    }
  ],
  "repeat": "",
  "crontab": "",
  "once": false,
  "onceDelay": 0.1,
  "topic": "",
  "payload": "{}",
  "payloadType": "json",
  "x": 150,
  "y": 380,
  "wires": [
    [
      "40a6cbf939d3a282"
    ]
  ],
  "_order": 64
}

module.exports = Node;