const Node = {
  "id": "8c007f8cdabe607c",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "add empty keys and yearWeek",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 950,
  "y": 420,
  "wires": [
    [
      "4f4c2e53668ab683"
    ]
  ],
  "_order": 206
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  const keys = ["citizens", "citizensPlannedScreen", "citizensDeliveredScreen", "timePlanned", "timeDelivered", "timePlannedScreen", "timeDeliveredScreen", "screensAvailable", "screensOnloan"];
  msg.payload = msg.payload.map((obj) => {
      obj.yearWeek = msg.week
      keys.forEach((k) => {
          if (!obj.hasOwnProperty(k)) obj[k] = 0;
      })
      return obj
  })
  return msg;
}

module.exports = Node;