(function () {
  const fields = ["actor", "action", "target", "authority", "execution", "evidence", "replay", "recognition", "recourse", "closure"];
  const output = document.getElementById("frameOutput");
  const status = document.getElementById("consoleStatus");

  function value(id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  function frame() {
    const now = new Date().toISOString();
    return {
      object_type: "BOUNDARYCAM_BOUNDARY_FRAME",
      version: "0.4.0",
      generated_at: now,
      primary_question: "What crossed the boundary?",
      frame_id: "BCAM-" + now.replace(/[-:.TZ]/g, "").slice(0, 14),
      actor: value("actor"),
      action: value("action"),
      target: value("target"),
      authority: value("authority"),
      execution: value("execution"),
      evidence: value("evidence"),
      replay: value("replay"),
      recognition: value("recognition"),
      recourse: value("recourse"),
      closure: value("closure"),
      public_only: true
    };
  }

  function render() {
    if (!output) return;
    output.textContent = JSON.stringify(frame(), null, 2);
    if (status) status.textContent = "Boundary Frame generated.";
  }

  function loadExample() {
    const example = {
      actor: "autonomous.browser.agent",
      action: "submitted a production form",
      target: "external customer-facing web endpoint",
      authority: "user-approved capability admission",
      execution: "HTTP submission completed",
      evidence: "timestamp, request digest, response digest, replay pointer",
      replay: "cold replay available from evidence bundle",
      recognition: "boundary crossing acknowledged",
      recourse: "manual review and rollback path declared",
      closure: "public completion state explicit"
    };
    fields.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.value = example[id];
    });
    render();
  }

  async function copyFrame() {
    render();
    if (!output) return;
    await navigator.clipboard.writeText(output.textContent);
    if (status) status.textContent = "Boundary Frame copied.";
  }

  function downloadFrame() {
    render();
    if (!output) return;
    const blob = new Blob([output.textContent + "\n"], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "boundarycam-frame.json";
    a.click();
    URL.revokeObjectURL(url);
    if (status) status.textContent = "Boundary Frame downloaded.";
  }

  document.getElementById("buildFrame")?.addEventListener("click", render);
  document.getElementById("loadExample")?.addEventListener("click", loadExample);
  document.getElementById("copyFrame")?.addEventListener("click", copyFrame);
  document.getElementById("downloadFrame")?.addEventListener("click", downloadFrame);

  if (output) render();
})();
