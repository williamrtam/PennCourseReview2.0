var express = require('express');
var router = express.Router();
var path = require('path');

// Connect string to MySQL
var mysql = require('mysql');
var connection = mysql.createConnection({
  host     : 'cis450.c5rvqqjl9c91.us-east-1.rds.amazonaws.com',
  user     : 'cis450',
  password : '',
  database : ''
});
// 147561825462-a04fittba8hpc0fqtd00abarboa07tli.apps.googleusercontent.com
// y4XCfko-sOuVq8eq5WpVPE5F

// Connect to DynamoDB
var AWS = require('aws-sdk');
// Set the region
AWS.config.update({region: 'us-east-1'});

// Create the DynamoDB service object
ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

// var ddb = new AWS.DynamoDB.DocumentClient();

router.get('/loggin',function(req,res) {
  res.sendFile(path.join(__dirname, '../', 'views', 'loggin.html'));
});

router.get('/loginAuth', function(req,res) {
  req.session.loggedIn = "YES";
  res.json({ok:'OK'});
})

router.get('/logout',function(req,res) {
  req.session.loggedIn = undefined;
  res.redirect('/');
})

/* GET home page. */
router.get('/', function(req, res, next) {

  if (req.session && req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  res.sendFile(path.join(__dirname, '../', 'views', 'index.html'));
});

router.get('/quiz', function(req, res, next) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  res.sendFile(path.join(__dirname, '../', 'views', 'quiz.html'));
});

router.get('/result/prof', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
    var query = 'SELECT name, avg_rating FROM Professor GROUP BY avg_rating ORDER BY avg_rating DESC LIMIT 50;';
    connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
        res.json(rows);
    }
    });
});

router.get('/result/course', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
    var query = 'select * from Course where quality > -1 and difficulty > -1 order by quality desc limit 50;';
    connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
        res.json(rows);
    }
    });

});

router.get('/result/easy', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
    var query = 'select * from Course where quality > -1 and difficulty > -1 order by difficulty asc limit 50;';
    connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
        res.json(rows);
    }
    });
});

router.get('/result/hard', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
    var query = 'select * from Course where quality > -1 order by difficulty desc limit 50;';
    connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
        res.json(rows);
    }
    });
});


router.get('/result/:search/:searchopt/:includeTimes/:startAfter/:endBefore/:includeDiff/:diffAbove/:diffBelow/:includeQual/:qualAbove/:qualBelow/:includeProfQual/:profqualAbove/:profqualBelow/:includeNumStudents/:numStudentsBelow/:includeMeetinDays/:meetingDaysOptions', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  var searchopt = req.params.searchopt;
  var includeTimes = req.params.includeTimes;
  var search = req.params.search;
  var start = req.params.startAfter;
  var end = req.params.endBefore;
  var includeDiff = req.params.includeDiff;
  var diffAbove = req.params.diffAbove;
  var diffBelow = req.params.diffBelow;
  var includeQual = req.params.includeQual;
  var qualAbove = req.params.qualAbove;
  var qualBelow = req.params.qualBelow;
  var includeProfQual = req.params.includeProfQual;
  var profqualAbove = req.params.profqualAbove;
  var profqualBelow = req.params.profqualBelow;
  var includeNumStudents = req.params.includeNumStudents;
  var numStudentsBelow = req.params.numStudentsBelow;
  var includeMeetinDays = req.params.includeMeetinDays;
  var meetingDaysOptions = req.params.meetingDaysOptions;

  console.log(req.params);

  if (searchopt === "Course") {
    var trimmed = search.trim();
    var query = 'select * from CourseListing c inner join SectionAverages s ON s.secid like concat(c.secid, "%") where c.secid like "' + trimmed + '%"' 
        + ' and s.quality > -1 and s.difficulty > -1'

    if (includeTimes == "false" && includeMeetinDays == "false") {
      query = 'select * from Section s inner join Teaches t on s.sid = t.sid inner join Professor p on t.pid = p.pid where s.sid like "' + trimmed + '%"' 
        + ' and s.quality > -1 and s.difficulty > -1'
    }

    if (includeDiff == "true") {
      query += ' and s.difficulty > ' + diffAbove + ' and s.difficulty < ' + diffBelow;
    }

    if (includeQual == "true") {
      query += ' and s.quality > ' + qualAbove + ' and s.quality < ' + qualBelow;

    }

    if (includeTimes == "true") {
        query += ' and c.start_time > ' + start + ' and c.end_time < ' + end;
    }

    if (includeProfQual == "true" && includeTimes == "false" && includeMeetinDays == "false") {
      query += ' and t.InstructorQuality > ' + profqualAbove + ' and t.InstructorQuality < ' + profqualBelow;
    } else if (includeProfQual == "true") {
      query += ' and s.InstructorQuality > ' + profqualAbove + ' and s.InstructorQuality < ' + profqualBelow;
    }

    if (includeNumStudents == "true") {
      query += ' and s.num_students < ' + numStudentsBelow;
    }

    if (includeMeetinDays == "true") {
      query += ' and c.days like "%' + meetingDaysOptions + '%"' 
    }


    query += ';';
    // console.log(query);
    connection.query(query, function(err, rows, fields) {
        if (err) console.log(err);
        else {
          res.json(rows);
        }
      });
    
  } else if (searchopt === "Professor") {

      var query = 'select distinct * from Professor p inner join Teaches t on p.pid = t.pid inner join Section s on t.sid = s.sid where p.name like "' + search  + '%"';

      if (includeQual == 'true') {
        query += ' and p.avg_rating > ' + qualAbove + ' and p.avg_rating < ' + qualBelow;
      }

      query += ' group by p.pid,t.sid;';
      connection.query(query, function(err, rows, fields) {
        if (err) console.log(err);
        else {
          res.json(rows);
        }
      });

  } else {
    res.json({'results':'undefined'});
  }

});


