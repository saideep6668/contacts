// static/script.js
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const contactCards = document.querySelectorAll(".contact-card");

    searchButton.addEventListener("click", searchContacts);
    searchInput.addEventListener("input", searchContacts);

    function searchContacts() {
        const searchTerm = searchInput.value.trim().toLowerCase();

        contactCards.forEach(function (card) {
            const contactName = card.querySelector(".contact-name").textContent.trim().toLowerCase();
            if (contactName.includes(searchTerm)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }
});















// static/script.js
// document.addEventListener("DOMContentLoaded", function () {
//     const searchInput = document.getElementById("searchInput");
//     const searchButton = document.getElementById("searchButton");

//     searchButton.addEventListener("click", searchContacts);
//     searchInput.addEventListener("keydown", function (event) {
//         if (event.key === "Enter") {
//             searchContacts();
//         }
//     });

//     function searchContacts() {
//         const searchTerm = searchInput.value.toLowerCase();
//         const contactCards = document.querySelectorAll(".contact-card");

//         contactCards.forEach(function (card) {
//             const contactName = card.querySelector(".contact-name").textContent.toLowerCase();
//             if (contactName.includes(searchTerm)) {
//                 card.style.display = "block";
//             } else {
//                 card.style.display = "none";
//             }
//         });
//     }
// });
