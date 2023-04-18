const Node = {
  "id": "13e4ce3715ad282c",
  "type": "change",
  "z": "971a7ae6df987a48",
  "g": "5b803f1c3bcb0822",
  "name": "Opsætning af forespørgsel ↓ \\n Hent metadata på senest \\n opdaterede datafil",
  "rules": [
    {
      "t": "set",
      "p": "url",
      "pt": "msg",
      "to": "https://admin.opendata.dk/api/3/action/package_show",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "method",
      "pt": "msg",
      "to": "POST",
      "tot": "str"
    },
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "{\"include_tracking\":false,\"include_tracking_children\":false,\"sort\":\"resources.metadata_modified desc\"}",
      "tot": "json"
    },
    {
      "t": "set",
      "p": "payload.id",
      "pt": "msg",
      "to": "antal-krydsende-cyklister-over-randers-fjord",
      "tot": "str"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 200,
  "y": 440,
  "wires": [
    []
  ],
  "info": "",
  "_order": 28
}

Node.info = `
https://www.opendata.dk/randers-kommune/antal-krydsende-cyklister-over-randers-fjord
`

module.exports = Node;