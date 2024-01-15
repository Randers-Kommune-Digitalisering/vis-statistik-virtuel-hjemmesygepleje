const Node = {
  "id": "e1643981.20d7c8",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "8442dad57efd375b",
  "name": "html",
  "field": "payload",
  "fieldType": "msg",
  "format": "handlebars",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 1070,
  "y": 180,
  "wires": [
    [
      "7d8e179a.283e4"
    ]
  ],
  "_order": 92
}

Node.template = `
<p>Filen {{name}} er blevet uploadet.</p>
<form action="/upload" method="GET">
    <input type="submit" value="Upload flere filer">
</form>
`

module.exports = Node;