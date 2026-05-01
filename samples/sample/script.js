// script.js — Open Library integration (plain JavaScript)
// - Fetch search results from Open Library Search API
// - Render book cards (limit to 12 results)
// - Debounced search input
// - Show modal with additional details (fetch work details if available)
// - Handle missing data safely

const API_SEARCH = 'https://openlibrary.org/search.json';
const COVER_BY_ID = id => `https://covers.openlibrary.org/b/id/${id}-L.jpg`;
const COVER_BY_ISBN = isbn => `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg`;
const PLACEHOLDER = 'https://via.placeholder.com/420x630?text=No+Cover';

const searchInput = document.getElementById('search');
const grid = document.getElementById('booksGrid');
const status = document.getElementById('status');
const modal = document.getElementById('modal');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const modalAuthor = document.getElementById('modal-author');
const modalExtra = document.getElementById('modal-extra');
const modalDesc = document.getElementById('modal-desc');
const yearSpan = document.getElementById('year');

if (yearSpan) yearSpan.textContent = new Date().getFullYear();

// Small debounce helper
function debounce(fn, wait = 300) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

// Normalize Open Library doc to our minimal book object
function normalizeDoc(doc, idx) {
  const title = doc.title || 'Untitled';
  const authors = doc.author_name || [];
  const author = authors.length ? authors.join(', ') : 'Unknown author';
  const first_publish_year = doc.first_publish_year || '';
  const workKey = doc.key || null; // e.g., "/works/OL123W"
  // Choose cover: prefer cover_i, fallback to isbn[0], else placeholder
  let image = PLACEHOLDER;
  if (doc.cover_i) {
    image = COVER_BY_ID(doc.cover_i);
  } else if (doc.isbn && doc.isbn.length) {
    image = COVER_BY_ISBN(doc.isbn[0]);
  }
  // Short description fallback: try first_sentence, subtitle, or snippet
  let short = 'No description available.';
  if (doc.first_sentence) {
    if (typeof doc.first_sentence === 'string') short = doc.first_sentence;
    else if (Array.isArray(doc.first_sentence) && doc.first_sentence.length) short = doc.first_sentence[0];
    else if (doc.first_sentence.value) short = doc.first_sentence.value;
  } else if (doc.subtitle) {
    short = doc.subtitle;
  } else if (doc.text && Array.isArray(doc.text) && doc.text.length) {
    // brief snippet from text field (not ideal but fallback)
    short = doc.text.slice(0,2).join(' ');
  }

  return {
    id: `${doc.key || 'id'}-${idx}`,
    title,
    author,
    authors,
    year: first_publish_year,
    image,
    short,
    workKey
  };
}

// Update status line
function setStatus(message) {
  if (!status) return;
  status.textContent = message;
}

// Fetch search results from Open Library (limit 12)
async function fetchSearch(query) {
  const q = String(query || '').trim();
  if (!q) {
    setStatus('Type a title or author to search books (Open Library)');
    return [];
  }

  setStatus('Searching...');
  const url = `${API_SEARCH}?q=${encodeURIComponent(q)}&limit=12`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data || !Array.isArray(data.docs)) {
      setStatus('No results.');
      return [];
    }
    setStatus(`Showing up to ${data.docs.length} results for "${q}"`);
    return data.docs.map((d, i) => normalizeDoc(d, i));
  } catch (err) {
    console.error('Search error', err);
    setStatus('Error fetching results. Please try again.');
    return [];
  }
}

