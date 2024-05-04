const express = require('express');
const router = express.Router();
const controller = require('./controller');

router.post('/auth/submit', controller.loginSubmit);

router.get('/logout', controller.logout);

router.get('/auth/check', controller.loginCheck);

router.get('/getData', controller.getData);

router.post('/executeModel', controller.executeModel);

module.exports = router;
