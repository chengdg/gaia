'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var EventEmitter = require('events');

var Merger = function (_EventEmitter) {
  _inherits(Merger, _EventEmitter);

  function Merger() {
    _classCallCheck(this, Merger);

    return _possibleConstructorReturn(this, (Merger.__proto__ || Object.getPrototypeOf(Merger)).apply(this, arguments));
  }

  _createClass(Merger, [{
    key: '_mergeSecurityDefinitions',
    value: function _mergeSecurityDefinitions(swaggers) {
      var ret = null;
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.securityDefinitions) {
          var ref = Object.keys(swagger.securityDefinitions);
          for (var j = 0; j < ref.length; j++) {
            var key = ref[j];
            if (ret == null) {
              ret = {};
            }
            if (!ret[key]) {
              ret[key] = swagger.securityDefinitions[key];
            } else {
              this.emit("warn", 'multiple security definitions with the same name has define in swagger collection: ' + key);
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: '_mergedSchemes',
    value: function _mergedSchemes(swaggers) {
      var ret = [];
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.schemes) {
          var ref = swagger.schemes;
          for (var j = 0; j < ref.length; j++) {
            var scheme = ref[j];
            if (scheme && ret.indexOf(scheme) < 0) {
              ret.push(scheme);
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: '_mergedConsume',
    value: function _mergedConsume(swaggers) {
      var ret = [];
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.consumes) {
          var ref = swagger.consumes;
          for (var j = 0; j < ref.length; j++) {
            var consume = ref[j];
            if (consume && ret.indexOf(consume) < 0) {
              ret.push(consume);
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: '_mergedProduces',
    value: function _mergedProduces(swaggers) {
      var ret = [];
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.produces) {
          var ref = swagger.produces;
          for (var j = 0; j < ref.length; j++) {
            var produce = ref[j];
            if (produce && ret.indexOf(produce) < 0) {
              ret.push(produce);
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: '_mergedPaths',
    value: function _mergedPaths(swaggers) {
      var ret = null;
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.paths) {
          if (swagger.basePath == null) {
            swagger.basePath = '';
          }
          var ref = Object.keys(swagger.paths);
          for (var j = 0; j < ref.length; j++) {
            var key = ref[j];
            if (ret == null) {
              ret = {};
            }
            if (!ret[swagger.basePath + key]) {
              ret[swagger.basePath + key] = swagger.paths[key];
            } else {
              this.emit("warn", "multiple routes with the same name and base path has define in swagger collection: " + (swagger.basePath + key));
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: '_mergedDefinitions',
    value: function _mergedDefinitions(swaggers) {
      var ret = null;
      for (var i = 0; i < swaggers.length; i++) {
        var swagger = swaggers[i];
        if (swagger.definitions) {
          var ref = Object.keys(swagger.definitions);
          for (var j = 0; j < ref.length; j++) {
            var key = ref[j];
            if (ret == null) {
              ret = {};
            }
            if (!ret[key]) {
              ret[key] = swagger.definitions[key];
            } else {
              this.emit("warn", "multiple definitions with the same name has define in swagger collection: " + key);
            }
          }
        }
      }
      return ret;
    }
  }, {
    key: 'merge',
    value: function merge(swaggers, info, basePath, host, schemes) {
      var definitions = void 0,
          paths = void 0,
          ret = void 0,
          securityDefinitions = void 0;
      if ((typeof info === 'undefined' ? 'undefined' : _typeof(info)) !== 'object') {
        throw 'no info object as input or different format';
      }
      if (typeof basePath !== 'string') {
        throw 'no basePath string as input or different format';
      }
      if (typeof host !== 'string') {
        throw 'no host string as input or different format';
      }
      ret = {
        swagger: "2.0",
        info: info,
        host: host,
        basePath: basePath,
        schemes: schemes || this._mergedSchemes(swaggers),
        consumes: this._mergedConsume(swaggers),
        produces: this._mergedProduces(swaggers)
      };
      securityDefinitions = this._mergeSecurityDefinitions(swaggers);
      if (securityDefinitions) {
        ret.securityDefinitions = securityDefinitions;
      }
      definitions = this._mergedDefinitions(swaggers);
      if (definitions) {
        ret.definitions = definitions;
      }
      paths = this._mergedPaths(swaggers);
      if (paths) {
        ret.paths = paths;
      }
      return ret;
    }
  }]);

  return Merger;
}(EventEmitter);

var merger = new Merger();
module.exports = merger;