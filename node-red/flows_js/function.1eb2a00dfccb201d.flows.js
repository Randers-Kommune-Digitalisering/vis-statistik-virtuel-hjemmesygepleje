const Node = {
  "id": "1eb2a00dfccb201d",
  "type": "function",
  "z": "39989dadda5c9a15",
  "name": "byg SQL",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 840,
  "y": 500,
  "wires": [
    [
      "3bb28f11aade4b81"
    ]
  ],
  "_order": 148
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  
    
      
      const table = flow.get("tablet_nexus_table");
      msg.sql = `INSERT IGNORE INTO ${table}(enhed, udlaante, ledige, uge) VALUES `
      for (let i = 0; i < msg.payload.length; i++) {
        msg.sql += `('${msg.payload[i].enhed}','${msg.payload[i].udlaante}', '${msg.payload[i].ledige}', '${msg.payload[i].uge}')`;
        if (i < msg.payload.length - 1) msg.sql += ',';
      
      }
      return msg
      
    
  
}

module.exports = Node;