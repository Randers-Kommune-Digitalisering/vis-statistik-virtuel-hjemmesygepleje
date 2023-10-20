const express = require('express');
const router = express.Router();
const multer  = require('multer');
const storage= multer.memoryStorage();
const upload = multer({storage: storage});
const fileUploadController = require('../controllers/fileUpload.controller');
const consts = require('../utils/constants.util');

router.post('/', upload.single('file'), async function(req, res, next) {

    try {
        const file = req.file;
        const file_type = req.body.filetype;
        const datetime = req.body.datetime;
        const week = req.body.week;

        // Check if file type in request and an allowed type
        if(!consts.ALLOWED_FILES_TABLES.includes(file_type)) {
            throw Error('Invalid file type');
        }
        
        // Get the extension of the uploaded file
        const file_extension = file.originalname.slice(
            ((file.originalname.lastIndexOf('.') - 1) >>> 0) + 2
        );
    
        // Check if the uploaded file is allowed
        if (!consts.ALLOWED_FILE_EXT.includes(file_extension) || !consts.ALLOWED_MIME_TYPES.includes(file.mimetype)) {
            throw Error('Invalid file');
        }
    
        if ((file.size / (1024 * 1024)) > consts.MAX_FILE_SIZE) {                  
           throw Error('File too large');
        }
        res.json( await fileUploadController.uploadFile(file, file_type, datetime, week));
    } catch (err) {
        console.error(`Error uploading file`, err.message);
        next(err);
    }

});
  

module.exports = router;