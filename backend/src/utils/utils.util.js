const jsonata = require('jsonata');
const moment = require('moment');
const consts = require('../utils/constants.util'); //consts.ALLOWED_FILES_TABLES = ['video_calls', 'tablets_knox', 'tablets_nexus', 'citizens']

async function restructureData(data, file_type, datetime, week) {
  let expr = jsonata('$.{}');
  
  switch(file_type) {
      case consts.ALLOWED_FILES_TABLES[0]:
        // add week for Call/Vitacomm data
        data = data.map(item => ({...item, week: moment(item.Starttidspunkt, 'DD-MM-yyy hh:mm').year() + "-W" + moment(data[0].Starttidspunkt, 'DD-MM-yyy hh:mm').isoWeek()}));
        expr = jsonata('$.{ \
          "id": $."CallId", \
          "unit": $."Organisatorisk_enhed", \
          "answered": $contains($."Slutresultat", "Opkald besvaret"), \
          "time":$fromMillis($toMillis($."Starttidspunkt", "[D01]-[M01]-[Y0001] [H#1]:[m01]")), \
          "week": $."week", \
          "duration": $."Varighed", \
          "call_from": $contains($."Opkald_fra", "Medarbejder") ? "employee" : "citizen", \
          "call_to": $contains($."Opkald_til", "Medarbejder") ? "employee" : "citizen", \
          "name": $trim($substringBefore($."Opkald_til", "(")) \
          }');
        break;
      case consts.ALLOWED_FILES_TABLES[1]:
        if(!datetime) throw Error("No datetime for Knox data")
        expr = jsonata(`$.{
        "id": $."IMEI___MEID",
        "last_seen": $fromMillis($toMillis($pad("${datetime}", 19, ":00")) - (function($num, $unit){$unit = "m" ? $num * 60 * 1000 : $unit = "h" ?  $num * 60 * 60 * 1000 : $unit = "d" ? $num * 24 * 60 * 60 * 1000 : 365 * 24 * 60 * 60 * 1000}($number($substring($."Last_Seen", 0, $length($."Last_Seen")-1)), $substring($."Last_Seen", $length($."Last_Seen")-1, 1)))),
        "last_location_latitude": $."Last_Location" ? $number($split($trim($substringBefore($."Last_Location", "(")),",")[0]) : null,
        "last_location_longitude": $."Last_Location" ? $number($trim($split($trim($substringBefore($."Last_Location", "(")),",")[1])) : null,
        "last_location_time": $."Last_Location" ? $split($substring($substringAfter($."Last_Location", "("), 0, 23), " ")[0] & "T" & $split($substring($substringAfter($."Last_Location", "("), 0, 23), " ")[1] &".000Z" : null
        }`);
        break;
      case consts.ALLOWED_FILES_TABLES[2]:
        if(!week) throw Error("No week for Nexus data")
        expr = jsonata(`$.{
          "unit": $."Organisation_(Niveau_09)",
          "on_loan": $."Udlånt_skærm" = '' ? 0 :  $."Udlånt_skærm",
          "available": $."Ledig_skærm" = '' ? 0 : $."Ledig_skærm",
          "week": "${week}"
          }`);
          break;
      case consts.ALLOWED_FILES_TABLES[3]:
        if(!week) throw Error("No week for Nexus data")
        expr = jsonata(`$.{
          "unit": $."Organisation_(Niveau_09)",
          "citizens": $."Antal_borgere_(i)",
          "week": "${week}"
          }`);
          break;
      default:
        throw Error('Unknown file type - not in allowed files');
  }
  const result = await expr.evaluate(data);
  return result;
}

function generateSQL(data, table) {
  let sql = ""
  switch(table) {
    case consts.ALLOWED_FILES_TABLES[0]:
      sql = `INSERT IGNORE INTO ${table} VALUES `
      for (let i = 0; i < data.length; i++) {
        sql += `('${data[i].id}','${data[i].unit}',${data[i].answered},'${data[i].time}','${data[i].week}','${data[i].duration}','${data[i].call_from}','${data[i].call_to}','${data[i].name}')`;
        if(i<data.length-1) sql += ',';
      };
      break;
    case consts.ALLOWED_FILES_TABLES[1]:
      sql = `INSERT IGNORE INTO ${table} VALUES `
      for (let i = 0; i < data.length; i++) {
        sql += `('${data[i].id}','${data[i].last_seen}',${data[i].last_location_latitude},${data[i].last_location_longitude},'${data[i].last_location_time}')`;
        if (i < data.length - 1) sql += ',';
      };
      break;
    case consts.ALLOWED_FILES_TABLES[2]:
      sql = `INSERT INTO ${table}(unit, on_loan, available, week) VALUES `
      for (let i = 0; i < data.length; i++) {
        sql += `('${data[i].unit}','${data[i].on_loan}','${data[i].available}','${data[i].week}')`;
        if (i < data.length - 1) sql += ',';
      };
      break;
    case consts.ALLOWED_FILES_TABLES[3]:
      sql = `INSERT INTO ${table}(unit, citizens, week) VALUES `
      for (let i = 0; i < data.length; i++) {
        sql += `('${data[i].unit}','${data[i].citizens}','${data[i].week}')`;
        if (i < data.length - 1) sql += ',';
      };
      break;
    default:
      throw Error('Unknown database table - not in allowed tables');
  };
  return sql;
}

function csvToObjs(file){

  const separator = ';';
  let csv = file.buffer.toString();

  var lines=csv.split("\n");
  lines = lines.map(l => l.trim());
  var result = [];

  var headers = lines[0].split(separator);
  headers = headers.map(e => e.split(' ').join('_').replace('/', '_').replace('&', '_'));

  for(var i=1;i<lines.length-1;i++){
    var obj = {};
    var currentline=lines[i].split(separator);

    for(var j=0;j<headers.length;j++){
      obj[headers[j]] = currentline[j];
    }
    result.push(obj);
  }

  return result;
}

function fileToSQL(file, file_type, datetime, week) {
    let data = csvToObjs(file);
    return restructureData(data, file_type, datetime, week).then((data) => { return generateSQL(data, file_type) });
}

module.exports = {
    fileToSQL
}