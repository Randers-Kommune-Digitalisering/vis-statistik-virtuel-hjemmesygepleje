const Node = {
  "id": "179ebe244cb51d47",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "konverter vitacomm data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"id\": CallId,\t    \"enhed\": $.\"Organisatorisk enhed\", \t    \"besvaret\": $contains(Slutresultat, \"Opkald besvare\"),\t    \"varighed\": $number($substring(Varighed,6)) +  $number($substring(Varighed, 3,2))*60 + $number($substring(Varighed,0,2))*60*60,\t    \"fra\": $contains($.\"Opkald fra\", \"Medarbejder\") ? \"medarbejder\" : \"borger\",\t    \"til\": $contains($.\"Opkald til\", \"Medarbejder\") ? \"medarbejder\" : \"borger\"\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 510,
  "y": 420,
  "wires": [
    [
      "2eeb8241fa47f222"
    ]
  ],
  "_order": 99
}

module.exports = Node;