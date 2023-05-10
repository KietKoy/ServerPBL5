import { HOST, PORT } from "../config.js";

let list_Parking = []

const parkingItems = document.querySelector('.parking-list')
const selectItem = document.querySelector('.select-list')

const parkingAPI = `http://${HOST}:${PORT}/api/parkinglots/`


function main() {
    getData(showParkingList)
}
function getData(callback) {
    fetch(parkingAPI)
    .then(function (response) {
        return response.json()
    })
    .then(function (response) {
        list_Parking = response
        return response
    })
    .then(callback)
}
function showParkingList(list_Parking) {
    let color = ''
    let id = 0
    for(let i = 0; i < list_Parking.length; i++) {
        if(list_Parking[i].isfree == true) {
            color = 'EB455F'
        }
        else if(list_Parking[i].isfree == false) {
            color = '32C684'
        }

        id = list_Parking[i].id
        const htmls = `<div class="parking-item w-[150px] h-[200px] bg-[#${color}] rounded-[4px] shadow-lg hover:shadow-xl hover:translate-y-[-4px] duration-300 cursor-pointer flex justify-center items-center text-white text-4xl font-semibold">${id}</div>`
        parkingItems.innerHTML += htmls
    }
}
export function searchParkingList() {
    let color = ''
    let id = 0
    const select = selectItem.options[selectItem.selectedIndex].innerHTML
    let items = []
    if(select === "Empty") {
        items = list_Parking.filter(item => item.isfree == true)
    }
    else if (select === "Full") {
        items = list_Parking.filter(item => item.isfree == false)
    }
    else {
        items = list_Parking
    }
    parkingItems.innerHTML = ''

    for(let i = 0; i < items.length; i++) {
        if(items[i].isfree == true) {
            color = '32C684'
        }
        else if(items[i].isfree == false) {
            color = 'EB455F'
        }
        id = items[i].id
        const htmls = `<div class="parking-item w-[150px] h-[200px] bg-[#${color}] rounded-[4px] shadow-lg hover:shadow-xl hover:translate-y-[-4px] duration-300 cursor-pointer flex justify-center items-center text-white text-4xl font-semibold">${id}</div>`
        parkingItems.innerHTML += htmls
    }
}

main()