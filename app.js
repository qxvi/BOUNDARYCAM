const normalizeClass = status => {
if (status === "CLOSED") return "closed";
if (status === "CONTROLLED") return "controlled";
return "incomplete";
};

const rows = item => [
["Actor", item.actor],
["Action", item.action],
["Target", item.target],
["Authority", item.authority],
["Execution", item.execution],
["Evidence", item.evidence],
["Replay", item.replay],
["Recognition", item.recognition],
["Recourse", item.recourse],
["Closure", item.closure]
];

fetch("data/examples.json")
.then(response => {
if (!response.ok) throw new Error("Failed to load examples");
return response.json();
})
.then(items => {
const cards = document.getElementById("cards");
cards.innerHTML = items.map(item => `      <article class="card ${normalizeClass(item.status)}">         <small>${item.id}</small>         <h3>${item.title}</h3>         <div class="rows">
          ${rows(item).map(([k, v]) =>`<div class="row"><span>${k}</span><b>${v}</b></div>`).join("")}         </div>         <div class="status">${item.status}</div>         <p class="questionline">${item.question}</p>       </article>
    `).join("");
})
.catch(error => {
document.getElementById("cards").innerHTML = `<p>${error.message}</p>`;
});
