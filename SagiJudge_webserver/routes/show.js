var express = require('express');
var router = express.Router();
var util = require('util');
var url = require('url');

var cheerio = require('cheerio');
var request = require('request');

var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host : '127.0.0.1',
  database : 'lacidem',
  user : 'lacidem',
  password : 'lacidem',
});

router.route('/').get(function (req, res){
  res.render('test', {data:'default show'});
});

router.route('/get_id/:url').get(function(req, res){
  request(req.params.url, function(error, response, html){
  	if (error) {throw error};

  	// console.log (html);

  	var $ = cheerio.load(html);
  	var result = "";
  	$('#entry div.article p').each(function(){
  		//console.log($(this).text());
  		result += $(this).text() + "\r\n";
  	});

    var urlAddr = url.parse(req.params.url);
    var urlStirng = urlAddr.host + urlAddr.pathname;
    console.log(urlStirng);
  	var query = "CALL getIdByUrl("+ urlAddr + ", "+ JSON.stringify(result)  +")" ;
  	console.log("Query: "+ query);
  	pool.query(query, function (err, rows, fields){
  		console.log(fields);
      res.type('text/plain');
      res.send(JSON.stringify(rows));
  	});
  });
});

router.route('/get_rating/:id').get(function(req, res){
  var query = "";
  pool.query(query, function (err, rows, fields){

    // this is dummy data. // MC
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
