const Node = {
  "id": "27d5ebd64204c3f6",
  "type": "function",
  "z": "971a7ae6df987a48",
  "name": "function 1",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1300,
  "y": 880,
  "wires": [
    [
      "fa6c704e02782af1"
    ]
  ],
  "_order": 73
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  
  var test = "first" || undefined || "test";
  
  
  msg.payload = test;
  
  
  return msg;
}

module.exports = Node;