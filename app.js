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

const renderCards = items => {
const cards = document.getElementById("cards");
if (!cards) return;
cards.innerHTML = items.map(item => `    <article class="card ${normalizeClass(item.status)}">       <small>${item.id}</small>       <h3>${item.title}</h3>       <div class="rows">
        ${rows(item).map(([k, v]) =>`<div class="row"><span>${k}</span><b>${v}</b></div>`).join("")}       </div>       <div class="status">${item.status}</div>       <p class="questionline">${item.question}</p>     </article>
  `).join("");
};

fetch(location.pathname.includes("/pages/") ? "../data/examples.json" : "data/examples.json")
.then(response => {
if (!response.ok) throw new Error("Failed to load examples");
return response.json();
})
.then(renderCards)
.catch(error => {
const cards = document.getElementById("cards");
if (cards) cards.innerHTML = `<p>${error.message}</p>`;
});

const captureBtn = document.getElementById("captureBtn");
if (captureBtn) {
captureBtn.addEventListener("click", () => {
const actor = document.getElementById("actor").value.trim() || "unknown-actor";
const action = document.getElementById("action").value.trim() || "unknown-action";
const target = document.getElementById("target").value.trim() || "unknown-target";
const frame = {
id: "BCAM-LIVE",
actor,
action,
target,
authority: "unverified",
execution: "not admitted",
evidence: "not recorded",
replay: "unavailable",
recognition: "not accepted",
recourse: "required",
closure: "not closed",
status: "BOUNDARY INCOMPLETE",
question: "What evidence proves this action was authorized before crossing the boundary?"
};
document.getElementById("captureOut").textContent = JSON.stringify(frame, null, 2);
});
}
