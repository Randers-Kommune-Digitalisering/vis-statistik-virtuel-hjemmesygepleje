const Node = {
  "id": "927f26bdeb11c581",
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
    },
    {
      "p": "payload.filename",
      "v": "randers2020eksempel.xlsx",
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
  "x": 170,
  "y": 500,
  "wires": [
    [
      "919ae4955014270c"
    ]
  ],
  "_order": 40
}

module.exports = Node;