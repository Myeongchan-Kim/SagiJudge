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

router.route('/comment/').post(function (req, res){
  var page_id = req.body.page_id;
  var user_id = req.body.user_id;
  var user_comment = req.body.user_comment;
  var user_rating = req.body.user_rating;

  console.log(req.body);
  var query = "INSERT INTO rates (page_id, user_id, content, rate) values ('"
  + page_id + "', '" + user_id + "', '" + user_comment + "', '" + user_rating +"');";
  console.log(query);
  pool.query(query, function (err, rows, fields){
    if(err) throw err;
    res.type('text/json');
    res.send(JSON.stringify(rows));
  });
})

router.route('/user/').post(function (req, res){
  var user_email = req.body.user_email;
  var user_password = req.body.user_password;
  var user_type = req.body.user_type;

  console.log(req.body);
  var query = "INSERT INTO users (email, password, opt) values ('"
  + user_email + "', '" + user_password + "', '" + user_type +"');";
  console.log(query);
  pool.query(query, function (err, rows, fields){
    if(err) throw err;
    res.type('text/json');
    res.send(JSON.stringify(rows));
  });
})

module.exports = router;
