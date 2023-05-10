import { HOST, PORT } from "../config.js";

let list_Account = []
const containerForm = document.querySelector('.modal-signin')
const email = document.querySelector('#email')
const password = document.querySelector('#password')

const accountAPI = `http://${HOST}:${PORT}/api/accounts/`

function main() {
    getData()
}
function getData() {
    fetch(accountAPI)
    .then(function (response) {
        return response.json()
    })
    .then(function (response) {
        list_Account = response
        console.log(list_Account);
    })
}

export function openSignInForm() {
    containerForm.classList.remove('hidden')
    containerForm.classList.add('flex')
}

export function closeSignInForm() {
    containerForm.classList.add('hidden')
}
export function submitSignInForm() {
    const account = list_Account.find(acc => acc.email == email.value && acc.password == password.value);
    // console.log(account);
    if (account) {
        localStorage.setItem("currentUser", JSON.stringify(account));
        const currentUser = JSON.parse(localStorage.getItem("currentUser"));
        if (currentUser) {
            window.location.href = ("http://127.0.0.1:5500/server/web/templates/Admin/main.html");
            // window.location.assign("./Admin/main.html");
        }
    } else {
        alert("Tên đăng nhập hoặc mật khẩu không đúng!");
        window.location.href = "http://127.0.0.1:5500/server/web/templates/General/unSign.html";
    }
}
export function signOut() {
    localStorage.removeItem("currentUser")
    window.location.replace("http://127.0.0.1:5500/server/web/templates/General/unSign.html")
}
export function getInfor() {
    const account = JSON.parse(localStorage.getItem("currentUser"))
    // console.log(account);
    return account
}
main()