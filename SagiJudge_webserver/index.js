var express = require('express');
var app = express();
var bodyparser = require('body-parser').urlencoded({extended:true}); //form 평문전달


// Add headers
app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With, content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

app.use(bodyparser);
app.use('/static', express.static(__dirname + '/static'));
app.use('/node_modules', express.static(__dirname + '/node_modules'));

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', __dirname + '/views');
app.set('port', process.env.PORT || 3001);


app.get('/', function(req, res){
  res.redirect("static/index.html");
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
