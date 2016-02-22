/**
 * Created by paulguichon on 19/02/2016.
 */
var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var plumber = require('gulp-plumber');

var paths = {
    lib: ['duck_recruitment/static/angular/angular.js',
      'duck_recruitment/static/angular/angular-route.js',
      'duck_recruitment/static/angular/angular-resource.js',
      'duck_recruitment/static/angular/ui-bootstrap-0.13.1.js',
      'duck_recruitment/static/recruitment/app/js/services.js',
      'duck_recruitment/static/recruitment/app/js/app.js',
      'duck_recruitment/static/recruitment/app/js/etat_heure/controllers.js',
      'duck_recruitment/static/recruitment/app/js/controllers.js']
};


// Compilation du coffeescript, minification et concaténation

gulp.task('app', function() {
  return gulp.src(paths.lib)
    .pipe(plumber())
    .pipe(concat('app.min.js'))
      // .pipe(uglify())
    .pipe(gulp.dest('duck_recruitment/static/recruitment/app/js/'));
});
// Copie des images statiques avec optimisation
// Relance les tâches ci-dessus lorsque les fichiers changent
gulp.task('watch', function () {
  gulp.watch(paths.lib, ['app']);
});
