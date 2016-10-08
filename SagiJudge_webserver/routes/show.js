var express = require('express');
var router = express.Router();
var util = require('util');

var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host : '127.0.0.1',
  database : 'laos',
  user : 'guest',
  password : '1234'
});

router.route('/').get(function (req, res){
  res.render('test', {data:'default show'});
});

router.route('/get_url/:url').get(function(req, res){
  var query = "";
  pool.query(query, function (err, rows, fields){
    console.log(JSON.stringify(rows));
    res.type('text/plain');
    res.send("13221");
  });
});

router.route('/get_rating/:id').get(function(req, res){
  var query = "";
  pool.query(query, function (err, rows, fields){
    console.log(JSON.stringify(rows));
    var result = {
      expert :{
        good : 123,
        bad : 55,
        avg : 123 / (123 + 55),
      },
      public_user :{
        good : 7244,
        bad : 1284,
        avg : 7244 / (7244 + 1284),
      },
      ai : {
        avg : 0.65,
      },
    }
    res.type('text/plain');
    res.send(result);
  });
});

module.exports = router;
