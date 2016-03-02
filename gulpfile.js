/**
 * Created by paulguichon on 19/02/2016.
 */
var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var plumber = require('gulp-plumber');

var paths = {
    lib: [
      'static/angular/angular.js',
      'static/angular/angular-route.js',
      'static/angular/angular-resource.js',
      'static/angular/ui-bootstrap-0.13.1.js',
      'static/recruitment/app/js/services.js',
      'static/recruitment/app/js/app.js',
      'static/recruitment/app/js/etat_heure/controllers.js',
      'static/recruitment/app/js/controllers.js']
};


// Compilation du coffeescript, minification et concaténation

gulp.task('app', function() {
  return gulp.src(paths.lib)
    .pipe(plumber())
    .pipe(concat('app.min.js'))
      // .pipe(uglify())
    .pipe(gulp.dest('static/recruitment/app/js/'));
});

gulp.task('watch', function () {
  gulp.watch(paths.lib, ['app']);
});
