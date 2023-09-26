const Node = {
  "id": "c52431f10d8337a8",
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
  "y": 380,
  "wires": [
    [
      "f9b56a0aca89a817"
    ]
  ],
  "_order": 115
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const tablet_table = flow.get('tablet_table');
  msg.sql_tablet = `INSERT IGNORE INTO ${tablet_table} VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql_tablet += `('${msg.payload[i].id}','${msg.payload[i].sidst_set}')`;
      if (i < msg.payload.length - 1) msg.sql_tablet += ',';
      
  }
  
  const location_table = flow.get('location_table');
  msg.sql_lokation = `INSERT IGNORE INTO ${location_table} (tid, latitude, longitude, tablet_id) VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      // Only add location if it has data
      if (msg.payload[i].latitude && msg.payload[i].longitude) {
          msg.sql_lokation += `('${msg.payload[i].tid_sidste_lokation}', ${msg.payload[i].latitude},${msg.payload[i].longitude}, '${msg.payload[i].id}')`;
          if (i < msg.payload.length - 1) msg.sql_lokation += ',';
      }
  }
  // Remove last character if it is ','
  if (msg.sql_lokation.charAt(msg.sql_lokation.length - 1) === ',') msg.sql_lokation.slice(0, -1);
  return msg;
}

module.exports = Node;