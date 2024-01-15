const Node = {
  "id": "7a810cb7fc1cf90b",
  "type": "change",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "filter data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "payload.\t{\t    \"callerDistrict\": $.\"Caller OU\",\t    \"calleeDistrict\": $trim($substringAfter($.\"Callee OU\", \":\")),\t    \"calleeCpr\": $trim($substringAfter($.\"Callee's CPR\", \":\")),\t    \"calleeName\": $trim($substringAfter($.\"Callee\", \":\")),\t    \"callerRole\": $.\"Caller's role\",\t    \"calleeRole\":  $trim($substringAfter($.\"Callee's role\", \":\")),\t    \"startTime\": $.\"Start time\" ? $fromMillis($toMillis($.\"Start time\")) : null,\t    \"endTime\": $.\"End time\" ? $fromMillis($toMillis($.\"End time\")) : null,\t    \"duration\": $.\"Duration (seconds)\",\t    \"endReason\": $.\"End reason\"\t}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 800,
  "y": 260,
  "wires": [
    [
      "759d5e5fa770315c"
    ]
  ],
  "_order": 178
}

module.exports = Node;