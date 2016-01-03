# RottenCrawler
Fetch Rotten Tomatoes Data without an API key.

---

### API (`RottenCrawler.js`)

#### `RottenCrawler(movieURL)`
Construct a new `RottenCrawler` class, where `movieURL` is the RT's url e.g. `/m/The_Dark_Knight/`.  
return the class;
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
```

---

#### `RottenCrawler.prototype.getCritics(page)`  
get all the critics data in page `page` and store them into `RottenCrawler.prototype.critics`.  
return a promise.
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
rc.getCritics(1)
    .then(function() {
        console.log(rc.critics);
    });
```
---

#### `RottenCrawler.prototype.getReviews(page)`  
get all the audience reviews data in page `page` and store them into `RottenCrawler.prototype.reviews`.  
return a promise.
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
rc.getReviews(1)
    .then(function() {
        console.log(rc.reviews);
    });
```
---

#### `RottenCrawler.prototype.getAllCritics()`  
get all the critics of the movies of every pages. Store them all into `RottenCrawler.prototype.critics`.  
return a promise.
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
rc.getAllCritics()
    .then(function() {
        console.log(rc.critics);
    });
```
---

#### `RottenCrawler.prototype.getAllReviews()`  
get all the audience reviews of the movies of every pages. Store them all into `RottenCrawler.prototype.reviews`.  
return a promise.
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
rc.getAllReviews()
    .then(function() {
        console.log(rc.reviews);
    });
```
---

#### `RottenCrawler.prototype.getMovieInfo()`  
get the movie info along with all the critics and audience reviews of the movie, store them into the class.  
return a promise.
```
var rc = new RottenCrawler('/m/The_Dark_Knight/');
rc.getMovieInfo()
    .then(function() {
        console.log(rc);
    });
```
