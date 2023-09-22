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
  "x": 450,
  "y": 80,
  "wires": [
    [
      "737e44d2.373a64"
    ]
  ],
  "_order": 80
}

Node.template = `
<!-- moment libary made available with httpstatic in settings.js file, the libary is located in node-red/scripts -->
<script src="moment-with-locales.min.js"></script>
<script src="moment-timezone-with-data.js"></script>

<h1>Upload en fil her:</h1>

<form action="/upload" method="POST" enctype="multipart/form-data">
  <label for="filetype">Vælg en filtype:</label>
  <select name="filetype" id="filetype">
    <option value="unknown">Ukendt</option>
    <option value="knox">Knox</option>
    <option value="vitacomm">Vitacomm</option>
  </select>
    <input id="datetime" type="hidden" name="datetime">
    <input id="file" type="file" name="file" accept=".csv"/>
    <input disabled type="submit" id="submit" value="Indsend">
</form>

<script>{{{payload.js}}}</script>
`

module.exports = Node;