// Render book cards
function renderBooks(list) {
  grid.innerHTML = '';
  if (!list.length) {
    const e = document.createElement('div');
    e.className = 'empty-message';
    e.textContent = 'No books found.';
    grid.appendChild(e);
    return;
  }

  list.forEach(book => {
    const card = document.createElement('article');
    card.className = 'card';
    card.setAttribute('role', 'listitem');
    card.innerHTML = `
      <div class="card-cover" style="background-image:url('${escapeHtml(book.image)}');" aria-hidden="true"></div>
      <div class="card-body">
        <h3 class="card-title">${escapeHtml(book.title)}</h3>
        <p class="card-author">by ${escapeHtml(book.author)}</p>
        <p class="card-desc">${escapeHtml(book.short)}</p>
        <div class="card-actions">
          <button class="btn" data-action="view" data-work="${escapeHtml(book.workKey || '')}" data-title="${escapeHtml(book.title)}" data-author="${escapeHtml(book.author)}" data-image="${escapeHtml(book.image)}">View Details</button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

// Fetch work details (description) if available
async function fetchWorkDetails(workKey) {
  if (!workKey) return null;
  const url = `https://openlibrary.org${workKey}.json`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Work fetch ${res.status}`);
    const data = await res.json();
    // description can be string or object {value: ''}
    if (data.description) {
      if (typeof data.description === 'string') return data.description;
      if (typeof data.description === 'object' && data.description.value) return data.description.value;
    }
    // sometimes there is a "subtitle" or "excerpt"
    if (data.excerpts && Array.isArray(data.excerpts) && data.excerpts.length) {
      const e = data.excerpts[0];
      if (typeof e === 'string') return e;
      if (e.excerpt) return e.excerpt;
      if (e.comment) return e.comment;
    }
    return null;
  } catch (err) {
    console.warn('Work details fetch failed', err);
    return null;
  }
}

// Open modal with book data; try to fetch work description for fuller details
async function openModalFromButton(btn) {
  const title = btn.dataset.title || 'Untitled';
  const author = btn.dataset.author || 'Unknown author';
  const image = btn.dataset.image || PLACEHOLDER;
  const workKey = btn.dataset.work || '';

  modalImage.src = image;
  modalImage.alt = `Cover of ${title}`;
  modalTitle.textContent = title;
  modalAuthor.textContent = `by ${author}`;
  modalExtra.textContent = ''; // reset
  modalDesc.textContent = 'Loading details…';

  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  // fetch work details (if any)
  if (workKey) {
    const desc = await fetchWorkDetails(workKey);
    if (desc) {
      modalDesc.textContent = desc;
    } else {
      modalDesc.textContent = 'No additional description available.';
    }
  } else {
    modalDesc.textContent = 'No additional description available.';
  }

  // move focus to close button for accessibility
  const closeBtn = modal.querySelector('[data-action="close"]');
  if (closeBtn) closeBtn.focus();
}

// Close modal
function closeModal() {
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  modalImage.src = '';
}

// Utility: escape HTML
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str.replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

// Event delegation for view buttons and modal close
document.addEventListener('click', (e) => {
  const t = e.target;
  if (!t) return;

  // View details
  if (t.matches('[data-action="view"]')) {
    openModalFromButton(t);
    return;
  }

  // Close modal (overlay or button)
  if (t.closest && t.closest('[data-action="close"]')) {
    closeModal();
    return;
  }
});

// Prevent clicks inside modal panel from closing
const modalPanel = modal.querySelector('.modal-panel');
if (modalPanel) {
  modalPanel.addEventListener('click', (e) => e.stopPropagation());
}

// Close modal on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') closeModal();
});

// Main search handler (debounced)
const handleSearch = debounce(async (ev) => {
  const q = ev.target.value || '';
  if (!q.trim()) {
    renderBooks([]); // clear grid
    setStatus('Type a title or author to search books (Open Library)');
    return;
  }

  setStatus('Searching...');
  const results = await fetchSearch(q);
  renderBooks(results);
}, 350);

// Attach handler
searchInput.addEventListener('input', handleSearch);

// Helper to set status text
function setStatus(txt) {
  if (status) status.textContent = txt;
}

/* Initial state: empty grid and instructions */
renderBooks([]);

// Expose fetchSearch for internal use
async function fetchSearch(query) {
  return await fetchSearchInternal(query);
}

// Implementation separation to avoid hoisting confusion
async function fetchSearchInternal(query) {
  const q = String(query || '').trim();
  if (!q) {
    return [];
  }
  const url = `${API_SEARCH}?q=${encodeURIComponent(q)}&limit=12`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data || !Array.isArray(data.docs)) return [];
    return data.docs.map((d, i) => normalizeDoc(d, i));
  } catch (err) {
    console.error('Search failed', err);
    setStatus('Error fetching results. Please try again.');
    return [];
  }
}