const Node = {
  "id": "a437c12bd1accb6b",
  "type": "http request",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "call list",
  "method": "GET",
  "ret": "txt",
  "paytoqs": "ignore",
  "url": "https://vitacomm.dk/api/portal/CallReport/GetCallReport?api_key={{{auth}}}&{{{query}}}",
  "tls": "",
  "persist": false,
  "proxy": "",
  "insecureHTTPParser": false,
  "authType": "",
  "senderr": false,
  "headers": [],
  "x": 730,
  "y": 220,
  "wires": [
    [
      "ce75e98f5fc2f4cc"
    ]
  ],
  "_order": 168
}

module.exports = Node;