var https = require('https'),
    fs = require('fs'),
    crypto = require('crypto');

https.globalAgent.maxSockets = 20;

var CAPTCHA_URL = 'https://sodexosaldocartao.com.br/saldocartao/jcaptcha.do';

function download_captcha (done) {
    var request = https.get(CAPTCHA_URL, function (res) {
        var md5 = crypto.createHash('md5');
        var imageData = '';

        res.setEncoding('binary');

        res.on('data', function (chunk) {
            md5.update(chunk);
            imageData += chunk;
        });

        res.on('end', function() {
            var fileName = md5.digest('hex') + '.jpg';
            fs.writeFile('captcha/' + fileName, imageData, 'binary', function (err) {
                if (done) done(err);
            });
        });
    });
}


function multiple_download (quantity, done) {
    var start = Date.now(),
        download_count = 0;

    function _done () {
        download_count += 1;
        if (download_count >= quantity) {
            done();
        }
    }

    for (var i=quantity; i--;) {
        download_captcha(_done);
    }
}

var start = Date.now(),
    file_quantity = 10000;

multiple_download(file_quantity, function () {
    var time = (Date.now() - start) / 1000;
    console.log('done');
    console.log('speed', file_quantity / time);
});

