const Node = {
  "id": "2eeb8241fa47f222",
  "type": "function",
  "z": "39989dadda5c9a15",
  "name": "byg SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 760,
  "y": 400,
  "wires": [
    []
  ],
  "_order": 108
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  msg.sql = "INSERT IGNORE INTO opkald VALUES "
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql += `('${msg.payload[i].id}','${msg.payload[i].enhed}',${msg.payload[i].besvaret},${msg.payload[i].varighed},'${msg.payload[i].fra}', '${msg.payload[i].til}')`;
      if(i<msg.payload.length-1) msg.sql += ',';
      
  }
  return msg
}

module.exports = Node;