router.get('/result/descrip/:search', function(req, res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  var search = req.params.search;

  var params = {
    TableName: 'Project',
    Key: {
      'code' : {S:search},
    },
    ProjectionExpression: 'description'
  };

  ddb.getItem(params, function(err, data) {
    if (err) {
      console.log("Error", err);
    } else {
      if (data.Item === undefined) {
        console.log('No description found');
        res.json();
      } else {
        console.log("Success", data.Item.description.S);
        res.json({description:data.Item.description.S});
      }
    }
  });
});

router.get('/quiz/alldept', function(req,res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  var query = "select did from Department;";
  connection.query(query, function(err, rows, fields) {
    if (err) 
      console.log(err);
    else {
      res.json(rows);
    }
  });
});

router.get('/quiz/dept/:dept', function(req,res) {
  if (req.session === undefined || req.session.loggedIn === undefined) {
    res.redirect('/loggin');
    return;
  }
  var did = req.params.dept;
  // $scope.Answers = [[(deptName+"110"),(deptName+"121"),(deptName+"450")],["Susan Davidson","Paul Will McBurney","Michael Jordan"],[(deptName+"110"),(deptName+"121"),(deptName+"450")]];
  // $scope.Questions = [{answer:"0",text:"Which of these has a higher course difficulty?",index:0},{answer:"1",index:1,text:"Which of these professors does not teach in this department?"},{answer:"2",index:2,text:"Which of these has the highest course quality?"}];

  var answers = [];
  var arr = []; 
  var answer_key = [];
  
  query = "select code, name, quality, difficulty from Course where did = '" + did + "';"
  connection.query(query, function(err, rows, fields) {
    if (err) 
      console.log(err);
    else {
      // console.log(fields);
      if (rows.length === 0) {
        console.log('hello',query,rows);
        answers[0] = [];
        answer_key[0] = [];
      } else {
        arr = [];
        randnum = getRandomInt(0,(rows.length)-1);
        arr[0] = {code:rows[randnum].code,difficulty:rows[randnum].difficulty};
        randnum = getRandomInt(0,(rows.length)-1);
        arr[1] = {code:rows[randnum].code,difficulty:rows[randnum].difficulty};
        randnum = getRandomInt(0,(rows.length)-1);
        arr[2] = {code:rows[randnum].code,difficulty:rows[randnum].difficulty};
        answers[0] = arr;

        if (arr[0].difficulty > arr[1].difficulty && arr[0].difficulty > arr[2].difficulty) 
         answer_key[0] = 0;
        else if (arr[1].difficulty > arr[0].difficulty && arr[1].difficulty > arr[2].difficulty) 
          answer_key[0] = 1;
        else 
          answer_key[0] = 2;
      }
      query = "select name, avg_rating from InDepartment i inner join Professor p on i.pid = p.pid where i.did = '" + did + "';";
      connection.query(query, function(err, rows, fields) {
        if (err) 
          console.log(err);
         else {
          // console.log(rows);
          if (rows.length === 0) {
            console.log('hello',query,rows);
            answers[0] = [];
            answer_key[0] = [];
          } else {
            arr = [];
            randnum = getRandomInt(0,(rows.length)-1);
            arr[0] = {name:rows[randnum].name,rating:rows[randnum].avg_rating};
            randnum = getRandomInt(0,(rows.length)-1);
            arr[1] = {name:rows[randnum].name,rating:rows[randnum].avg_rating};
            randnum = getRandomInt(0,(rows.length)-1);
            arr[2] = {name:rows[randnum].name,rating:rows[randnum].avg_rating};
            answers[1] = arr;

            if (arr[0].rating > arr[1].rating && arr[0].rating > arr[2].rating) 
                answer_key[1] = 0;
              else if (arr[1].rating > arr[0].rating && arr[1].rating > arr[2].rating) 
                answer_key[1] = 1;
              else 
                answer_key[1] = 2;
          }
          query = "select code, name, quality, difficulty from Course where did = '" + did + "';"
          connection.query(query, function(err, rows, fields) {
            if (err) 
              console.log(err);
            else {
              // console.log(rows);
              if (rows.length === 0) {
                console.log('hello',query,rows);
                answers[0] = [];
                answer_key[0] = [];
              } else {
                arr = [];
                randnum = getRandomInt(0,(rows.length)-1);
                arr[0] = {code:rows[randnum].code,quality:rows[randnum].quality};
                randnum = getRandomInt(0,(rows.length)-1);
                arr[1] = {code:rows[randnum].code,quality:rows[randnum].quality};
                randnum = getRandomInt(0,(rows.length)-1);
                arr[2] = {code:rows[randnum].code,quality:rows[randnum].quality};
                answers[2] = arr;

                if (arr[0].quality > arr[1].quality && arr[0].quality > arr[2].quality) 
                  answer_key[2] = 0;
                else if (arr[1].quality > arr[0].quality && arr[1].quality > arr[2].quality) 
                  answer_key[2] = 1;
                else 
                  answer_key[2] = 2;
              }
              answers[3] = answer_key;
              console.log(answers);
              res.json(answers);
            }
          });
        }
      })
    }
  });


});

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}

module.exports = router;
