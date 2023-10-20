const dbService = require('../services/db.service');
const consts = require('../utils/constants.util');
const moment = require('moment')

async function getActiveByWeek(week) {
  let sql = `SELECT
    (SELECT CAST(SUM(on_loan) AS INTEGER) FROM ${consts.ALLOWED_FILES_TABLES[2]} WHERE week = "${week}") AS nexus_active,
    (SELECT CAST(SUM(on_loan) + SUM(available) AS INTEGER) FROM ${consts.ALLOWED_FILES_TABLES[2]} WHERE week = "${week}") AS nexus_total,
    (SELECT COUNT(DISTINCT (name)) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = TRUE AND call_to = "citizen") AS vitacomm_active,
    (SELECT COUNT(DISTINCT (name)) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE call_to = "citizen") AS vitacomm_total`;
  
  const active_week = await dbService.query(sql);
  return { active_week };
}

async function getConversionData(week) {
  let sql_vitacomm = `
    SELECT
      unit,
      COUNT(DISTINCT (name)) AS active
    FROM 
      ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = TRUE AND call_to = "citizen"
    GROUP BY
      unit
    `
  const vitacomm_tablets = await dbService.query(sql_vitacomm);

  let sql_nexus = `
    SELECT
      unit,
      on_loan,
	    available
    FROM 
      ${consts.ALLOWED_FILES_TABLES[2]} WHERE week = "${week}"
    GROUP BY
      unit
    `
  const nexus_tablets = await dbService.query(sql_nexus);

  sql_citizens = `
    SELECT
      unit,
      citizens
    FROM 
      ${consts.ALLOWED_FILES_TABLES[3]} WHERE week = "${week}"
    GROUP BY
      unit
    `
  const citizens = await dbService.query(sql_citizens);
  return { vitacomm_tablets, nexus_tablets, citizens };
}

async function getActiveNow() {
  const date = moment().subtract(7,'d').format('YYYY-MM-DD HH:mm');
  let sql = `SELECT 
    (SELECT COUNT(*) FROM ${consts.ALLOWED_FILES_TABLES[1]} WHERE last_seen > "${date}") AS knox_active,
    (SELECT COUNT(*) FROM ${consts.ALLOWED_FILES_TABLES[1]}) AS knox_total,
    (SELECT COUNT(DISTINCT (name)) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE time > "${date}" AND answered = TRUE AND call_to = "citizen") AS vitacomm_active,
    (SELECT COUNT(DISTINCT (name)) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE call_to = "citizen") AS vitacomm_total`;
  
  const active_now = await dbService.query(sql);
  return { active_now };
}

module.exports = {
  getActiveByWeek,
  getActiveNow,
  getConversionData
};