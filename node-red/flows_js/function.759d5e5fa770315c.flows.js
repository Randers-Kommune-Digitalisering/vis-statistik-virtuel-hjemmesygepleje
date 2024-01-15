const Node = {
  "id": "759d5e5fa770315c",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "g": "3fe1323433ebf5d2",
  "name": "datetime and id",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 960,
  "y": 260,
  "wires": [
    [
      "c4381af0d3da0269"
    ]
  ],
  "_order": 190
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  // From https://weeknumber.com/how-to/javascript
  
  // Returns the ISO week of the date.
  Date.prototype.getWeek = function () {
      var date = new Date(this.getTime());
      date.setHours(0, 0, 0, 0);
      // Thursday in current week decides the year.
      date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
      // January 4 is always in week 1.
      var week1 = new Date(date.getFullYear(), 0, 4);
      // Adjust to Thursday in week 1 and count number of weeks from date to week1.
      return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
          - 3 + (week1.getDay() + 6) % 7) / 7);
  }
  
  // Returns the four-digit year corresponding to the ISO week of the date.
  Date.prototype.getWeekYear = function () {
      var date = new Date(this.getTime());
      date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
      return date.getFullYear();
  }
  
  
  // Add start and end time for unanswered calls
  let latest_time = msg.startTime;
  
  for (let i = 0; i < msg.payload.length; i++) {
      if (!msg.payload[i].startTime && !msg.payload[i].endTime) {
          let new_time = new Date(latest_time);
          new_time = new_time.setSeconds(new_time.getSeconds() + 1)
          msg.payload[i].startTime = new_time
          msg.payload[i].endTime = new_time
          latest_time = new_time
      } else latest_time =msg.payload[i].endTime
  }
  
  // Calculating year and week and reformat datetime
  msg.payload = msg.payload.map(obj => ({
      ...obj,
      yearWeek: obj.startTime ? new Date(obj.startTime).getWeekYear() + "-" + new Date(obj.startTime).getWeek() : new Date(msg.midDate).getWeekYear() + "-" + new Date(msg.midDate).getWeek(),
      startTime: obj.startTime ? new Date(obj.startTime).toISOString().slice(0, 19).replace('T', ' ') : null,
      endTime: obj.endTime ? new Date(obj.endTime).toISOString().slice(0, 19).replace('T', ' ') : null
  }))
  
  return msg;
}

module.exports = Node;