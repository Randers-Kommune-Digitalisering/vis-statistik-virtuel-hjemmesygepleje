const Node = {
  "id": "1b9d442866c32d28",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "set dates",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 240,
  "y": 220,
  "wires": [
    [
      "37e7a50781e54f2b"
    ]
  ],
  "_order": 173
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  msg.startTime = new Date(msg.time).setDate(new Date(msg.time).getDate() - 30);
  msg.endTime = msg.time
  return msg;
}

module.exports = Node;