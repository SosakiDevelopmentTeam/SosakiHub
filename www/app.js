import z from './lib/zombular.js';
import './lib/jquery-3.3.1.min.js'
import './lib/semantic.min.js';
import {Button, Input, Icon, Message} from './lib/views.js';
import API from './lib/api.js'

let username = z.Val('');
let password = z.Val('');


let message_text = z.Val('');
let message_modifiers = {hidden: true, negative: true}
let message_object = undefined

let load = true;

const centered = (c, styles) => z({is: '.centered-block', style: styles ? styles : ''}, c);
let user_id = undefined;

// TODO: Make popup message for onmessage
const api = new API("ws://panel.sosaki.ru/socket"); // Make WS connection to server

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
        default:
            throw "No such message handle.";

    }

}); // Handler that shows what comes from server!

const CPMain = z('');

const LoginPage = z._div['align-center'](
    z._div.center.aligned(
        z._h1.ui.header.center.aligned({style: 'margin-top: 2%; color: #c5c5c5;'}, 'Log in'),
        centered(z({is: '', on$created: (e) => message_object = e.target}, Message('Notification', message_text, message_modifiers, Icon("close")))),
        centered(Input(username, 'Login', {large: true})),
        centered(Input(password, 'Password', {large: true}, 'password')),
        centered(Button(
            z('',
                z('.visible.content', 'Login'),
                z('.hidden.content', Icon({'right arrow': true}))
            ),
            () => (load = false, api.login(username.get(), password.get(), (data) => {
                switch (data.type) {
                    case 'user_id':
                        z.setBody(CPMain);
                        z.update();
                        break;
                    case 'error':
                        message_text = data.content;
                        message_modifiers.hidden = false;
                        $(message_object).transition("fade in");
                        load = true;
                        z.update();
                        break;
                    default:
                        load = true;
                        z.update();
                        //TODO: Make more handlers
                }
            }), z.update()),
            {animated: () => load, medium: true, loading: () => !load}
        )),
    )
);

z.setBody(LoginPage);