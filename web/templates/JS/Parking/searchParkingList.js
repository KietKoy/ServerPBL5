import {searchParkingList} from './index.js'

const searchParking_btn = document.querySelector('.search-packing_btn')

searchParking_btn.addEventListener('click', searchParkingList, (event) => {
    event.preventDefault()
})
