var RottenCrawler = require("./RottenCrawler.js");
var rp = require("request-promise");
var fs = require("fs");

var FOUT = "rt100List.json";
var LISTMAXLENGTH = 100;

var fetchList = function(results, rtList, i) {
    if (rtList.length >= LISTMAXLENGTH) return rtList;
    var rc = new RottenCrawler(results[i].url);
    return rc.getMovieInfo()
        .then(function() {
            rtList.push(rc);
            console.log(rtList.length + "\tDone fetching: " + results[i].title);

            return fetchList(results, rtList, i + 1);
        })
        .catch(function(err) {
            console.log(results[i].title + "\t" + err);
            return fetchList(results, rtList, i + 1);
        });
};

rp("http://d3biamo577v4eu.cloudfront.net/api/private/v1.0/m/list/find?limit=200&type=dvd-all&services=amazon%3Bamazon_prime%3Bflixster%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu&sortBy=release&country=TW")
    .then(function(response) {
        var results = JSON.parse(response).results;
        console.log("Start fetching...");

        results = results.filter(function(movie) {
            return movie.popcornScore && movie.tomatoScore;
        });

        return fetchList(results, [], 0);
    })
    .then(function(rtList) {
        fs.writeFile(FOUT, JSON.stringify(rtList, null, "\t"), "utf-8", function() {
            console.log("length: " + rtList.length);
            console.log("Done writing to file " + FOUT + ".");
        });
    });
