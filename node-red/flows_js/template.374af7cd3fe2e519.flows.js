const Node = {
  "id": "374af7cd3fe2e519",
  "type": "template",
  "z": "971a7ae6df987a48",
  "g": "eeea7645cd4f2c0d",
  "name": "Forespørgsel ↓\\n Indsæt eller opdater \\n data i tabel",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 220,
  "y": 680,
  "wires": [
    [
      "8d36afbf75141029"
    ]
  ],
  "_order": 56
}

Node.template = `
INSERT INTO {{flow.tablename}} 
    (Måned, Biltype, Drivmiddel, Anvendelse, Antal)
VALUES( 
        '{{{data.maaned}}}',
        '{{{data.BILTYPE}}}',
        '{{{data.DRIV}}}',
        '{{{data.BRUG}}}',
        '{{{data.INDHOLD}}}'
        )
ON DUPLICATE KEY UPDATE
    Antal = '{{{data.INDHOLD}}}'
`

module.exports = Node;