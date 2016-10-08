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
  	if (error) {
      console.log(error);
      res.type('text/plain');
      res.send("Wrong URI");
    };

  	// console.log (html);

  	var $ = cheerio.load(html);
  	var contents = "";
  	$('#entry div.article p').each(function(){
  		//console.log($(this).text());
  		contents += $(this).text() + "\r\n";
  	});
    contents = contents.replace(/\\/g, "\\\\")
     .replace(/\$/g, "\\$")
     .replace(/'/g, "\\'")
     .replace(/"/g, "\\\"");

    var title = "";
    $('div.titleWrap h2 .subs').each(function(){
  		console.log($(this).text());
      title += $(this).text();
  	});
    title = title.replace(/\\/g, "\\\\")
     .replace(/\$/g, "\\$")
     .replace(/'/g, "\\'")
     .replace(/"/g, "\\\"");

    //console.log(req.params.url);
    console.log(encodeURIComponent(req.params.url) );
    var query = "CALL getIdByUrl( '"+ encodeURIComponent(req.params.url) + "', '" + title + "', '"+ contents  +"' )" ;
    console.log("Query: "+ query);
  	pool.query(query, function (err, rows, fields){
      if(err) throw err;
  		res.type('text/plain');
      res.send(JSON.stringify(rows[0][0]));
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
        avg : Math.random(),
      },
    }
    res.type('text/plain');
    res.send(result);
  });
});

router.route('/get_comments/user/:id').get(function(req, res){
  var result = [
    {
      id: "mc1004",
      comment: "개사기 꺼져.",
      rating: 0,
    },
    {
      id: "tawoo",
      comment: "정말 좋아요~!! ^^.",
      rating: 1,
    },
    {
      id: "hahahah1925",
      comment: "아무래도 구라 같은데...",
      rating: 0,
    },
    {
      id: "Minytong",
      comment: "아무래도 구라구라왕구라",
      rating: 0,
    },
    {
      id: "asdf11111",
      comment: "좋은 정보 감사합니다~!!",
      rating: 1,
    },
  ];
  res.type('text/plain');
  res.send(JSON.stringify(result));
});

router.route('/get_comments/doctor/:id').get(function(req, res){
  var result = [
    {
      id: 'Dr.MC',
      comment: '사긴거같네요',
      rating: 0,
    },
    {
      id: 'Dr.TW',
      comment: '진짜같네요',
      rating: 1,
    },
    {
      id: 'Dr.JW',
      comment: '바보같네요',
      rating: 0,
    },
    {
      id: 'Dr.MY',
      comment: 'FUCK!',
      rating: 0,
    },
    {
      id: 'Dr.SM',
      comment: '매우 의심스럽습니다.',
      rating: 0,
    },
  ]
  res.type('text/plain');
  res.send(JSON.stringify(result));
});

module.exports = router;
