const Node = {
  "id": "f516441356147238",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "konverter vitacomm data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"id\": CallId,\t    \"enhed\": $.\"Organisatorisk enhed\", \t    \"besvaret\": $contains(Slutresultat, \"Opkald besvare\"),\t    \"tidspunkt\":$fromMillis($toMillis($.\"Starttidspunkt\", '[D01]-[M01]-[Y0001] [H#1]:[m01]')),\t    \"varighed\": $.\"Varighed\",\t    \"fra\": $contains($.\"Opkald fra\", \"Medarbejder\") ? \"medarbejder\" : \"borger\",\t    \"til\": $contains($.\"Opkald til\", \"Medarbejder\") ? \"medarbejder\" : \"borger\",\t    \"navn\": $trim($substringBefore($.\"Opkald til\", \"(\"))\t}",
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
      "69d681cabe53d7e7"
    ]
  ],
  "_order": 144
}

module.exports = Node;