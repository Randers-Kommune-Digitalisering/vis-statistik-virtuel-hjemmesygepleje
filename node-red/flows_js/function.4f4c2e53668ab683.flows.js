const Node = {
  "id": "4f4c2e53668ab683",
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
  "y": 420,
  "wires": [
    [
      "6b798cfa6d8e5710"
    ]
  ],
  "_order": 205
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const table = flow.get("nexus_table");
  const district_table = flow.get("district_table");
  let keys = Object.keys(msg.payload[0]).sort()
  msg.sql = `INSERT INTO ${table} (`
  keys.forEach((key, index) => {
      if(key === 'district') msg.sql += "districtId"
      else msg.sql += key 
      if(index < keys.length -1) msg.sql += ","
      else msg.sql += ")"
  })
  msg.sql += "VALUES "
  //msg.sql = `INSERT INTO ${table} (districtId,citizens,citizenPlannedScreen,citizensDeliveredScreen,screensAvailable,screensOnloan,weekYear,timePlanned,timeDelivered,timePlannedScreen,timeDeliveredScreen)VALUES `
  
  for (let i = 0; i < msg.payload.length; i++) {
      /*
      //msg.sql += `((SELECT id FROM ${district_table} WHERE nexusDistrict='${msg.payload[i].district}'),${msg.payload[i].citizens}, ${msg.payload[i].citizenPlannedScreen},${msg.payload[i].citizensDeliveredScreen},${msg.payload[i].screensAvailable},${msg.payload[i].screensOnloan},${msg.payload[i].weekYear},${msg.payload[i].timePlanned})`;
      msg.sql = '';
  
      for (const [key, value] of Object.entries(msg.payload[i])) {
          msg.st.push(key)
      }
      */
      msg.sql += "("
      keys.forEach((key, index) => {
          if (key === 'district') msg.sql += `(SELECT id FROM ${district_table} WHERE nexusDistrict='${msg.payload[i][key]}')`
          else msg.sql += `'${msg.payload[i][key]}'`
          if (index < keys.length - 1) msg.sql += ","
          else msg.sql += ")"
      })
  
      if (i < msg.payload.length - 1) msg.sql += ',';
  
  }
  //msg.sql += `ON DUPLICATE KEY UPDATE status=VALUE(status), lastSeen=VALUE(lastSeen), updated=VALUE(updated)`
  
  msg.sql += "ON DUPLICATE KEY UPDATE "
  keys.forEach((key, index) => {
      if (!(key === 'district' || key === 'yearWeek'))
          msg.sql += `${key}=VALUE(${key}),`
      if (index === keys.length - 1) msg.sql = msg.sql.slice(0,-1)
  })
  
  return msg
}

module.exports = Node;