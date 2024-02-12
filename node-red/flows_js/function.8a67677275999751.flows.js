const Node = {
  "id": "8a67677275999751",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 690,
  "y": 840,
  "wires": [
    [
      "6b798cfa6d8e5710"
    ]
  ],
  "_order": 203
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = flow.get("district_table");
  msg.sql = `INSERT INTO ${table} (vitacommDistrict, nexusDistrict)VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      msg.sql += `('${msg.payload[i].vitacommDistrict}','${msg.payload[i].nexusDistrict}')`;
      if (i < msg.payload.length - 1) msg.sql += ',';
  
  }
  return msg
}

module.exports = Node;