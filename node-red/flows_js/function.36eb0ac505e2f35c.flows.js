const Node = {
  "id": "36eb0ac505e2f35c",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "g": "b277ca7841462180",
  "name": "set user/pass",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 270,
  "y": 60,
  "wires": [
    [
      "1bcc5ea5062f24ba"
    ]
  ],
  "_order": 162
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  
  let user = env.get("KNOX_CLIENT");
  let pass = env.get("KNOX_SECRET");
  msg.auth = user + ":" + pass;
  return msg;
  
}

module.exports = Node;