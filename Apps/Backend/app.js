const cors = require('cors');
var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;

const router = require('./route');
const expressSession = require('express-session');

app.use(cors({
  origin: [
    "http://localhost:4200"
  ],
  credentials: true
}));

app.use(express.json());

app.use(express.urlencoded({
  extended: true
}));

const session = expressSession({
  secret: 'YOUR-SESSION-CODE-e58c97e1-1fd4-435d-9035-18b3496689f6',
  resave: false,
  saveUninitialized: false,
  unset: 'destroy'
});
app.use(session);

app.use('/', router);

app.listen(port);

console.log('Angular App - RESTful API server started on port: ' + port);
