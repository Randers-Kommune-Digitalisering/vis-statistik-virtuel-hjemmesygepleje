const express = require('express'); 
const bodyParser = require('body-parser');
var cors = require('cors')

const app = express(); 
const PORT = 80;

const fileUploadRouter = require('./src/routes/fileUpload.route');
const tabletsRouter = require('./src/routes/tablets.route');
const callsRouter = require('./src/routes/calls.route');
const dbService = require('./src/services/db.service.js');

app.use(cors())
app.use(express.static('dist'));

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

app.use('/file-upload', fileUploadRouter);
app.use('/tablets', tabletsRouter);
app.use('/calls', callsRouter);

 /* Error handler middleware */
app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    console.error(err.message, err.stack);
    res.status(statusCode).json({'message': err.message});

    return;
});
  
app.listen(PORT, (error) =>{
  // Setup database tables if they do not exist
  dbService.setupDatabase().then( () => {
    if(!error) 
      console.log("Server is Successfully Running, and App is listening on port " + PORT) 
    else 
      console.log("Error occurred, server can't start", error); 
  });
});