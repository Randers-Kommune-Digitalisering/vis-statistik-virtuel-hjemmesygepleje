const Node = {
  "id": "927f26bdeb11c581",
  "type": "inject",
  "z": "971a7ae6df987a48",
  "g": "e183203bdc1f7193",
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
    },
    {
      "p": "payload.filename",
      "v": "randersall.csv",
      "vt": "str"
    },
    {
      "p": "payload.filename",
      "v": "workdir & \"/\" & payload.filename",
      "vt": "jsonata"
    }
  ],
  "repeat": "",
  "crontab": "",
  "once": false,
  "onceDelay": 0.1,
  "topic": "",
  "payload": "{}",
  "payloadType": "json",
  "x": 1310,
  "y": 720,
  "wires": [
    [
      "919ae4955014270c"
    ]
  ],
  "_order": 49
}

module.exports = Node;