const input = document.getElementById("search");
const suggestionsList = document.getElementById("suggestions");
const resultDiv = document.getElementById("result");
const dialectSelect = document.getElementById("dialectSelect");

let suggestions = [];
let selectedIndex = -1;

input.addEventListener("input", async () => {
  const q = input.value.trim();
  if (!q) {
    suggestions = [];
    selectedIndex = -1;
    suggestionsList.innerHTML = "";
    input.classList.add("no-suggestions");
    return;
  }

  const res = await fetch(`/api/suggest?q=${encodeURIComponent(q)}`);
  suggestions = await res.json();
  selectedIndex = -1;
  renderSuggestions();
});

input.addEventListener("keydown", async (e) => {
  if (e.key === "ArrowDown") {
    e.preventDefault();
    if (suggestions.length > 0) {
      selectedIndex = (selectedIndex + 1) % suggestions.length;
      renderSuggestions();
    }
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    if (suggestions.length > 0) {
      selectedIndex = (selectedIndex - 1 + suggestions.length) % suggestions.length;
      renderSuggestions();
    }
  } else if (e.key === "Enter") {
    e.preventDefault();
    const word = selectedIndex >= 0 ? suggestions[selectedIndex] : input.value.trim();
    if (word) {
      suggestionsList.innerHTML = "";
      input.classList.add("no-suggestions");
      await getWordInfo(word);
    }
  }
});

suggestionsList.addEventListener("click", (e) => {
  if (e.target.tagName === "LI") {
    input.value = e.target.textContent;
    suggestionsList.innerHTML = "";
    input.classList.add("no-suggestions");
    getWordInfo(e.target.textContent);
  } else if (e.key === "Escape") {
    selectedIndex = -1;
    suggestionsList.innerHTML = "";
    input.classList.add("no-suggestions");
    // Optional: set input.value = previousTypedValue if you saved it
  }
});

function renderSuggestions() {
  suggestionsList.innerHTML = "";
  
  if (suggestions.length === 0) {
    input.classList.add("no-suggestions");
    return;
  }
  
  input.classList.remove("no-suggestions");
  
  suggestions.forEach((word, i) => {
    const li = document.createElement("li");
    li.textContent = word;
    if (i === selectedIndex) {
      li.classList.add("highlight");
      input.value = word; // 👈 this keeps input synced with highlighted suggestion
    }
    suggestionsList.appendChild(li);
  });
}


async function getWordInfo(word) {
  const res = await fetch(`/api/word/${encodeURIComponent(word)}`);
  const data = await res.json();
  console.log(`/api/word/${word} response:`, data);
  
  // Get selected dialect
  const selectedDialect = dialectSelect.value;
  const ipa = (data.ipa && data.ipa[selectedDialect]) ? data.ipa[selectedDialect] : "[No IPA available for selected dialect]";

  if (!data.examples || !data.examples.length) {
    resultDiv.innerHTML = `
      <h2>${data.word}</h2>
      <p><strong>IPA:</strong> ${ipa}</p>
      <p>No audio examples available.</p>
    `;
    return;
  }

  let selectedExample = Math.floor(Math.random() * data.examples.length);
  const dropdown = data.examples.map((ex, i) =>
    `<option value="${i}" ${i === selectedExample ? "selected" : ""}>Example ${i + 1} (${ex.dialect})</option>`
  ).join("");
  const selected = data.examples[selectedExample];

  resultDiv.innerHTML = `
    <h2>${data.word}</h2>
    <p><strong>IPA:</strong> ${ipa}</p>

    <label for="exampleSelect">Choose Example:</label>
    <select id="exampleSelect">${dropdown}</select>

    <p id="sentence">${selected.sentence}</p>
    <audio id="audioEl" src="${selected.audio}" controls preload="metadata">
      Your browser does not support the audio element.
    </audio>
  `;

  const select = document.getElementById("exampleSelect");
  const sentence = document.getElementById("sentence");
  const audioEl = document.getElementById("audioEl");

  select.addEventListener("change", () => {
    const newExample = data.examples[parseInt(select.value)];
    sentence.textContent = newExample.sentence;
    audioEl.src = newExample.audio;
  });
}

// Helper function to get readable dialect names
function getDialectDisplayName(dialectKey) {
  const dialectNames = {
    'e_written': 'Eastern (Written)',
    'e_spoken': 'Eastern (Spoken)',
    'n_written': 'Northern (Written)', 
    'n_spoken': 'Northern (Spoken)',
    'sw_written': 'South-Western (Written)',
    'sw_spoken': 'South-Western (Spoken)',
    't_written': 'Trøndelag (Written)',
    't_spoken': 'Trøndelag (Spoken)',
    'w_written': 'Western (Written)',
    'w_spoken': 'Western (Spoken)'
  };
  return dialectNames[dialectKey] || dialectKey;
}

// Add event listener for dialect changes to update current word
dialectSelect.addEventListener("change", () => {
  const currentWord = resultDiv.querySelector('h2');
  if (currentWord) {
    getWordInfo(currentWord.textContent);
  }
});
