const Node = {
  "id": "1e46866d75e45ca5",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "merge",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 1070,
  "y": 380,
  "wires": [
    [
      "a4ed1f3c78e67080"
    ]
  ],
  "_order": 186
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  for (const [key, value] of Object.entries(msg.payload)) {
      value.map((item) => {
          if (item['Besøgs status'] === "Planlagt som skærmbesøg") {
              item['Planlagt tid (timer)(skærm)'] = parseFloat(String(item['Planlagt tid (timer)']).replace(',', ''));
              item['Antal borgere planlagt(i)(skærm)'] = parseFloat(String(item['Antal borgere (i)']).replace(',', ''));
              delete item['Planlagt tid (timer)']
              delete item['Antal borgere (i)']
              delete item['Besøgs status'];
          } else if (item['Besøgs status'] === "Leveret som skærmbesøg") {
              item['Leveret tid (timer)(skærm)'] = parseFloat(String(item['Leveret tid (timer)']).replace(',', ''));
              item['Antal borgere leveret(i)(skærm)'] = parseFloat(String(item['Antal borgere (i)']).replace(',', ''));
              delete item['Leveret tid (timer)']
              delete item['Antal borgere (i)']
              delete item['Besøgs status'];
          } else if (item['Besøgs status'] === "Planlagt") {
              item['Planlagt tid (timer)'] = parseFloat(String(item['Planlagt tid (timer)']).replace(',', ''));
              delete item['Besøgs status'];
          } else if (item['Besøgs status'] === "Udført med planlagt tid") {
              item['Leveret tid (timer)'] = parseFloat(String(item['Leveret tid (timer)']).replace(',', ''));
              delete item['Besøgs status'];
          }
      })
  }
  
  function mergeArr(arr1, arr2) {
      let merged = [];
      for (let i = 0; i < arr1.length; i++) {
          merged.push({
              ...arr1[i],
              ...(arr2.find((itmInner) => itmInner['Organisation (Niveau 09)'] === arr1[i]['Organisation (Niveau 09)']))
          }
          );
      }
      return merged;
  }
  
  let temp_arr = null;
  
  for (const [key, value] of Object.entries(msg.payload)) {
      if (!(key === "ydelser") && !(key === "ydelser-skærm")) {
          if(temp_arr) temp_arr = mergeArr(temp_arr, value)
          else temp_arr = value
      }
  }
  
  let service = msg.payload['ydelser']
  let screenservice = msg.payload['ydelser-skærm']
  
  msg.payload = {}
  msg.payload.nexus = {"nexus" : temp_arr}
  msg.payload.service = { "service": service }
  msg.payload.screenservice = { "screenservice": screenservice}
  
  return msg;
}

module.exports = Node;