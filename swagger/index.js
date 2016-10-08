var fs = require('fs');
var path = require('path');
var swaggermerge = require('./lib/merge');

var sourceFolder = __dirname;
var outputFolder = __dirname;
var outputFileName = 'openapi.json';

var basePath = '/api';
var host = 'hermes.com';
var schemes =  ['http'];

// basePath = '';
host = '';
// schemes = [];




var info = {
    "version": "1.0.0",
    "title": "New Zeus API"
};


swaggermerge.on('warn', function (msg) {
    console.warn(msg)
});

// 扫描json 文件
console.log("开始扫描json 文件=================================");

var swaggerJsonFiles = fs.readdirSync(sourceFolder).filter(function (file) {
    return /\.json$/.test(file) && outputFileName != file;
}).map(function (file) {
	var filePath = path.join(sourceFolder,file);
	console.log(filePath);
    return require(filePath);
});

console.log("结束扫描json文件=================================");


var merged = swaggermerge.merge(swaggerJsonFiles, info, basePath, host, schemes);

var data = JSON.stringify(merged, null, 4);

var outputFile = path.join(outputFolder, outputFileName);

console.log("输出文件：" + outputFile);

fs.writeFile(outputFile, data);

