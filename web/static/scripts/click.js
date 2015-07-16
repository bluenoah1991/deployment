(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var Toolkits, _;

Toolkits = (function() {
  function Toolkits() {}

  Toolkits.hasClass = function(element, className) {
    var reg;
    reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
    return element.className.match(reg);
  };

  Toolkits.addClass = function(element, className) {
    if (!this.hasClass(element, className)) {
      return element.className += " " + className;
    }
  };

  Toolkits.removeClass = function(element, className) {
    var reg;
    if (this.hasClass(element, className)) {
      reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
      return element.className = element.className.replace(reg, ' ');
    }
  };

  return Toolkits;

})();

window.crumbs = function(d) {
  var body, i, item, j, len, seg;
  body = '<i class="icon-home icon-large"></i>';
  for (i = j = 0, len = d.length; j < len; i = ++j) {
    item = d[i];
    if (!!!item.url || item.url === '') {
      seg = "<span>" + item.name + "</span>";
      body += seg;
    } else {
      seg = "<a href=\"" + item.url + "\">" + item.name + "</a>";
      body += seg;
    }
    if (i < d.length - 1) {
      body += '<i class="icon-angle-right"></i>';
    }
  }
  return body;
};

window.clickgo = function(elements) {
  var ele, j, len, results;
  results = [];
  for (j = 0, len = elements.length; j < len; j++) {
    ele = elements[j];
    results.push(ele.addEventListener('click', function(e) {
      return e.srcElement.style.display = 'none';
    }));
  }
  return results;
};

window.clicktoggle = function(element, target) {
  return element.addEventListener('click', function(e) {
    var focus;
    focus = e.srcElement.getAttribute('focus');
    if ((focus != null) && focus === '1') {
      e.srcElement.setAttribute('focus', '0');
      return target.style.display = 'none';
    } else {
      e.srcElement.setAttribute('focus', '1');
      return target.style.display = 'block';
    }
  });
};

window.clickfocus = function(elements) {
  var ele, j, len, results;
  results = [];
  for (j = 0, len = elements.length; j < len; j++) {
    ele = elements[j];
    results.push(ele.addEventListener('click', function(e) {
      var _, k, len1;
      for (k = 0, len1 = elements.length; k < len1; k++) {
        _ = elements[k];
        Toolkits.removeClass(_, 'focus');
      }
      return Toolkits.addClass(e.srcElement, 'focus');
    }));
  }
  return results;
};

_ = require('./wizard.coffee');

window.Magician = _.Magician;

window.Magic = _.Magic;


},{"./wizard.coffee":2}],2:[function(require,module,exports){
var Magic, Magician, Wizard;

Magician = (function() {
  function Magician(name) {
    this.name = name;
  }

  Magician.wizard_sequence = {};

  Magician.practice = function(magic) {
    var w;
    w = Magician.wizard_sequence[magic.wizardName];
    if (w != null) {
      return w.practice(magic);
    } else {
      w = new Wizard(magic.wizardName);
      Magician.wizard_sequence[magic.wizardName] = w;
      return w.practice(magic);
    }
  };

  Magician.fire = function(wizardName, mana) {
    var w;
    w = Magician.wizard_sequence[wizardName];
    if (w != null) {
      return w.fire(mana);
    }
  };

  return Magician;

})();

Wizard = (function() {
  function Wizard(name) {
    this.name = name;
  }

  Wizard.prototype.magic_sequence = [];

  Wizard.prototype.practice = function(magic) {
    return this.magic_sequence[magic.index] = magic;
  };

  Wizard.prototype.fire = function(mana) {
    var i, len, m, ref, results, try_;
    try_ = true;
    ref = this.magic_sequence;
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      m = ref[i];
      if (m != null) {
        if (m.ready) {
          results.push(mana = m.incantation(m, mana));
        } else if (try_) {
          try_ = false;
          mana = m.incantation(m, mana);
          if (m.ready) {
            results.push(try_ = true);
          } else {
            results.push(void 0);
          }
        } else {
          results.push(void 0);
        }
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  return Wizard;

})();

Magic = (function() {
  function Magic(name, wizardName1, index, incantation) {
    this.name = name;
    this.wizardName = wizardName1;
    this.index = index;
    this.incantation = incantation;
  }

  Magic.prototype.ready = false;

  Magic.prototype.mana = {};

  return Magic;

})();

module.exports.Magician = Magician;

module.exports.Magic = Magic;


},{}]},{},[1]);
