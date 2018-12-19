var system = requiore("system");
var url = system.stdin.readLine();
var page = require('webpage').create();
page.open(url, function() {
    setTimeout(function() {
        page.render(url+'.png');
        phantom.exit();
    }, 200);
}); 
system.stdout.writeLine(url+'.png');
