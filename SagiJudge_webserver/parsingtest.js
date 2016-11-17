var cheerio = require('cheerio');
var request = require('request');

var url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&latlng=37.4824642,126.9943559';
request(url, function(error, response, html){
	if (error) {throw error};

  var data = JSON.parse(html);
	console.log (data.results[0].address_components[3].long_name);
	// var $ = cheerio.load(html);
  // //console.log(html);
	// var result = "";
	// $('div p').each(function(){
	// 	console.log($(this).text());
	// 	result += $(this).text() + "\r\n";
	});
//
// console.log(encodeURIComponent("http://lemontia.tistory.com/50"));
//
//
// console.log(Math.random());
