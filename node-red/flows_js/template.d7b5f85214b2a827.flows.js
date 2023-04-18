const Node = {
  "id": "d7b5f85214b2a827",
  "type": "template",
  "z": "971a7ae6df987a48",
  "g": "43dc5f7a23936f1d",
  "name": "Forespørgsel ↓\\n Indsæt eller opdater \\n data i tabel",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 320,
  "y": 1140,
  "wires": [
    [
      "e7203cc4056ebbb4"
    ]
  ],
  "_order": 50
}

Node.template = `
INSERT INTO {{flow.tablename}} 
    (Month,	stat1, stat2)
VALUES( 
        '{{{data.stat1}}}',
        '{{{data.stat2}}}'
        )
ON DUPLICATE KEY UPDATE
    stat1 = '{{data.stat1}}'
`

module.exports = Node;