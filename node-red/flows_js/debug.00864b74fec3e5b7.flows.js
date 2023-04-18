const Node = {
  "id": "00864b74fec3e5b7",
  "type": "debug",
  "z": "971a7ae6df987a48",
  "name": "stdout",
  "active": true,
  "tosidebar": true,
  "console": true,
  "tostatus": false,
  "complete": "payload.warningStatus = 0\t? { $flowContext(\"tablename\"): \"table created\" }:\tpayload.warningStatus = 1\t? { $flowContext(\"tablename\"): \"table exists\" }:\t{\"warningstatus\" : payload.warningStatus}",
  "targetType": "jsonata",
  "statusVal": "",
  "statusType": "auto",
  "x": 1400,
  "y": 100,
  "wires": [],
  "_order": 26
}

module.exports = Node;