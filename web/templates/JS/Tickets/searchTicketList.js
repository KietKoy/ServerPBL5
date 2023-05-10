import { searchTicketListByLicense } from "./renderDataTickets.js";

const searchTicket_btn = document.querySelector('.search-ticket_btn')

searchTicket_btn.addEventListener('click', searchTicketListByLicense, (event) => {
    event.preventDefault()
})
