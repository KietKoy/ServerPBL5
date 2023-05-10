import {openSignInForm, closeSignInForm, submitSignInForm, getInfor} from './index.js'

const openSignInForm_btn = document.querySelector('.signin')
const closeSignInForm_btn = document.querySelector('.close-signin-btn')
const submit_btn = document.querySelector('.signIn')

openSignInForm_btn.addEventListener('click', openSignInForm)
closeSignInForm_btn.addEventListener('click', closeSignInForm)
    
submit_btn.addEventListener('click', submitSignInForm, (event) => {
    event.preventDefault();
});




