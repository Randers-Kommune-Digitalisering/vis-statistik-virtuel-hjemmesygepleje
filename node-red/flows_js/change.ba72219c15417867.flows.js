const Node = {
  "id": "ba72219c15417867",
  "type": "change",
  "z": "39989dadda5c9a15",
  "name": "konverter knox data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"id\": $.\"IMEI / MEID\",\t    \"sidst_set\": $.\"Last Seen\",\t    \"sidste_lokation\": $trim($substringBefore($.\"Last Location\", \"(\")),\t    \"tid_sidste_lokation\":$substring($substringAfter($.\"Last Location\", \"(\"), 0, 23)\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 510,
  "y": 520,
  "wires": [
    []
  ],
  "_order": 86
}

module.exports = Node;