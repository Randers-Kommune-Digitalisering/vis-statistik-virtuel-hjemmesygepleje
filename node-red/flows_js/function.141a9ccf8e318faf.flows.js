const Node = {
  "id": "141a9ccf8e318faf",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "transform",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1020,
  "y": 460,
  "wires": [
    [
      "04d3c153b3e35466"
    ]
  ],
  "_order": 214
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  let stripped = msg.payload.map((obj) => {
      return Object.fromEntries(Object.entries(obj).filter(([_, v]) => v != null));
  })
  
  msg.payload = []
  stripped.forEach((obj) => {
      let org = obj["Organisation (Niveau 09)"]
      for (const [key, value] of Object.entries(obj)) {
          if (key != "Organisation (Niveau 09)") {
              msg.payload.push({ "district": org, "name": key, "visits": value, "yearWeek": msg.week})
          }
      }
  })
  
  return msg;
}

module.exports = Node;