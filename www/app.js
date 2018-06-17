import z from './lib/zombular.js';
import './lib/jquery-3.3.1.min.js'
import './lib/semantic.min.js';
import {Button, Input, Icon} from './lib/views.js';
import API from './lib/api.js'

let username = z.Val('');
let password = z.Val('');

let load = true;

const centered = (c, styles) => z({is: '.centered-block', style: styles ? styles : ''}, c);
const bg = (c, color) => z._div({style: `background-color: ${color}`}, c);

// TODO: Make popup message for onmessage
const api = new API("ws://panel.sosaki.ru/socket"); // Make WS connection to server

const CPMain = z('');

const LoginPage = z._div['align-center'](
    z._div.center.aligned(
        z._h1.ui.header.center.aligned({style: 'margin-top: 2%; color: #c5c5c5;'}, 'Log in')   ,
        centered(Input(username, 'Login', {large: true})),
        centered(Input(password, 'Password', {large: true}, 'password')),
        centered(Button(
            z('',
                z('.visible.content', 'Login'),
                z('.hidden.content', Icon({'right arrow': true}))
            ),
            () => (load = false, api.login(username.get(), password.get()), z.update()),
            {animated: () => load, medium: true, loading: () => !load}
        )),
    )
);

z.setBody(LoginPage);