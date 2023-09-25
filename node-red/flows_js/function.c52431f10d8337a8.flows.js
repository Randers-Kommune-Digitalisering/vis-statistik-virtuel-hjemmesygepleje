const Node = {
  "id": "c52431f10d8337a8",
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
  "y": 360,
  "wires": [
    [
      "f9b56a0aca89a817"
    ]
  ],
  "_order": 112
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  msg.sql_tablet = "INSERT IGNORE INTO tablet VALUES "
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql_tablet += `('${msg.payload[i].id}','${msg.payload[i].sidst_set}')`;
      if (i < msg.payload.length - 1) msg.sql_tablet += ',';
      
  }
  msg.sql_lokation = "INSERT IGNORE INTO lokation (tid, latitude, longitude, tablet_id) VALUES "
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql_lokation += `('${msg.payload[i].tid_sidste_lokation}', ${msg.payload[i].latitude},${msg.payload[i].longitude}, '${msg.payload[i].id}')`;
      if (i < msg.payload.length - 1) msg.sql_lokation += ',';
  
  }
  return msg;
}

module.exports = Node;