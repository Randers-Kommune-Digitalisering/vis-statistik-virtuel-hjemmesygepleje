const Node = {
  "id": "179ebe244cb51d47",
  "type": "change",
  "z": "39989dadda5c9a15",
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
  "x": 230,
  "y": 520,
  "wires": [
    []
  ],
  "_order": 85
}

module.exports = Node;