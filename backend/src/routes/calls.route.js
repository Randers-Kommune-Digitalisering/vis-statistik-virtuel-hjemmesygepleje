const express = require('express');
const router = express.Router();
const moment = require('moment')
const callsController = require('../controllers/calls.controller');

router.get('/citizens', async function(req, res, next) {
    try {
        if(req.query.week) {
            res.json( await callsController.getWeek(req.query.week));
        } else {
            // No week parsed - get last week as default
            let lastWeek = new Date();
            lastWeek.setDate(lastWeek.getDate() - 7);
            const yearWeek = ref(lastWeek.getFullYear() + "-W" + (moment(lastWeek).isoWeek()));
            res.json( await callsController.getWeek(yearWeek));
        }
    } catch (err) {
        console.error(`Error getting tablets`, err.message);
        next(err);
    }
});  

module.exports = router;