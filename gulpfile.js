'use strict';

var config = require('./gulp-settings.json');
var gulp = require('gulp');
var gulpSequence = require('gulp-sequence')
var gutil = require('gulp-util');
var $ = require('gulp-load-plugins')();
var browserSync = require('browser-sync').create();
var sass = require('gulp-sass');
var sassLint = require('gulp-sass-lint');
var browserify = require('gulp-browserify');
var iconfont = require('gulp-iconfont');
var consolidate = require('gulp-consolidate');
var rename = require("gulp-rename");

var AUTOPREFIXER_BROWSERS = [
    'ie >= 10',
    'ie_mob >= 10',
    'ff >= 30',
    'chrome >= 34',
    'safari >= 7',
    'opera >= 23',
    'ios >= 7',
    'android >= 4.4'
];


var SASS_INCLUDE_PATHS = [
    './node_modules/foundation-sites/scss',
    './node_modules/font-awesome/scss',
    'static/sass/lib/motion-ui'
];

var FOUNDATION_JS = [
    './node_modules/foundation-sites/js/foundation.core.js',
    './node_modules/foundation-sites/js/foundation.util.box.js',
    './node_modules/foundation-sites/js/foundation.util.nest.js',
    './node_modules/foundation-sites/js/foundation.util.motion.js',
    './node_modules/foundation-sites/js/foundation.util.triggers.js',
    './node_modules/foundation-sites/js/foundation.util.keyboard.js',
    './node_modules/foundation-sites/js/foundation.util.touch.js',
    './node_modules/foundation-sites/js/foundation.util.mediaQuery.js',
    './node_modules/foundation-sites/js/foundation.util.timerAndImageLoader.js',
    './node_modules/foundation-sites/js/foundation.dropdown.js',
    './node_modules/foundation-sites/js/foundation.dropdownMenu.js',

];

var STATIC_ROOT = {
    dev: './website/site-static/',
    dist: './website/site-static/dist/'
};

var SASS_SRC_PATHS = [
    'static/sass/screen.sass'
];

var JS_SRC_PATHS = [
    './static/js/bundle.js'
];


var ICON_SRC_PATHS = [
    'static/icons/'
];

var ICON_SASS_PATHS = [
    'static/sass/site/style/'
];


var FONT_SRC_PATHS = [
    STATIC_ROOT.dev + 'fonts/**/*',
    './node_modules/font-awesome/fonts/**/*'
];

gulp.task('proxy', ['styles:base', 'scripts:base'], function () {

    browserSync.init({
        notify: false,
        port: config.local_port,
        host: config.hostname,
        open: false,
        proxy: {
            target: "127.0.0.1:" + config.proxy_port
        },
        ui: {
            port: config.local_port + 1,
            weinre: {
                port: config.local_port + 2
            }
        }
    });

    gulp.watch("static/sass/**/*.sass", ['styles:base', 'lint:styles']);
    gulp.watch("static/js/**/*.js", ['scripts:base']);
});

/**********************************************************************
 * stylesheet hanfling
 **********************************************************************/

gulp.task('styles', gulpSequence(
    'lint:styles',
    'styles:base'
));

gulp.task('styles:base', function () {
    return gulp.src(SASS_SRC_PATHS)
        .pipe($.sourcemaps.init())
        .pipe($.sass({
            includePaths: SASS_INCLUDE_PATHS,
            precision: 10
        }))
        .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest(STATIC_ROOT.dev + 'css/'))
        .pipe(browserSync.stream({match: '**/*.css'}))
        .pipe($.size({title: 'stylesheet size:'}));
});

/**********************************************************************
 * script handling
 **********************************************************************/

gulp.task('scripts', gulpSequence(
    'scripts:foundation',
    'scripts:base'
));

gulp.task('scripts:foundation', function () {
    return gulp.src(FOUNDATION_JS)
        .pipe($.babel({
            presets: ['es2015']
        }))
        .pipe($.concat('foundation.js'))
        .pipe(gulp.dest('./static/js/lib/'));
});

gulp.task('scripts:base', function () {
    // entry point to browserify
    gulp.src(JS_SRC_PATHS)
        .pipe(browserify({
            insertGlobals: true,
            debug: true
        }))
        .pipe($.concat('bundle.js'))
        .pipe(gulp.dest(STATIC_ROOT.dev + 'js/'))
        .pipe($.size({title: 'scripts size:'}));
});


