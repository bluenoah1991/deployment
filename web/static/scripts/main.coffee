# CoffeeScript

class Toolkits
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
