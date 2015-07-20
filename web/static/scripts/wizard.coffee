# CoffeeScript

# Don't ref DOM element

class Magician
    constructor: (@name) ->

    @wizard_sequence: {}

    @practice: (magic) =>
        w = @wizard_sequence[magic.wizardName]
        if w?
            w.practice magic
        else
            w = new Wizard magic.wizardName
            @wizard_sequence[magic.wizardName] = w
            w.practice magic

    @fire: (wizardName, mana) =>
        w = @wizard_sequence[wizardName]
        if w?
            w.fire mana

class Wizard
    constructor: (@name) ->

    magic_sequence: []

    practice: (magic) ->
        @magic_sequence[magic.index] = magic 

    fire: (mana) ->
        try_ = true
        for m in @magic_sequence
            if m?
                if m.ready
                    mana = m.incantation(m, mana)
                else if try_
                    try_ = false
                    mana = m.incantation(m, mana)
                    if m.ready then try_ = true

class Magic
    constructor: (@name, @wizardName, @index, @incantation) ->

    ready: false

    mana: {}


module.exports.Magician = Magician
module.exports.Magic = Magic


# Example (each magic)

# Input data 100 to textbox a, Output a * 2

# window.addEventListener('load', function(){
#     var m = new Magic('magicName', 'wizardName', 1, function(magic, mana){

#         # mana == 100
#         # let textbox_a.value = mana

#         # if all done
#         magic.ready = true
#         # else
#         magic.ready = false

#         return mana * 2;
#     }); 
#     Magician.practice(m);

#     # retry fire when you modify some values
#     Magician.fire('wizardName', null);
# }); 