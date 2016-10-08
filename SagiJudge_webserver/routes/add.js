var express = require('express');
var router = express.Router();
var util = require('util');

var bodyparser = require('body-parser').urlencoded({extended:true}); //form 평문전달

var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host : '127.0.0.1',
  database : 'lacidem',
  user : 'lacidem',
  password : 'lacidem',
});


router.route('/').get(function (req, res){
  res.render('test', {data:"default delete"});
});

router.route('/comment/:page_id').post(function (req, res){
  var query = "";

})

module.exports = router;
