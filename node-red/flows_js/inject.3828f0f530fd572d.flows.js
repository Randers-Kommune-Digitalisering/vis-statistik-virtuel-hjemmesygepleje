const Node = {
  "id": "3828f0f530fd572d",
  "type": "inject",
  "z": "971a7ae6df987a48",
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
    },
    {
      "p": "filename",
      "v": "2017.csv",
      "vt": "str"
    }
  ],
  "repeat": "",
  "crontab": "",
  "once": false,
  "onceDelay": 0.1,
  "topic": "",
  "x": 1210,
  "y": 460,
  "wires": [
    [
      "191801912cae56d3",
      "dec51ee954d8e78e"
    ]
  ],
  "_order": 61
}

module.exports = Node;