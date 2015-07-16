(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var Toolkits, _, __IFRAME_REGISTER_FUNCTION__, iframe_push;

String.prototype.replaceAll = function(s1, s2) {
  return this.replace(new RegExp(s1, "gm"), s2);
};

window.Toolkits = Toolkits = (function() {
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

  Toolkits.post = function(url, headers, data, mime) {
    var k, v, xmlhttp;
    xmlhttp = null;
    if (window.XMLHttpRequest) {
      xmlhttp = new XMLHttpRequest;
    } else {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("POST", url, false);
    for (k in headers) {
      v = headers[k];
      xmlhttp.setRequestHeader(k, v);
    }
    xmlhttp.setRequestHeader("Content-type", mime);
    xmlhttp.send(data);
    return xmlhttp.responseText;
  };

  Toolkits.async_post = function(url, headers, data, mime, callback, err) {
    var k, v, xmlhttp;
    xmlhttp = null;
    if (window.XMLHttpRequest) {
      xmlhttp = new XMLHttpRequest;
    } else {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
        if (!!callback) {
          return callback(xmlhttp, xmlhttp.responseText);
        }
      } else {
        if (!!err) {
          return err(xmlhttp);
        }
      }
    };
    xmlhttp.open("POST", url, false);
    for (k in headers) {
      v = headers[k];
      xmlhttp.setRequestHeader(k, v);
    }
    xmlhttp.setRequestHeader("Content-type", mime);
    xmlhttp.send(data);
    return xmlhttp.responseText;
  };

  Toolkits.get = function(url, headers) {
    var k, v, xmlhttp;
    xmlhttp = null;
    if (window.XMLHttpRequest) {
      xmlhttp = new XMLHttpRequest;
    } else {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET", url, false);
    if (!!headers) {
      for (k in headers) {
        v = headers[k];
        xmlhttp.setRequestHeader(k, v);
      }
    }
    xmlhttp.send();
    return xmlhttp.responseText;
  };

  Toolkits.async_get = function(url, headers, callback, err) {
    var k, v, xmlhttp;
    xmlhttp = null;
    if (window.XMLHttpRequest) {
      xmlhttp = new XMLHttpRequest;
    } else {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
        if (!!callback) {
          return callback(xmlhttp, xmlhttp.responseText);
        }
      } else {
        if (!!err) {
          return err(xmlhttp);
        }
      }
    };
    xmlhttp.open("GET", url, false);
    if (!!headers) {
      for (k in headers) {
        v = headers[k];
        xmlhttp.setRequestHeader(k, v);
      }
    }
    xmlhttp.send();
    return xmlhttp.responseText;
  };

  return Toolkits;

})();

window.__IFRAME__ = null;

__IFRAME_REGISTER_FUNCTION__ = [];

iframe_push = function(url, d) {
  if (!window.__IFRAME__) {
    return null;
  }
  return Toolkits.async_get(url, null, function(xmlhttp, data) {
    var k, v;
    for (k in d) {
      v = d[k];
      data = data.replaceAll("{{" + k + "}}", v);
      data = data.replaceAll("___" + k + "___", v);
    }
    return jQuery(window.__IFRAME__).append(data);
  });
};

window.iframe_register = function(f) {
  return __IFRAME_REGISTER_FUNCTION__.push(f);
};

window.iframe_pushs = function(d) {
  var _, j, l, len, len1, results;
  for (j = 0, len = d.length; j < len; j++) {
    _ = d[j];
    iframe_push(_.url, _.d);
  }
  results = [];
  for (l = 0, len1 = __IFRAME_REGISTER_FUNCTION__.length; l < len1; l++) {
    _ = __IFRAME_REGISTER_FUNCTION__[l];
    results.push(_());
  }
  return results;
};

window.iframe_clear = function() {
  if (!window.__IFRAME__) {
    return null;
  }
  window.__IFRAME__.innerHTML = '';
  return __IFRAME_REGISTER_FUNCTION__ = [];
};

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
      var _, l, len1;
      for (l = 0, len1 = elements.length; l < len1; l++) {
        _ = elements[l];
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
