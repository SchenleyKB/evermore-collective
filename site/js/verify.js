/*
 * Client-side verification logic for the Evermore Collective site.
 *
 * This script calculates SHA-256 digests of uploaded files using the
 * Web Crypto API and compares them against a hardcoded registry of
 * known hashes. It also fetches the seal log to display the latest
 * sealed artifacts. Supports both file input and drag-and-drop.
 */

// Hardcoded registry of known file hashes.
const HASH_REGISTRY = [
  {"filename": "origin_witness_v1.0.0.md", "hash": "04fc9c89ec52a2c890d9abc1e92b41050e1011d5719f5bc1c917251fd092cd74"},
  {"filename": "README.md", "hash": "580e383510a9cc778d82891827e6cd3f977cbbf1456df29c4541a19eed80f8b8"}
];

/**
 * Compute the SHA-256 digest of a File object using the Web Crypto API.
 * @param {File} file - The file to hash.
 * @returns {Promise<string>} A promise that resolves to the hex digest.
 */
async function sha256(file) {
  const buffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Verify a file against the hash registry and display the result.
 * @param {File} file - The file to verify.
 */
async function verifyFile(file) {
  const resultPre = document.getElementById('result');
  resultPre.textContent = 'Calculating hash...';
  resultPre.style.color = '#e0e0e0';
  const digest = await sha256(file);
  const match = HASH_REGISTRY.find(
    entry => entry.hash.toLowerCase() === digest.toLowerCase()
  );
  if (match) {
    resultPre.textContent = 'VERIFIED\nFile: ' + match.filename + '\nHash: ' + digest;
    resultPre.style.color = '#00d4aa';
  } else {
    resultPre.textContent = 'NOT FOUND IN REGISTRY\nFile: ' + file.name + '\nHash: ' + digest;
    resultPre.style.color = '#ff5555';
  }
}

/**
 * Load the seal log from the ledger and populate the seal list.
 */
function loadSealLog() {
  const sealList = document.getElementById('sealList');
  fetch('ledger/seal_log.json')
    .then(response => response.json())
    .then(entries => {
      sealList.innerHTML = '';
      entries.forEach(entry => {
        const li = document.createElement('li');
        const status = entry.blockchain_anchor || 'UNKNOWN';
        li.textContent = entry.seal_id + ': ' + entry.document + ' ' + entry.version + ' (' + status + ')';
        sealList.appendChild(li);
      });
    })
    .catch(() => {
      sealList.innerHTML = '<li>Unable to load seal log.</li>';
    });
}

/**
 * Initialize event listeners once the DOM is ready.
 */
document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('fileInput');
  const dropZone = document.getElementById('dropZone');

  // Standard file input handler
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) verifyFile(file);
  });

  // Drag-and-drop handlers
  if (dropZone) {
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file) verifyFile(file);
    });

    // Clicking the drop zone triggers file input
    dropZone.addEventListener('click', () => {
      fileInput.click();
    });
  }

  loadSealLog();
});
