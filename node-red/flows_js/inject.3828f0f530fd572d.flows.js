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
  "x": 1250,
  "y": 480,
  "wires": [
    [
      "191801912cae56d3",
      "dec51ee954d8e78e"
    ]
  ],
  "_order": 61
}

module.exports = Node;