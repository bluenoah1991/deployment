# CoffeeScript

String.prototype.replaceAll  = (s1, s2) ->
    @replace(new RegExp(s1, "gm"), s2)

window.Toolkits = class Toolkits
    @hasClass = (element, className) -> 
        reg = new RegExp('(\\s|^)' + className + '(\\s|$)') 
        return element.className.match(reg) 

    @addClass = (element, className) ->
        if !@hasClass(element, className) 
            element.className += " " + className

    @removeClass = (element, className) ->
        if @hasClass(element, className)
            reg = new RegExp('(\\s|^)' + className + '(\\s|$)') 
            element.className = element.className.replace(reg, ' ')

    @post = (url, headers, data, mime) ->
        xmlhttp = null
        if window.XMLHttpRequest
            xmlhttp = new XMLHttpRequest
        else
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        xmlhttp.open("POST", url, false)
        for k, v of headers
            xmlhttp.setRequestHeader(k, v)
        xmlhttp.setRequestHeader("Content-type", mime)
        xmlhttp.send(data)
        return xmlhttp.responseText

    @async_post = (url, headers, data, mime, callback, err) ->
        xmlhttp = null
        if window.XMLHttpRequest
            xmlhttp = new XMLHttpRequest
        else
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        xmlhttp.onreadystatechange = ->
            if xmlhttp.readyState == 4 and xmlhttp.status == 200
                if !!callback then callback(xmlhttp, xmlhttp.responseText)
            else
                if !! err then err(xmlhttp)
        xmlhttp.open("POST", url, false)
        for k, v of headers
            xmlhttp.setRequestHeader(k, v)
        xmlhttp.setRequestHeader("Content-type", mime)
        xmlhttp.send(data)
        return xmlhttp.responseText

    @get = (url, headers) ->
        xmlhttp = null
        if window.XMLHttpRequest
            xmlhttp = new XMLHttpRequest
        else
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        xmlhttp.open("GET", url, false)
        if !!headers
            for k, v of headers
                xmlhttp.setRequestHeader(k, v)
        xmlhttp.send()
        return xmlhttp.responseText

    @async_get = (url, headers, callback, err) ->
        xmlhttp = null
        if window.XMLHttpRequest
            xmlhttp = new XMLHttpRequest
        else
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        xmlhttp.onreadystatechange = ->
            if xmlhttp.readyState == 4 and xmlhttp.status == 200
                if !!callback then callback(xmlhttp, xmlhttp.responseText)
            else
                if !! err then err(xmlhttp)
        xmlhttp.open("GET", url, false)
        if !!headers
            for k, v of headers
                xmlhttp.setRequestHeader(k, v)
        xmlhttp.send()
        return xmlhttp.responseText


window.__IFRAME__ = null
__IFRAME_REGISTER_FUNCTION__ = []

iframe_push = (url, d) ->
    if !window.__IFRAME__
        return null
    Toolkits.async_get(url, null, (xmlhttp, data)->
        for k, v of d
            data = data.replaceAll("{{#{k}}}", v)
            data = data.replaceAll("___#{k}___", v)
        #window.__IFRAME__.insertAdjacentHTML('beforeEnd', data) # Bug scripts not execute
        jQuery(window.__IFRAME__).append(data)
    )

window.iframe_register = (f) ->
    __IFRAME_REGISTER_FUNCTION__.push(f)

window.iframe_pushs = (d) ->
    for _ in d
        iframe_push(_.url, _.d)
    for _ in __IFRAME_REGISTER_FUNCTION__
        _()

window.iframe_clear = ->
    if !window.__IFRAME__
        return null
    window.__IFRAME__.innerHTML = ''
    __IFRAME_REGISTER_FUNCTION__ = []

window.crumbs = (d) ->
    body = '<i class="icon-home icon-large"></i>'
    for item, i in d
        if !!!item.url or item.url is ''
            seg = "<span>#{item.name}</span>"
            body += seg
        else
            seg = "<a href=\"#{item.url}\">#{item.name}</a>"
            body += seg
        if i < d.length - 1
            body += '<i class="icon-angle-right"></i>'
    return body

window.clickgo = (elements) ->
    for ele in elements
        ele.addEventListener 'click', (e) ->
            e.srcElement.style.display = 'none'

window.clicktoggle = (element, target) ->
    element.addEventListener 'click', (e) ->
        focus = e.srcElement.getAttribute('focus')
        if focus? and focus is '1'
            e.srcElement.setAttribute('focus', '0')
            target.style.display = 'none'
        else
            e.srcElement.setAttribute('focus', '1')
            target.style.display = 'block'

window.clickfocus = (elements) ->
    for ele in elements
        ele.addEventListener 'click', (e) ->
            for _ in elements
                Toolkits.removeClass(_, 'focus')
            Toolkits.addClass(e.srcElement, 'focus')

_ = require('./wizard.coffee')
window.Magician = _.Magician
window.Magic = _.Magic
