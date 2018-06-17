import z from './zombular.js';

const Styles = z('style', `
@import url('./lib/semantic.min.css');
@import url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:400);

* { margin: 0; padding: 0; list-style-type: none; }

body { font-family: 'Source Sans Pro', sans-serif; letter-spacing: 0.05em;
	line-height: 24px; background-color: #111; font-weight: 400; }

.flex { display: flex; }
.nowrap { flex-wrap: nowrap; }
.column { flex-direction: column; }
.space-around { justify-content: space-around; }


.ml0, .ml1, .ml2, .ml3 { display: inline-block; }
.ml0 { margin-left: .25em; }
.ml1 { margin-left: .5em; }
.ml2 { margin-left: .75em; }
.ml3 { margin-left: 1em; }

.l1 { width: 15vw; height: 5vh; }
.l2 { width: 5vw; height: 5vh;  }
.l3 { font-size: 20px; }

.login_text { color: #c5c5c5; font-size: 3em; }

.center { align-self: center; }
.align-center { text-align: center; }
.centered-block { display: block; margin-bottom: 10px; }


.fullwidth { width: 100%; }
.fullheight { height: 100%; }

.b0 { background: #151515; } .b1 { background: #252525; } .b2 { background: #4c5b61; }
.c0 { color: #eee; } .c1 { color: #c5c5c5; } .c2 { color: #4c5b61; }

.nosel { user-select: none; }
`);

z.Node(document.head, Styles);

export const range = length => [...Array(length).keys()];

export const Segment = (...c) => z.ui.basic.segment(c);
export const Icon = name => z._i.icon({class: name});

export const Button = (text, action, modifiers) => z({
    is: '.ui.button',
    class: modifiers, onclick: action
}, text);

export const Select = (val, placeholder, options) => z({
        is: 'select.ui.selection.dropdown',
        value: val.get, onchange: e => (val.set(e.target.value), z.update()),
        on$created: e => $(e.target).dropdown()
    },
    z._option({disabled: true, selected: true, hidden: true}, placeholder),
    Object.keys(options).map(value => z({is: 'option', value}, value))
);

export const Input = (val, placeholder, modifiers, type = "text") => z({
        is: '.ui.input',
        class: modifiers
    },
    z({
        is: 'input',
        class: modifiers,
        value: val.get, type,
        oninput: (e) => {
            val.set(e.target.value), z.update()
        }, placeholder
    })
);

export const Message = (header, text, modifiers, icon) => {
    z._div.ui.message(
        {class: modifiers},
        icon,
        z._div.header(header),
        z._p(text)
        )
};