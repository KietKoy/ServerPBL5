import {getInfor} from './index.js'

const account_name = document.querySelector('.account_name')
account_name.innerHTML = getInfor().name
console.log(account_name, getInfor().name);
