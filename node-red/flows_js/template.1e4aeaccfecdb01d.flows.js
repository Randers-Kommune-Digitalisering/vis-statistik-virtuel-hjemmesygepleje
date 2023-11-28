const Node = {
  "id": "1e4aeaccfecdb01d",
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
  "y": 220,
  "wires": [
    [
      "7d8e179a.283e4"
    ]
  ],
  "_order": 93
}

Node.template = `
<p>{{errMsgUser}}</p>
<form action="/upload" method="GET">
    <input type="submit" value="Upload en anden fil">
</form>
`

module.exports = Node;