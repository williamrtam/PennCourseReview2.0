
var app = angular.module('550project',[]);
app.controller('quizController', function($scope, $http) {
    console.log('Quiz controller: hello, world');
    
    $scope.quizSetup = true;
    $scope.quizResults = false;
    $http({
          method: 'GET',
          url: '/quiz/alldept'
        }).then(function successCallback(response) {
            $scope.departments = response.data;
            console.log(response.data);
          }, function errorCallback(err) {
            console.log(err);
          });
    
    $scope.selectDept = function (deptName) {
        $scope.Answers = null;
        console.log(deptName.did);
        $scope.quizSetup = false;
        $scope.deptSelected = deptName;
        $scope.Questions = [
        {text:"Which of these has a higher course difficulty?",index:0},
        {index:1,text:"Which of these professors has the highest rating in this department?"},
        {index:2,text:"Which of these has the highest course quality?"}];
        $http({
          method: 'GET',
          url: '/quiz/dept/'+deptName.did
        }).then(function successCallback(response) {
            $scope.Answers = response.data;
            console.log($scope.Answers[3]);
          }, function errorCallback(err) {
            console.log(err);
          });
        console.log($scope.Answers);
        $scope.answer1 = undefined;
        $scope.answer2 = undefined;
        $scope.answer3 = undefined;
    }
    $scope.submitQuiz = function() {
        console.log('Quiz');
        $scope.quizResults = true;
        $scope.quizSetup = false;
        var correct = 0;
        if ($scope.answer1) {
            correct = correct + ($scope.answer1.val === $scope.Answers[3][0] + "");
            console.log(correct);
        }
        if ($scope.answer2) {
            correct = correct + ($scope.answer2.val === $scope.Answers[3][1] + "");
            console.log(correct);
        }
        if ($scope.answer3) {
            correct = correct + ($scope.answer3.val === $scope.Answers[3][2] + "");
            console.log(correct);
        }
        $scope.score = "You got " + correct + " correct out of 3!";
    }

    $scope.resetQuiz = function () {
        $scope.quizResults = false;
        $scope.quizSetup = true;
    }
});
app.controller('searchController', function($scope, $http) {
        $scope.message="";
        $scope.show = false;
        $scope.show_no_time = false;
        $scope.showProf = false;
        $scope.showDescrip = false;
        $scope.showCourse = false;
        $scope.includeTimes = false;
        $scope.includeDiff = false;
        $scope.includeQual = false;
        $scope.diffAbove="0.0";
        $scope.diffBelow="4.0";        
        $scope.qualAbove="0.0";
        $scope.qualBelow="4.0";
        $scope.selectAfter = "8.0";
        $scope.selectBefore ="21.3";
        $scope.includeProfQual = false;
        $scope.profqualAbove="0.0";
        $scope.profqualBelow="4.0";
        $scope.includeNumStudents = false;
        $scope.numStudentsBelow="600";
        $scope.includeMeetingDays = false;
        $scope.meetingDaysOptions="M";


        //Search Button clicked
        $scope.Search = function() {
            $scope.showProf = false;
            $scope.showCourse = false;
            $scope.showDescrip = false;

            if ($scope.opt == 'Course') {
                    $scope.showCourse = false;
                    $scope.showProfSearch = false;
                if (!$scope.includeTimes && !$scope.includeMeetingDays) {
                    $scope.show = false; 
                    $scope.show_no_time = true;
                } else {
                    $scope.show = true; 
                    $scope.show_no_time = false;
                }
               

            } else if ($scope.opt == 'Professor') {
                $scope.showCourse = false;
                $scope.show = false;
                $scope.show_no_time = false;
                $scope.showProfSearch = true;
            }

            if ($scope.search === undefined || $scope.search === "") {
                $scope.search = ' ';
            }

            var request = $http.get('/result/'+$scope.search + '/' + $scope.opt + '/' + $scope.includeTimes + '/' +
            $scope.selectAfter + '/' + $scope.selectBefore + '/' + $scope.includeDiff +"/" + $scope.diffAbove + "/" + $scope.diffBelow + "/" 
            + $scope.includeQual + "/" + $scope.qualAbove + "/" + $scope.qualBelow + "/" + $scope.includeProfQual + "/" + $scope.profqualAbove + "/" 
            + $scope.profqualBelow + "/" + $scope.includeNumStudents + "/" + $scope.numStudentsBelow + "/" + $scope.includeMeetingDays + "/" + $scope.meetingDaysOptions);
            request.success(function(data) {
                $scope.data = data;
                console.log(data)
            });
            request.error(function(data){
                console.log('err');
            });
        };

        //50 Easiest Courses Button Clicked
        $scope.easiestCourse = function() {
            $scope.showProf = false;
            $scope.show = false;
            $scope.show_no_time = false;
            $scope.showCourse = true;
            $scope.showDescrip = false;
            $scope.showProfSearch = false;

            var request = $http.get('/result/easy');
            request.success(function(data) {
                $scope.datacourse = data;
            });
            request.error(function(data){
                console.log('err');
            });
        };

        //50 Hardest Courses Button Clicked
        $scope.hardestCourse = function() {
            $scope.showProf = false;
            $scope.show = false;
            $scope.show_no_time = false;
            $scope.showCourse = true;
            $scope.showDescrip = false;
            $scope.showProfSearch = false;

            var request = $http.get('/result/hard/');
            request.success(function(data) {
                $scope.datacourse = data;
            });
            request.error(function(data){
                console.log('err');
            });
        };

        //50 Best Rated Professors Button Clicked
        $scope.bestProf = function() {
            $scope.show = false;
            $scope.show_no_time = false;
            $scope.showProf = true;
            $scope.showCourse = false;
            $scope.showDescrip = false;
            $scope.showProfSearch = false;

            var request = $http.get('/result/prof/');
            request.success(function(data) {
                console.log(data);
                $scope.dataprof = data;
            });
            request.error(function(data){
                console.log('err');
            });
    };

        //50 Highest Rated Courses Button Clicked
        $scope.bestCourse = function() {
            $scope.showProf = false;
            $scope.show = false;
            $scope.show_no_time = false;
            $scope.showCourse = true;
            $scope.showDescrip = false;
            $scope.showProfSearch = false;

            var request = $http.get('/result/course');
            request.success(function(data) {
                $scope.datacourse = data;
            });
            request.error(function(data){
                console.log('err');
            });
    };

    // Get description for a course
    $scope.fetchDescription = function(data) {
        var section = data.secid.split("-");
        var search = section[0] + "-" + section[1];

        $scope.showDescrip = true;

        var request = $http.get('/result/descrip/'+search);
        request.success(function(data) {
            console.log("description:",data);
            if (data.description !== undefined)
                $scope.description = data.description;
            else 
                $scope.description = "There is no description availible for this course";
        });
        request.error(function(data){
            console.log('err');
        });
    };

    $scope.PresetDescriptions = function(data) {
        console.log(data);
        $scope.showDescrip = true;
        var request = $http.get('/result/descrip/'+data.code);
        request.success(function(data) {
            console.log("description:",data);
            if (data.description !== undefined)
                $scope.description = data.description;
            else 
                $scope.description = "There is no description availible for this course";
        });
        request.error(function(data){
            console.log('err');
        });
    };
});
