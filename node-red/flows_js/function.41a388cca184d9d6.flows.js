const Node = {
  "id": "41a388cca184d9d6",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1230,
  "y": 120,
  "wires": [
    [
      "6b798cfa6d8e5710"
    ]
  ],
  "_order": 200
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = flow.get("device_table");
  msg.sql = `INSERT IGNORE INTO ${table} VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql += `('${msg.payload[i].id}','${msg.payload[i].imei}', '${msg.payload[i].status}','${msg.payload[i].lastSeen}','${msg.payload[i].updated}')`;
      if (i < msg.payload.length - 1) msg.sql += ',';
  
  }
  msg.sql += `ON DUPLICATE KEY UPDATE status=VALUE(status), lastSeen=VALUE(lastSeen), updated=VALUE(updated)`
  return msg
}

module.exports = Node;