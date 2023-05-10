import { searchTicketListByDateTime } from "../Tickets/renderDataTickets.js";

const searchTicket_btn = document.querySelector('.search-ticket_btn')

searchTicket_btn.addEventListener('click', searchTicketListByDateTime, (event) => {
    event.preventDefault()
})
