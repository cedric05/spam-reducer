var http = require('http');
var fs = require('fs')
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write('Hello World!');
  console.log("request url "+req.url+" following data");
  req.on('data', d => {
    console.log(req.rawHeaders);
    process.stdout.write(d)
    fs.writeFile("test.eml", d, (error_message)=>{
        // var temp = "";
        // for(let header of  req.headers){
        //   temp
        // }
        console.log(error_message);
        });
    console.log("\ndone with  request");
  })
  res.end();
}).listen(8080);