/**********************************************************************
 * icon-font handling
 **********************************************************************/

// var runTimestamp = Math.round(Date.now()/1000);


/*
gulp.task('fonts:iconfont', function(){
  return gulp.src(ICON_SRC_PATHS)
    .pipe(iconfont({
      fontName: 'my-icons', // required
      prependUnicode: true, // recommended option
      formats: ['ttf', 'eot', 'woff', 'svg'], // default, 'woff2' and 'svg' are available
      timestamp: Math.round(Date.now()/1000), // recommended to get consistent builds when watching files
    }))
      .on('glyphs', function(glyphs, options) {
        // CSS templating, e.g.
        console.log(glyphs, options);
      })
    .pipe(gulp.dest(STATIC_ROOT.dev + 'fonts/'));
});
*/

var fontname = 'hoodini-icons'; // set name of your symbol font

gulp.task('fonts:iconfont', function () {
    gulp.src(ICON_SRC_PATHS + '*.svg')
        .pipe(iconfont({
            fontName: fontname,
            prependUnicode: true,
            formats: ['ttf', 'eot', 'woff', 'svg'],
            timestamp: Math.round(Date.now() / 1000),
            //appendCodepoints: true,
            //appendUnicode: false,
            normalize: true,
            fontHeight: 1001,
            //centerHorizontally: true,
        }))
        .on('glyphs', function (glyphs) {
            gulp.src(ICON_SRC_PATHS + '_iconfont.sass')
                .pipe(consolidate('lodash', {
                    glyphs: glyphs,
                    fontName: fontname,
                    fontPath: '../fonts/', // set path to font (from your CSS file if relative)
                    className: 'icon' // set class name in your CSS
                }))
                .pipe(rename({basename: '_icons'}))
                .pipe(gulp.dest('static/sass/site/style/')); // set path to export your CSS
        })
        .pipe(gulp.dest(STATIC_ROOT.dev + 'fonts/')); // set path to export your fonts

});


gulp.task('fonts:watch', ['fonts:iconfont'], function () {

    gulp.watch(ICON_SRC_PATHS, ['fonts:iconfont']);
});


/**********************************************************************
 * linters
 **********************************************************************/

gulp.task('lint', gulpSequence(
    'lint:styles'
));

gulp.task('lint:styles', function () {
    return gulp.src([
        '!./static/sass/site/components/plyr/*.s+(a|c)ss',
        '!./static/sass/site/components/swiper/*.s+(a|c)ss',
        './static/sass/**/*.s+(a|c)ss'

        ])
        .pipe(sassLint({
            configFile: './linters/sass-lint.yaml'
        }))
        .pipe(sassLint.format())
        .pipe(sassLint.failOnError())
});


/**********************************************************************
 * distripution tasks
 **********************************************************************/

gulp.task('dist', gulpSequence(
    'lint:styles',
    'dist:styles',
    //'lint:scripts',
    'scripts',
    'dist:scripts',
    'dist:fonts'
));

gulp.task('dist:styles', function () {
    return gulp.src(SASS_SRC_PATHS)
        .pipe($.sass({
            includePaths: SASS_INCLUDE_PATHS,
            precision: 10,
            outputStyle: 'compressed'
        }))
        .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
        .pipe($.concat('screen.css'))
        .pipe(gulp.dest(STATIC_ROOT.dist + 'css/'))
        .pipe($.size({title: 'stylesheet size:'}));
});

gulp.task('dist:scripts', function () {
    // entry point to browserify
    gulp.src(JS_SRC_PATHS)
        .pipe(browserify({
            insertGlobals: true,
            debug: false
        }))
        .pipe($.concat('bundle.js'))
        .pipe(gulp.dest(STATIC_ROOT.dist + 'js/'))
        .pipe($.size({title: 'script size:'}));
});

gulp.task('dist:fonts', function () {
    gulp.src(FONT_SRC_PATHS)
        .pipe(gulp.dest(STATIC_ROOT.dist + 'fonts/'))
        .pipe($.size({title: 'script size:'}));
});


/**********************************************************************
 * entry points
 **********************************************************************/

gulp.task('watch', ['proxy']);
