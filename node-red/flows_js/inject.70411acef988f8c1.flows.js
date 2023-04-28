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
      "p": "path",
      "v": "Randers",
      "vt": "str"
    }
  ],
  "repeat": "",
  "crontab": "",
  "once": false,
  "onceDelay": 0.1,
  "topic": "",
  "x": 150,
  "y": 380,
  "wires": [
    [
      "d53549388fa5baab"
    ]
  ],
  "_order": 42
}

module.exports = Node;