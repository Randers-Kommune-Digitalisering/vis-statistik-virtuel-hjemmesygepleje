const Node = {
  "id": "3153fbd3.203a64",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "b95d463f67a7a194",
  "name": "html",
  "field": "payload",
  "fieldType": "msg",
  "format": "handlebars",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 470,
  "y": 80,
  "wires": [
    [
      "737e44d2.373a64"
    ]
  ],
  "_order": 69
}

Node.template = `
<h1>Upload en fil her:</h1>

<form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="myFile" accept=".csv"/>
    <input type="submit" value="Indsend">
</form>
`

module.exports = Node;