const Node = {
  "id": "ed08a48b37684d4c",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "read xlsx",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [
    {
      "var": "xlsx",
      "module": "xlsx"
    }
  ],
  "x": 420,
  "y": 380,
  "wires": [
    [
      "47d92a71febd45a0"
    ]
  ],
  "_order": 181
}

Node.func = async function (node, msg, RED, context, flow, global, env, util, xlsx) {
  function process_RS(buffer) {
      var workbook = xlsx.read(buffer, { type: "buffer" });
      msg.payload = readExcelData(workbook); //cb(workbook);
  }
  
  function readExcelData(workbook) {
      let header = null;
      let uniform_sheets = [];
  
      for (const sheet of workbook.SheetNames) {
          let csv = xlsx.utils.sheet_to_csv(workbook.Sheets[sheet], { FS: ";", blankrows: false });
          if (sheet === "ugenr") msg.week = csv.split('\n')[1];
          else if (sheet === "skærme") uniform_sheets.push({name: sheet, data: "Organisation (Niveau 09)" + csv })
          else if (sheet === "ydelser") uniform_sheets.push({ name: sheet, data: "Organisation (Niveau 09)" + csv })
          else if (sheet === "ydelser-skærm") uniform_sheets.push({ name: sheet, data: "Organisation (Niveau 09)" + csv })
          else uniform_sheets.push({ name: sheet, data: csv })
      }
  
      return uniform_sheets;
  }
  
  process_RS(msg.payload)
  
  return msg;
}

module.exports = Node;