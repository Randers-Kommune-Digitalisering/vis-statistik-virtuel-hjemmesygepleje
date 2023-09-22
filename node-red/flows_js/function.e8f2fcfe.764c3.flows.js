const Node = {
  "id": "e8f2fcfe.764c3",
  "type": "function",
  "z": "39989dadda5c9a15",
  "name": "Check if color is light or dark",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "x": 1400,
  "y": 780,
  "wires": [
    [
      "d987f969.79c86"
    ]
  ],
  "_order": 104
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  var tinycolor = global.get('tinycolor')
  
  var color1 = tinycolor(msg.payload);
  var t1 = color1.isDark(); // false
  msg.payload = ("Is "+ color1 + " dark? "+ t1);
  return msg;
  
}

module.exports = Node;