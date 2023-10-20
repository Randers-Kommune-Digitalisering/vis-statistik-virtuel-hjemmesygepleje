const dbService = require('../services/db.service');
const utils = require('../utils/utils.util');

async function uploadFile(file, file_type, datetime, week) {
    let sql = await utils.fileToSQL(file, file_type, datetime, week);
    let result = await dbService.query(sql);

    let message = "Kunne ikke tilføje filen til databasen!";

    if (result.affectedRows) {
      message = "Filen blev succesfuldt tilføjet til databasen";
    }
  
    return { message };
}

module.exports = {
    uploadFile
};