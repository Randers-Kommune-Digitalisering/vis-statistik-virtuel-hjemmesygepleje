const Node = {
  "id": "04d3c153b3e35466",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1150,
  "y": 460,
  "wires": [
    [
      "6b798cfa6d8e5710"
    ]
  ],
  "_order": 214
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = msg.table
  const district_table = flow.get("district_table");
  
  msg.sql = `INSERT INTO ${table} (districtId, yearWeek, name, visits) VALUES `
  
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql += `((SELECT id FROM ${district_table} WHERE nexusDistrict='${msg.payload[i].district}'),'${msg.payload[i].yearWeek}','${msg.payload[i].name}',${msg.payload[i].visits})`;
  
      if (i < msg.payload.length - 1) msg.sql += ',';
  
  }
  msg.sql += `ON DUPLICATE KEY UPDATE visits=VALUE(visits)`
  
  return msg
}

module.exports = Node;