/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is not neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/*!**********************!*
  !*** ./src/entry.js ***!
  \**********************/
eval("var pswpElement = document.querySelectorAll('.pswp')[0];\r\n\r\n// build items array\r\nvar items = [\r\n    {\r\n        src: 'https://placekitten.com/600/400',\r\n        w: 600,\r\n        h: 400\r\n    },\r\n    {\r\n        src: 'https://placekitten.com/1200/900',\r\n        w: 1200,\r\n        h: 900\r\n    }\r\n];\r\n\r\n// define options (if needed)\r\nvar options = {\r\n    // optionName: 'option value'\r\n    // for example:\r\n    index: 0 // start at first slide\r\n};\r\n\r\n// Initializes and opens PhotoSwipe\r\nvar gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);\r\ngallery.init();\n\n//# sourceURL=webpack://temporarymoments/./src/entry.js?");
/******/ })()
;