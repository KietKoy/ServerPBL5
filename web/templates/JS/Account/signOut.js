import { signOut } from "./index.js";

const signOut_btn = document.querySelector('.signout')

signOut_btn.addEventListener('click', signOut, function (event) {
    event.preventDefault();
})