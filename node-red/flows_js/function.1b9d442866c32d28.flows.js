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
  "x": 260,
  "y": 220,
  "wires": [
    [
      "5faef195141dffea"
    ]
  ],
  "_order": 173
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  msg.endDate = msg.payload;
  msg.startDate = new Date(msg.payload).setDate(new Date(msg.payload).getDate() - 7);
  return msg;
}

module.exports = Node;