import { HOST, PORT } from "../config.js";
export let list_Ticket = []

const ticketItems = document.querySelector('.ticket-list')
const prev_btn = document.getElementById('prev_link')
const next_btn = document.getElementById('next_link')
const number_page = document.querySelector('.number-page')
const license = document.querySelector('.license')
const selectItem = document.querySelector('.select-list')
const timein = document.querySelector('.timein')
const timeout = document.querySelector('.timeout')
const total = document.querySelector('.total')

let perPage = 3
let currentPage = 1
let start = 0
let end = perPage
let totalPages = 0

const ticketsAPI = `http://${HOST}:${PORT}/api/tickets/`

function main() {
    getData(renderTicket)
}
function getData(callback) {
    fetch(ticketsAPI)
        .then(function (response) {
            // console.log(response);
            return response.json()
        })
        .then(function (response) {
            list_Ticket = response
            console.log(list_Ticket);
            totalPages = Math.ceil(list_Ticket.length / perPage)
            renderListPage(totalPages, list_Ticket)
            return response
        })
        .then(callback);
}
function renderTicket(list_Ticket) {
    let check
    let htmls = ''
    const content = list_Ticket.map((ticket, index) => {
        if (index >= start && index < end) {
            if (ticket.ispaid) {
                check = 'checked'
            }
            else {
                check = ''
            }
            if (ticket.timeout == null) {
                ticket.timeout = ""
            }
            if (ticket.total == null) {
                ticket.total = 0
            }
            htmls += `<tr class="h-[80px]">`
            htmls += `<td class="border border-black">${index + 1}</td>`
            htmls += `<td class="border border-black">${ticket.license}</td>`
            htmls += `<td class="border border-black">${ticket.timein}</td>`
            htmls += `<td class="border border-black">${ticket.timeout}</td>`
            htmls += `<td class="border border-black">${ticket.total}</td>`
            htmls += `<td class="border border-black"><input type="checkbox" name="" id="" ${check}></td>`
            htmls += `</tr>`
            return htmls
        }
    })
    ticketItems.innerHTML = htmls
}
function changePage(list_Ticket) {
    const currentNumberPage = document.querySelectorAll('.number-page div')
    for (let i = 0; i < currentNumberPage.length; i++) {
        // console.log(currentNumberPage[i]);
        currentNumberPage[i].addEventListener('click', () => {
            let value = i + 1
            currentPage = value
            $('.number-page div').removeClass('text-white')
            $('.number-page div').removeClass('bg-[#2B3467]')
            currentNumberPage[i].classList.add('text-white')
            currentNumberPage[i].classList.add('bg-[#2B3467]')
            // console.log(currentNumberPage[i]);
            start = (currentPage - 1) * perPage
            end = currentPage * perPage
            // console.log(currentPage);
            next_btn.classList.remove('text-[#ccc]')
            prev_btn.classList.remove('text-[#ccc]')
            if (i == 0) {
                prev_btn.classList.add('text-[#ccc]')
                // next_btn.classList.remove('text-[#ccc]')
                prev_btn.disable = true
            }
            if (i == currentNumberPage.length - 1) {
                next_btn.classList.add('text-[#ccc]')
                // prev_btn.classList.remove('text-[#ccc]')
                next_btn.disable = true
            }
            renderTicket(list_Ticket)

        })
    }
}

