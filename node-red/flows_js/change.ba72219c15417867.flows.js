const Node = {
  "id": "ba72219c15417867",
  "type": "change",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "konverter knox data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"id\": $.\"IMEI / MEID\",\t    \"sidst_set\": $fromMillis($toMillis($pad($flowContext(\"datetime\"), 19, \":00\")) - (function($num, $unit){$unit = \"m\" ? $num * 60 * 1000 : $unit = \"h\" ?  $num * 60 * 60 * 1000 : $unit = \"d\" ? $num * 24 * 60 * 60 * 1000 : 365 * 24 * 60 * 60 * 1000}($number($substring($.\"Last Seen\", 0, $length($.\"Last Seen\")-1)), $substring($.\"Last Seen\", $length($.\"Last Seen\")-1, 1)))),\t    \"latitude\": $.\"Last Location\" ? $number($split($trim($substringBefore($.\"Last Location\", \"(\")),\",\")[0]) : null,\t    \"longitude\": $.\"Last Location\" ? $number($trim($split($trim($substringBefore($.\"Last Location\", \"(\")),\",\")[1])) : null,\t    \"tid_sidste_lokation\": $.\"Last Location\" ? $split($substring($substringAfter($.\"Last Location\", \"(\"), 0, 23), \" \")[0] & \"T\" & $split($substring($substringAfter($.\"Last Location\", \"(\"), 0, 23), \" \")[1] &\".000Z\" : null\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 490,
  "y": 380,
  "wires": [
    [
      "c52431f10d8337a8"
    ]
  ],
  "_order": 113
}

module.exports = Node;