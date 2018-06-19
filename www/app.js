import z from './lib/zombular.js';
import './lib/jquery-3.3.1.min.js'
import './lib/semantic.min.js';
import {Button, Input, Icon, Message, Sidebar} from './lib/views.js';
import API from './lib/api.js'
import {set, remove} from './lib/storage.js'
import Chart from "./lib/Chart.bundle.min.js"



let username = z.Val('');
let password = z.Val('');


let message_text = z.Val('');
let message_modifiers = {hidden: true, negative: true, compact: true};
let message_object = undefined;

let button_load = true;

const centered = (c, styles) => z({is: '.centered-block', style: styles ? styles : ''}, c);
let user_id = undefined;
let login_form = undefined;
let button_object = undefined;
let loading_object = undefined;
let sidebar_object = undefined;
let target_page = undefined;
let loading = true;
const api = new API(`${location.protocol === 'https:' ? 'wss': ws}://panel.sosaki.ru/socket`); // Make WS connection to server

api.onmessage((msg) => {
    let data = JSON.parse(msg.data);
    switch (data.type) {
        case "user_id":
            user_id = data['user_id'];
        case "message":
        case "error":
            if ('cb_id' in data)
                api._call_cb(data['cb_id'], data);
            break;
        case "session_expired":
            remove('session');
            break;
        default:
            throw "No such message handle.";

    }

}); // Handler that shows what comes from server!

api.onopen(() => {
        let transit = (t) => $(loading_object).transition({
            animation: "fade",
            onStart: () => (target_page = t),
            onComplete: () => (loading = false, z.update())
        });

        api.check_auth((data) => (console.log("called"), data.type === "user_id" ? transit(CPMain) : transit(LoginPage)));
    }
);


function logged_cb(data) {
    switch (data.type) {
        case 'user_id':
            set('session', data.session);
            $(login_form).transition({
                animation: "horizontal flip",
                onComplete: () => z.setBody(CPMain)
            });
            break;
        case 'error':
            message_text.set(data.content);
            message_modifiers.hidden = false;
            $(message_object).transition("fade in");
            $(login_form).transition("shake");
            button_load = true;
            z.update();
            break;
        default:
            button_load = true;
            z.update();
        //TODO: Make more handlers

    }
}

function button_work() {
    button_load = false;
    api.login(username.get(), password.get(), logged_cb);
    z.update();
}

let login_form_enter = (e) => {
    login_form = e.target;
    e.target.addEventListener("keyup", function (event) {
        event.preventDefault();
        if (event.keyCode === 13)
            button_work();
    });
};

let chart_object = undefined;
let created_chart = undefined;
let create_chart = (objects) => {
    created_chart = c3.generate({
        bindto: chart_object,
        data: objects
    })
};

const CPMain = z('',
    z._div.pusher(
        z._div({on$created: (e) => chart_object = e.target})
    ),
    Sidebar(z.ui.logo("Simple header"),
        [
            {name: 'Add', icon: Icon("plus green")}
        ],
        {
            class: {vertical: true, visible: true, menu: true},
            on$created: e => (sidebar_object = e.target, $(sidebar_object).sidebar("setting", "transition", "scale down"))
        }
    )
);

const LoginPage = z._div['align-center']({style: "display: flex; height: 100%; justify-content: center;"},
    z({is: "form.center.aligned", on$created: login_form_enter},
        z._h1.ui.header.center.aligned({style: 'margin-top: 2%; color: #c5c5c5;'}, 'Log in'),
        centered(z({
            is: '',
            on$created: (e) => message_object = e.target
        }, Message('Notification', message_text, message_modifiers, Icon("close", () => $(message_object).transition("fade out"))))),
        centered(Input(username, 'Login', {large: true})),
        centered(Input(password, 'Password', {large: true}, 'password')),
        centered(Button(
            z('',
                z('.visible.content', 'Login'),
                z('.hidden.content', Icon({'right arrow': true}))
            ),
            button_work,
            {animated: () => button_load, medium: true, loading: () => !button_load})
        )
    )
);

const Loading = z._div({on$created: (e) => loading_object = e.target, style: "width: 100%; height: 100%; "},
    z._div.ui.active.dimmer(
        z._div.ui.text.loader("Loading"),
        z._p()
    )
);

const Body = z('',
    () => loading ? Loading : undefined,
    () => target_page
);

z.setBody(Body);