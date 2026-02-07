/*
 * Client-side verification logic for the Evermore Collective site.
 *
 * This script calculates SHA-256 digests of uploaded files using the
 * Web Crypto API and compares them against a hardcoded registry of
 * known hashes. It also fetches the seal log to display the latest
 * sealed artifacts. Results are displayed in the page without any
 * server interaction.
 */
// Hardcoded registry of known file hashes. Each entry contains the
// recorded filename and its corresponding SHA-256 digest. This list
// should be updated whenever new artifacts are sealed and logged.
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
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
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
        li.textContent = `${entry.seal_id}: ${entry.document} ${entry.version} (${status})`;
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
  const resultPre = document.getElementById('result');
  fileInput.addEventListener('change', async () => {
    const file = fileInput.files[0];
    if (!file) {
      return;
    }
    resultPre.textContent = 'Calculating hash...';
    const digest = await sha256(file);
    // Determine if the hash exists in the registry
    const match = HASH_REGISTRY.find(entry => entry.hash.toLowerCase() === digest.toLowerCase());
    if (match) {
      resultPre.textContent = `VERIFIED\nFile: ${match.filename}\nHash: ${digest}`;
      resultPre.style.color = '#00d4aa';
    } else {
      resultPre.textContent = `NOT FOUND\nHash: ${digest}`;
      resultPre.style.color = '#ff5555';
    }
  });
  loadSealLog();
});
