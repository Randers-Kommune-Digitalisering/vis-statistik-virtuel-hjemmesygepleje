const Node = {
  "id": "cabaa0127db8b20a",
  "type": "template",
  "z": "971a7ae6df987a48",
  "g": "0b6a3796775ca5e9",
  "name": "Forespørgsel ↓\\n Hent dato for seneste række ",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 200,
  "y": 280,
  "wires": [
    [
      "8899c8d86911d51f"
    ]
  ],
  "_order": 27
}

Node.template = `
SELECT MAX(Month) as latest_month
FROM {{flow.tablename}}
`

module.exports = Node;