function renderListPage(totalPages, list_Ticket) {
    let htmls = ''
    htmls += `<div class="text-white bg-[#2B3467] float-left py-2 px-4 duration-300 border border-[#ddd] mx-1 cursor-pointer">${1}</div>`
    for (let i = 2; i <= totalPages; i++) {
        htmls += `<div class=" float-left py-2 px-4 duration-300 border border-[#ddd] mx-1 cursor-pointer">${i}</div>`
    }
    number_page.innerHTML = htmls
    changePage(list_Ticket)
}
next_btn.addEventListener('click', () => {
    currentPage++

    if (currentPage > totalPages) {
        currentPage = totalPages
    }
    if (currentPage === totalPages) {
        next_btn.classList.add('text-[#ccc]')
    }
    prev_btn.classList.remove('text-[#ccc]')
    $('.number-page div').removeClass('text-white')
    $('.number-page div').removeClass('bg-[#2B3467]')
    $(`.number-page div:eq(${currentPage - 1})`).addClass('text-white')
    $(`.number-page div:eq(${currentPage - 1})`).addClass('bg-[#2B3467]')
    start = (currentPage - 1) * perPage
    end = currentPage * perPage
    renderTicket(list_Ticket)
})
prev_btn.addEventListener('click', () => {
    currentPage--

    if (currentPage < 1) {
        currentPage = 1
    }
    if (currentPage === 1) {
        prev_btn.classList.add('text-[#ccc]')
    }
    next_btn.classList.remove('text-[#ccc]')
    $('.number-page div').removeClass('text-white')
    $('.number-page div').removeClass('bg-[#2B3467]')
    $(`.number-page div:eq(${currentPage - 1})`).addClass('text-white')
    $(`.number-page div:eq(${currentPage - 1})`).addClass('bg-[#2B3467]')
    start = (currentPage - 1) * perPage
    end = currentPage * perPage
    renderTicket(list_Ticket)
})
export function searchTicketListByLicense() {
    // ticketItems.innerHTML = ''
    let tickets = []
    start = 0
    end = perPage
    const select = selectItem.options[selectItem.selectedIndex].innerHTML
    if (license.value != "") {
        if (select == "Paid") {
            tickets = list_Ticket.filter(ticket => ticket.ispaid == true && ticket.license == license.value)
        }
        else if (select == "Not paid") {
            tickets = list_Ticket.filter(ticket => ticket.ispaid == false && ticket.license == license.value)
        }
        else {
            tickets = list_Ticket.filter(ticket => ticket.license == license.value)
        }
    }
    else {
        if (select == "Paid") {
            tickets = list_Ticket.filter(ticket => ticket.ispaid == true)
        }
        else if (select == "Not paid") {
            tickets = list_Ticket.filter(ticket => ticket.ispaid == false)
        }
        else {
            tickets = list_Ticket
        }
    }
    totalPages = Math.ceil(tickets.length / perPage)
    ticketItems.innerHTML = ''
    // console.log(ticketItems.innerHTML);
    renderListPage(totalPages, tickets)
    renderTicket(tickets)
}
export function listDayBetween(startDate, endDate) {
    const datesInRange = [];

    const currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        const dateStr = currentDate.toISOString().slice(0, 10);
        datesInRange.push(dateStr);
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return datesInRange;

}
export function searchTicketListByDateTime() {
    // ticketItems.innerHTML = ''
    let tickets = []
    start = 0
    end = perPage
    // console.log(timein.value.slice(0, -6), timeout.value.slice(0, -6));
    // console.log(listDayBetween(new Date(timein.value.slice(0, -6)), new Date(timeout.value.slice(0, -6))));
    tickets = list_Ticket.filter(ticket => {
        if(listDayBetween(new Date(timein.value), new Date(timeout.value)).includes(ticket.timein.slice(0, -10)) && ticket.ispaid == true) {
            return true
        }
    })
    totalPages = Math.ceil(tickets.length / perPage)
    ticketItems.innerHTML = ''
    console.log(tickets);
    // console.log(ticketItems.innerHTML);
    renderListPage(totalPages, tickets)
    renderTicket(tickets)
    loadRevenues(tickets)
}
function loadRevenues(list_Ticket) {
    let totalSum = 0
    list_Ticket.forEach(ticket => {
        if(ticket.ispaid == true) {
            totalSum += Number.parseInt(ticket.total)
        }
        return totalSum
    })
    console.log(totalSum);
    total.innerHTML = totalSum
}
main()
