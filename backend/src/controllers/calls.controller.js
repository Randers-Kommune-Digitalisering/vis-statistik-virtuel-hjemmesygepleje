const dbService = require('../services/db.service');
const consts = require('../utils/constants.util');

async function getWeek(week) {
  const sql_total = `SELECT
  (SELECT COUNT(id) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = TRUE AND call_to = "citizen") AS answered,
  (SELECT COUNT(id) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = FALSE AND call_to = "citizen") AS unanswered,
  (SELECT IFNULL(SEC_TO_TIME(AVG(duration)), 0) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = TRUE AND call_to = "citizen") AS avg_duration,
  (SELECT IFNULL(SEC_TO_TIME(SUM(duration)), 0) FROM ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND answered = TRUE AND call_to = "citizen") AS sum_duration
  `;
  const calls_total = await dbService.query(sql_total);

  const sql_unit_answered = `
    SELECT
      unit,
      COUNT(CASE WHEN answered THEN 1 END) AS answered,
      COUNT(CASE WHEN NOT answered THEN 1 END) AS unanswered
    FROM 
      ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND call_to = "citizen"
    GROUP BY
      unit
    `;
  const calls_unit_answered = await dbService.query(sql_unit_answered);


  const sql_unit_duration = `
    SELECT
      unit,
      SEC_TO_TIME(AVG(duration)) AS avg,
      SEC_TO_TIME(SUM(duration)) AS sum
    FROM 
      ${consts.ALLOWED_FILES_TABLES[0]} WHERE week = "${week}" AND call_to = "citizen" AND answered = TRUE
    GROUP BY
      unit
    `;
  const calls_unit_duration = await dbService.query(sql_unit_duration);

  return { calls_total, calls_unit_answered, calls_unit_duration };
}

module.exports = {
 getWeek
};