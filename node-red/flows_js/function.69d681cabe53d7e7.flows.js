const Node = {
  "id": "69d681cabe53d7e7",
  "type": "function",
  "z": "39989dadda5c9a15",
  "g": "11c06edd8b070ea6",
  "name": "sæt uge",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 700,
  "y": 420,
  "wires": [
    [
      "acc2ace281fe9c86"
    ]
  ],
  "_order": 158
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  
    
      msg.payload = msg.payload.map(item => {
          const updatedItems = { ...item };
          updatedItems["uge"] = moment(item["tidspunkt"]).year() + "-W" + moment(item["tidspunkt"]).isoWeek();
          return updatedItems;
      });
      
      return msg;
    
  
}

module.exports = Node;