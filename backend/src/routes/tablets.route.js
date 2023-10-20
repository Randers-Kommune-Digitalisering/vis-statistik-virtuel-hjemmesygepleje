const express = require('express');
const router = express.Router();
const tabletsController = require('../controllers/tablets.controller');

router.get('/active', async function(req, res, next) {
    try {
        if(req.query.week) {
            res.json( await tabletsController.getActiveWeek(req.query.week));
        } else res.json( await tabletsController.getActiveNow());
    } catch (err) {
        console.error(`Error getting tablets`, err.message);
        next(err);
    }
});


router.get('/conversion', async function(req, res, next) {
    try {
        res.json( await tabletsController.getConversionData(req.query.week));
    } catch (err) {
        console.error(`Error getting tablets`, err.message);
        next(err);
    }
});

  

module.exports = router;