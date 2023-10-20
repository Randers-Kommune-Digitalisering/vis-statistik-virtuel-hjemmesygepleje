const mysql = require('mysql2/promise');
const dbConfig = require('../configs/db.config');
const consts = require('../utils/constants.util'); //consts.ALLOWED_FILES_TABLES  is ['video_calls', 'tablets_knox', 'tablets_nexus', 'citizens']

// Establish connection to database
const connection = mysql.createPool(dbConfig);

async function setupDatabase() {
  for(const table of consts.ALLOWED_FILES_TABLES) {
    let sql  = '';
    switch(table) {
      case consts.ALLOWED_FILES_TABLES[0]: 
        sql = `CREATE TABLE IF NOT EXISTS ${table} (
          id CHAR(36) NOT NULL,
          unit TINYTEXT,
          answered TINYINT(1),
          time TIMESTAMP,
          week TINYTEXT,
          duration TIME,
          call_from ENUM('citizen', 'employee'),
          call_to ENUM('citizen', 'employee'),
          name TINYTEXT,
          PRIMARY KEY (id)
        );`
        break;
      case consts.ALLOWED_FILES_TABLES[1]: 
        sql = `CREATE TABLE IF NOT EXISTS ${table} (
          id CHAR(15) NOT NULL,
          last_seen TIMESTAMP,
          last_location_latitude DECIMAL(8,6),
          last_location_longitude DECIMAL(9,6),
          last_location_time TIMESTAMP,
          PRIMARY KEY (id)
        );`
        break;
      case consts.ALLOWED_FILES_TABLES[2]:
        sql = `CREATE TABLE IF NOT EXISTS ${table} (
          id MEDIUMINT NOT NULL AUTO_INCREMENT,
          unit TINYTEXT,
          on_loan SMALLINT UNSIGNED,
          available SMALLINT UNSIGNED,
          week TINYTEXT,
          UNIQUE KEY week_unit (week, unit),
          PRIMARY KEY (id)
        );`
        break;
      case consts.ALLOWED_FILES_TABLES[3]: 
        sql = `CREATE TABLE IF NOT EXISTS ${table} (
          id MEDIUMINT NOT NULL AUTO_INCREMENT,
          unit TINYTEXT,
          citizens SMALLINT UNSIGNED,
          week TINYTEXT,
          UNIQUE KEY week_unit (week, unit),
          PRIMARY KEY (id)
        );`
        break;
      default:
        throw new Error('Unknown database table')
    }
    await connection.query(sql)
  }
}

async function query(sql, params) {
  const [results, ] = await connection.execute(sql, params);

  return results;
}

module.exports = {
  setupDatabase,
  query,
};