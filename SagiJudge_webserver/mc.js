// filename : scraping.js
// author : saltfactory@gmail.com

var cheerio = require('cheerio');
var request = require('request');

var url = 'http://damoadamoa.tistory.com/121';
request(url, function(error, response, html){
	if (error) {throw error};

	// console.log (html);

	var $ = cheerio.load(html);

	$('div.article p').each(function(){
		console.log("설명" + $(this).text());
	})

});
