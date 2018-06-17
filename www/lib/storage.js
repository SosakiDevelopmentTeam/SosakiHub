export function get(name) {
    return sessionStorage[name];
}

export function set(name, value) {
    sessionStorage[name] = value;
}

export const remove = (name) => delete sessionStorage[name];