const Node = {
  "id": "c4381af0d3da0269",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1110,
  "y": 260,
  "wires": [
    [
      "6b798cfa6d8e5710"
    ]
  ],
  "_order": 202
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = flow.get("call_table");
  const district_table = flow.get("district_table");
  msg.sql = `INSERT IGNORE INTO ${table} (calleeDistrictId, callerDistrictId, calleeCpr, calleeName, callerRole, calleeRole, startTime, duration, endReason, yearWeek, endTime)VALUES `
  for (let i = 0; i < msg.payload.length; i++) {
      let start_time = `'${msg.payload[i].startTime}'` //msg.payload[i].startTime ? `'${msg.payload[i].startTime }'` : 'NULL'
      let end_time = `'${msg.payload[i].endTime}'` //msg.payload[i].endTime ? `'${msg.payload[i].endTime}'` : 'NULL'
      msg.sql += `((SELECT id FROM ${district_table} WHERE vitacommDistrict='${msg.payload[i].calleeDistrict}'),(SELECT id FROM ${district_table} WHERE vitacommDistrict='${msg.payload[i].callerDistrict}'),'${msg.payload[i].calleeCpr}','${msg.payload[i].calleeName}','${msg.payload[i].callerRole}','${msg.payload[i].calleeRole}',${start_time},'${msg.payload[i].duration}','${msg.payload[i].endReason}','${msg.payload[i].yearWeek}',${end_time})`;
      if (i < msg.payload.length - 1) msg.sql += ',';
  }
  return msg
}

module.exports = Node;