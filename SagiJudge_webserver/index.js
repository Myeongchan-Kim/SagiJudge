var express = require('express');
var app = express();
var bodyparser = require('body-parser').urlencoded({extended:true}); //form 평문전달

app.use(bodyparser);
app.use('/static', express.static(__dirname + '/static'));
app.use('/node_modules', express.static(__dirname + '/node_modules'));

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', __dirname + '/views');
app.set('port', process.env.PORT || 3000);

app.get('/', function(req, res){
  res.render('index', {userName : "123"});
});

var showPage =  require('./routes/show');
app.use('/show', showPage);

var addPage = require('./routes/add');
app.use('/add', addPage);

var deletePage = require('./routes/delete');
app.use('/delete', deletePage);

app.use(function (req, res){
  res.type('text/plain');
  res.status('404');
  res.send('404 - Page not found');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('text/plain');
  res.status('500');
  res.send('500 - Server Error');
});

app.listen(app.get('port'), function (){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
