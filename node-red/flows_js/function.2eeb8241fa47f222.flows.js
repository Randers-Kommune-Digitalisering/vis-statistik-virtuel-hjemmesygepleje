const Node = {
  "id": "2eeb8241fa47f222",
  "type": "function",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "byg SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 720,
  "y": 420,
  "wires": [
    [
      "3bb28f11aade4b81"
    ]
  ],
  "_order": 116
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = flow.get("call_table");
  msg.sql = `INSERT IGNORE INTO ${table} VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql += `('${msg.payload[i].id}','${msg.payload[i].enhed}',${msg.payload[i].besvaret},'${msg.payload[i].tidspunkt}',${msg.payload[i].varighed},'${msg.payload[i].fra}', '${msg.payload[i].til}')`;
      if(i<msg.payload.length-1) msg.sql += ',';
      
  }
  return msg
}

module.exports = Node;