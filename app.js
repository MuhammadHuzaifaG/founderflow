const API_BASE = "https://founderflow1.vercel.app/";

const form = document.getElementById("taskForm");
const resultBox = document.getElementById("result");
const loading = document.getElementById("loading");
const historyList = document.getElementById("historyList");
const healthButton = document.getElementById("healthButton");
const notesBlock = document.getElementById("notesBlock");
const notesForm = document.getElementById("notesForm");
const notesList = document.getElementById("notesList");
const noteTitle = document.getElementById("noteTitle");
const noteBody = document.getElementById("noteBody");
const decisionFlag = document.getElementById("decisionFlag");

let currentTaskId = null;

async function getHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();
    alert(`Service status: ${data.status}`);
  } catch (error) {
    alert("API is not reachable. Check Vercel deployment.");
  }
}

async function loadHistory() {
  try {
    const response = await fetch(`${API_BASE}/history`);
    const tasks = await response.json();

    historyList.innerHTML = "";

    if (!tasks.length) {
      historyList.innerHTML = "<li>No saved founder tasks yet.</li>";
      return;
    }

    tasks.forEach((task) => {
      const item = document.createElement("li");
      const createdAt = new Date(task.created_at).toLocaleString();

      item.innerHTML = `
        <div class="history-item">
          <strong>${task.company_name}</strong>
          <span>${task.task_type}</span>
          <small>${createdAt}</small>
          <p>${task.summary}</p>
        </div>
      `;
      item.addEventListener("click", async () => {
        currentTaskId = task.id;
        await loadNotes(task.id);
      });
      historyList.appendChild(item);
    });
  } catch (error) {
    historyList.innerHTML = "<li>History not available right now.</li>";
  }
}

async function loadNotes(taskId) {
  if (!taskId) return;

  notesBlock.classList.remove("hidden");
  notesList.innerHTML = "<li>Loading notes...</li>";

  try {
    const response = await fetch(`${API_BASE}/notes/${taskId}`);
    const data = await response.json();

    notesList.innerHTML = "";

    if (!data.length) {
      notesList.innerHTML = "<li>No notes yet. Save a founder decision or observation.</li>";
      return;
    }

    data.forEach((note) => {
      const item = document.createElement("li");
      item.className = note.decision_flag ? "note note-decision" : "note";
      item.innerHTML = `
        <strong>${note.note_title}</strong>
        <span>${note.decision_flag ? "Decision" : "Note"}</span>
        <p>${note.note_body}</p>
      `;
      notesList.appendChild(item);
    });
  } catch (error) {
    notesList.innerHTML = "<li>Unable to load notes right now.</li>";
  }
}

function renderLeadCards(leadData) {
  if (!leadData || !leadData.opportunity_cards) return "";

  const cards = leadData.opportunity_cards.map((card) => `
    <div class="lead-card">
      <div class="lead-head">
        <strong>${card.name}</strong>
        <span class="score-pill">${card.score}/100</span>
      </div>
      <p><span class="label">Segment:</span> ${card.segment}</p>
      <p><span class="label">Urgency:</span> ${card.urgency} / Fit: ${card.fit} / Access: ${card.access}</p>
      <p>${card.reason}</p>
      <p><span class="label">Next step:</span> ${card.next_step}</p>
    </div>
  `).join("");

  return `
    <div class="lead-section">
      <h3>Lead generation opportunities</h3>
      <p>${leadData.summary}</p>
      <div class="lead-grid">${cards}</div>
      <p class="decision-prompt"><strong>Founder decision prompt:</strong> ${leadData.founder_decision_prompt}</p>
    </div>
  `;
}

function renderDecisionChecklist(workflow) {
  const steps = (workflow.steps || [])
    .map((step) => `<li><strong>${step.name}</strong>: ${step.goal}</li>`)
    .join("");

  const checkpoints = (workflow.decision_checkpoints || [])
    .map((cp) => `<li><strong>${cp.stage}</strong> — ${cp.question}</li>`)
    .join("");

  return `
    <div class="decision-box">
      <h3>Workflow steps</h3>
      <ul>${steps}</ul>

      <h3>Decision checkpoints</h3>
      <ul>${checkpoints}</ul>
    </div>
  `;
}

async function exportSummary() {
  if (!currentTaskId) return;

  try {
    const response = await fetch(`${API_BASE}/export/${currentTaskId}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Export failed");
    }

    const blob = new Blob([data.content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = data.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

  } catch (error) {
    alert(error.message);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  loading.classList.remove("hidden");
  resultBox.innerHTML = "<p class='placeholder'>Generating workflow output...</p>";

  const payload = {
    task_type: document.getElementById("taskType").value,
    company_name: document.getElementById("companyName").value,
    market: document.getElementById("market").value,
    founder_goal: document.getElementById("founderGoal").value,
    context: document.getElementById("context").value,
    output_length: 700
  };

  try {
    const response = await fetch(`${API_BASE}/task`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Unknown server error");

    currentTaskId = data.id;

    const workflow = data.workflow || {};
    const findings = (data.findings || []).map((item) => `<li>${item}</li>`).join("");
    const actions = (data.recommended_next_steps || []).map((item) => `<li>${item}</li>`).join("");

    resultBox.innerHTML = `
      <div>
        <div class="status-row">
          <span class="badge">${workflow.workflow_name || data.task_type}</span>
          <span class="confidence">Confidence: ${data.confidence}</span>
        </div>

        <h3>Summary</h3>
        <p>${data.summary}</p>

        ${renderDecisionChecklist(workflow)}

        <h3>Key findings</h3>
        <ul>${findings}</ul>

        <h3>Recommended next steps</h3>
        <ul>${actions}</ul>

        ${renderLeadCards(data.lead_generation)}

        <p><strong>Human judgment required:</strong> Yes</p>
        <p class="muted">${workflow.validation_summary || "The founder must confirm the key assumptions before moving forward."}</p>
      </div>
    `;

    notesBlock.classList.remove("hidden");
    await loadNotes(currentTaskId);
    await loadHistory();

  } catch (error) {
    resultBox.innerHTML = `
      <p class="placeholder">
        Error while generating workflow output: ${error.message}
      </p>
    `;
  } finally {
    loading.classList.add("hidden");
  }
});

notesForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!currentTaskId) {
    alert("Generate or select a task first.");
    return;
  }

  const title = noteTitle.value.trim();
  const body = noteBody.value.trim();

  if (!title || !body) {
    alert("Please add a note title and body.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        task_id: currentTaskId,
        note_title: title,
        note_body: body,
        decision_flag: decisionFlag.checked
      })
    });

    if (!response.ok) throw new Error("Unable to save note");

    notesForm.reset();
    await loadNotes(currentTaskId);

  } catch (error) {
    alert(error.message);
  }
});

healthButton.addEventListener("click", getHealth);
document.addEventListener("DOMContentLoaded", () => {
  loadHistory();
});
