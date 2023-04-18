const Node = {
  "id": "5b1c780ffe35c1eb",
  "type": "template",
  "z": "971a7ae6df987a48",
  "g": "6aa95c95913a1dc8",
  "name": "Forespørgsel ↓\\n Opret tabel hvis der ikke \\n eksisterer en i forvejen ",
  "field": "topic",
  "fieldType": "msg",
  "format": "sql",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 950,
  "y": 100,
  "wires": [
    [
      "4be122699e16f822"
    ]
  ],
  "_order": 25
}

Node.template = `
CREATE TABLE if not exists {{flow.tablename}} (
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	Month DATE,
	Stat1 DECIMAL(10,2)
	UNIQUE (Month, Stat1)
	);
`

module.exports = Node;