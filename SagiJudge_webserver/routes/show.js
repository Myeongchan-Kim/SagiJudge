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

router.route('/get_article/:page_id').get(function(req, res){
  var query = "select * from pages where _id = "+ req.params.page_id+";";
  pool.query(query, function (err, rows, fields){
    if(err){
      console.log(err);
      res.type('text/json');
      res.send("id_err");
    }
    //console.log(JSON.stringify(rows));
    res.type('text/json');
    res.send(JSON.stringify(rows[0]));
  });
});

router.route('/get_id').post(function(req, res){
  request(req.body.url, function(error, response, html){
  	if (error) {
      console.log(error);
      res.type('text/json');
      res.send("Wrong URI");
    };

  	// console.log (html);

    var $ = cheerio.load(html);
  	var contents = "";
    $('div p').each(function(){
  			//console.log($(this).text());
  		contents += $(this).text() + "\r\n";
  	});
    contents = contents.replace(/\\/g, "\\\\")
     .replace(/\$/g, "\\$")
     .replace(/'/g, "\\'")
     .replace(/"/g, "\\\"");

    var title = "";

    $('title').each(function(){
      console.log($(this).text());
      title += $(this).text();
  	});
    title = title.replace(/\\/g, "\\\\")
     .replace(/\$/g, "\\$")
     .replace(/'/g, "\\'")
     .replace(/"/g, "\\\"");

    var URLobj = url.parse(req.body.url);
    var url_str = URLobj.host + URLobj.path;
    console.log(encodeURIComponent(url_str) );
    var query = "CALL getIdByUrl( '"+ encodeURIComponent(url_str) + "', '" + title + "', '"+ contents  +"' )" ;
    console.log("Query: "+ query);
  	pool.query(query, function (err, rows, fields){
      if(err) throw err;
  		res.type('text/json');
      res.send(JSON.stringify(rows[0][0]));
  	});
  });
});


router.route('/get_rating/:id').get(function(req, res){
  var query = "CALL getRateOfPageById("+req.params.id+");";
  pool.query(query, function (err, rows, fields){
    if(err) throw err;

    // this is dummy data. // MC
    console.log(JSON.stringify(rows[0]));
    var ai_score = {};
    var public_user_score = {}
    for(id in rows[0])
    {
      if(rows[0][id].opt == 0)
        ai_score = rows[0][id];
      else if(rows[0][id].opt == 1)
        public_user_score = rows[0][id];
      else if(rows[0][id].opt == 2)
        expret_score = rows[0][id];
    }
    var result = {
      expert : expret_score,
      public_user : public_user_score,
      ai : ai_score,
    }
    res.type('text/json');
    res.send(result);
  });
});

router.route('/get_rating_com/:id').get(function(req, res){
  var query = "CALL getComputerRate("+req.params.id+");";
  console.log(query);
  pool.query(query, function (err, rows, fields){
    if(err) throw err;
    // this is dummy data. // MC
    console.log(JSON.stringify(rows[0]));
    var result = JSON.stringify(rows[0]);
    res.type('text/json');
    res.send(result);
  });
});

router.route('/get_comments/user/:page_id').get(function(req, res){
  // var result = [
  //   {
  //     id: "mc1004",
  //     comment: "개사기 꺼져.",
  //     rating: 0,
  //   },
  //   {
  //     id: "tawoo",
  //     comment: "정말 좋아요~!! ^^.",
  //     rating: 1,
  //   },
  //   {
  //     id: "hahahah1925",
  //     comment: "아무래도 구라 같은데...",
  //     rating: 0,
  //   },
  //   {
  //     id: "Minytong",
  //     comment: "아무래도 구라구라왕구라",
  //     rating: 0,
  //   },
  //   {
  //     id: "asdf11111",
  //     comment: "좋은 정보 감사합니다~!!",
  //     rating: 1,
  //   },
  // ];

  var query =
  "SELECT u._id, u.email, p.content, timestamp FROM	(SELECT * FROM rates WHERE page_id = " + req.params.page_id+" ORDER BY timestamp desc) as p LEFT JOIN users as u on p.user_id = u._id WHERE u.opt = 1 OERDER BY timestamp DESC LIMIT 5;";
  pool.query(query, function (err, rows, fields){
    if(err) {
      console.log(err);
      res.type('text/json');
      res.send(JSON.stringify("error"));
    };
    var result = rows;
    console.log(result);

    res.type('text/json');
    res.send(JSON.stringify(result));
  });
});

router.route('/get_comments/doctor/:page_id').get(function(req, res){
  // var result = [
  //   {
  //     id: 'Dr.MC',
  //     comment: '사긴거같네요',
  //     rating: 0,
  //   },
  //   {
  //     id: 'Dr.TW',
  //     comment: '애매합니다.......',
  //     rating: 1,
  //   },
  //   {
  //     id: 'Dr.JW',
  //     comment: '바보같네요',
  //     rating: 0,
  //   },
  //   {
  //     id: 'Dr.MY',
  //     comment: 'FUCK!',
  //     rating: 0,
  //   },
  //   {
  //     id: 'Dr.SM',
  //     comment: '매우 의심스럽습니다.',
  //     rating: 0,
  //   },
  // ]

    var query =
     "SELECT u._id, u.email, p.content, timestamp FROM	(SELECT * FROM rates WHERE page_id = " + req.params.page_id+" and content is not null ORDER BY timestamp desc) as p LEFT JOIN users as u on p.user_id = u._id WHERE u.opt = 2 LIMIT 5;";

    pool.query(query, function (err, rows, fields){
      if(err) {
        console.log(err);
        res.type('text/json');
        res.send(JSON.stringify("error"));
      };
      var result = rows;
      console.log(result);
      for(key in result){
        if(key == 1)
          result[key]['sub_special'] = "가정의학과";
        else if (key == 2)
          result[key]['sub_special'] = "재활의학과";
        else
          result[key]['sub_special'] = "내과";

        result[key]['grade'] = 3;
      }

      res.type('text/json');
      res.send(JSON.stringify(result));
    });
});

router.route('/hot/:user_id').get(function(req, res){
  // var result = [
  //   { id : 2,
  //     title : 'title2',
  //     url : 'www.url.com2',
  //     content :'contentntnentntn2',
  //     user_rate :{
  //       good: 100,
  //       bad: 50,
  //     },
  //     doctor_rate :{
  //       good: 10,
  //       bad: 21,
  //     },
  //   },
  //   {
  //     id : 6,
  //     title : 'title6',
  //     url : 'www.url.com6',
  //     content :'contentntnentntn6',
  //     user_rate :{
  //       good: 20,
  //       bad: 10,
  //     },
  //     doctor_rate :{
  //       good: 10,
  //       bad: 11,
  //     },
  //   },
  //   {
  //     id : 7,
  //     title : 'title7',
  //     url : 'www.url.com77',
  //     content :'contentntn7cv.zkjhcv.xcentntn2',
  //     user_rate :{
  //       good: 77,
  //       bad: 23,
  //     },
  //     doctor_rate :{
  //       good: 7,
  //       bad: 27,
  //     },
  //   },
  //   {
  //     id : 8,
  //     title : 'title8',
  //     url : 'www.url.com8',
  //     content :'contentntnent888888888ntn2',
  //     user_rate :{
  //       good: 88,
  //       bad: 8,
  //     },
  //     doctor_rate :{
  //       good: 81,
  //       bad: 801,
  //     },
  //   },
  // ];
  var query = "CALL getHotPages();";
  pool.query(query, function (err, rows, fields){
    if(err){
      console.log(err);
      res.type('text/json');
      res.send("id_err");
    }
    console.log(JSON.stringify(rows));
    res.type('text/json');
    res.send(JSON.stringify(rows[0]));
  });
});

router.route('/wait/:user_id').get(function(req, res){
  var result = [
    { id : 12,
      title : '가나다2',
      url : 'www.url.com2',
      content :'contentntnentntn2',
      user_rate :{
        good: 100,
        bad: 50,
      },
      doctor_rate :{
        good: 10,
        bad: 21,
      },
    },
    {
      id : 16,
      title : 'titㅁㄴㅇㄻㄴㅇㄹe6',
      url : 'wwwasdfasdfl.com6',
      content :'contenasdgahdfharhatntnentntn6',
      user_rate :{
        good: 20,
        bad: 10,
      },
      doctor_rate :{
        good: 10,
        bad: 11,
      },
    },
    {
      id : 17,
      title : 'Lacide7',
      url : 'www.laem.com/77',
      content :'contentnfasdfatn7cav.zfakjhcv.xcentntn2',
      user_rate :{
        good: 77,
        bad: 23,
      },
      doctor_rate :{
        good: 7,
        bad: 27,
      },
    },
    {
      id : 18,
      title : 'lacicicici88',
      url : 'www.url.com8',
      content :'contentntnent888888888ntn2',
      user_rate :{
        good: 88,
        bad: 8,
      },
      doctor_rate :{
        good: 81,
        bad: 801,
      },
    },
  ];

  var query = "CALL getWatingPages();";
  pool.query(query, function (err, rows, fields){
    if(err){
      console.log(err);
      res.type('text/json');
      res.send("wait_err");
    }
    console.log(JSON.stringify(rows));
    res.type('text/json');
    res.send(JSON.stringify(rows[0]));
  });
});

router.route('/wrong/:user_id').get(function(req, res){

  var result = [
    { id : 22,
      title : 'title2',
      url : 'www.url.com2',
      content :'contentntnentntn2',
      user_rate :{
        good: 100,
        bad: 50,
      },
      doctor_rate :{
        good: 10,
        bad: 21,
      },
    },
    {
      id : 26,
      title : 'title6',
      url : 'www.url.com6',
      content :'contentntnentntn6',
      user_rate :{
        good: 20,
        bad: 10,
      },
      doctor_rate :{
        good: 10,
        bad: 11,
      },
    },
    {
      id : 27,
      title : 'title7',
      url : 'www.url.com77',
      content :'contentntn7cv.zkjhcv.xcentntn2',
      user_rate :{
        good: 77,
        bad: 23,
      },
      doctor_rate :{
        good: 7,
        bad: 27,
      },
    },
    {
      id : 28,
      title : 'title8',
      url : 'www.url.com8',
      content :'contentntnent888888888ntn2',
      user_rate :{
        good: 88,
        bad: 8,
      },
      doctor_rate :{
        good: 81,
        bad: 801,
      },
    },
  ];

  var query = "CALL  getDangerousPages()";
  pool.query(query, function (err, rows, fields){
    if(err){
      console.log(err);
      res.type('text/json');
      res.send("get Wrong err");
      return;
    }
    console.log(JSON.stringify(rows));
    res.type('text/json');
    res.send(JSON.stringify(rows[0]));
  });
});

module.exports = router;
