/* the main js file */
/* BhrisTCG*/
/*
 * This JavaScript file handles page behavior, forms and live UI updates for the BhrisTCG marketplace. It includes:
 * - Navigation interactions (dropdowns, toggles)
 * - Flash message auto-dismissal
 * - Carousel controls for card listings
 * - Search and filter form auto-submission
 * - Cart interactions (add to cart, delivery options)
 * - Real-time chat and notifications via Socket.IO
 * Search and filter interactions here is also inspired by my previous project NZFTC :))))
 */

// ── Nav interactions ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // User dropdown
  const userBtn = document.getElementById('userMenuBtn');
  const userDrop = document.getElementById('userDropdown');
  if (userBtn && userDrop) {
    userBtn.addEventListener('click', e => {
      e.stopPropagation();
      userDrop.classList.toggle('open');
    });
    document.addEventListener('click', () => userDrop.classList.remove('open'));
  }

  // Flash auto-dismiss
  setTimeout(() => {
    document.querySelectorAll('.flash').forEach(f => {
      f.style.transition = 'opacity .3s';
      f.style.opacity = '0';
      setTimeout(() => f.remove(), 300);
    });
  }, 5000);

  // Password toggle visibility
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.input-with-icon').querySelector('input');
      input.type = input.type === 'password' ? 'text' : 'password';
      btn.textContent = input.type === 'password' ? '👁' : '🙈';
    });
  });

  // Carousel arrows
  document.querySelectorAll('.carousel-wrap').forEach(wrap => {
    const carousel = wrap.querySelector('.carousel');
    wrap.querySelector('.carousel-arrow--left')?.addEventListener('click', () => {
      carousel.scrollBy({ left: -340, behavior: 'smooth' });
    });
    wrap.querySelector('.carousel-arrow--right')?.addEventListener('click', () => {
      carousel.scrollBy({ left: 340, behavior: 'smooth' });
    });
  });

  // In-stock toggle
  const inStockToggle = document.getElementById('inStockToggle');
  const inStockInput = document.getElementById('inStockInput');
  if (inStockToggle && inStockInput) {
    inStockToggle.addEventListener('click', () => {
      const active = inStockToggle.classList.toggle('active');
      inStockInput.value = active ? '1' : '';
      document.getElementById('filterForm')?.submit();
    });
  }

  // Filter form auto-submit on dropdown change.
  // This matches the NZFTC-style search/filter behavior by submitting
  // immediately when options change.
  document.querySelectorAll('.filter-auto-submit').forEach(sel => {
    sel.addEventListener('change', () => document.getElementById('filterForm')?.submit());
  });

  // Cart delivery toggle
  const deliveryOptions = document.querySelectorAll('.delivery-option-radio');
  const shippingAddrGroup = document.getElementById('shippingAddressGroup');
  deliveryOptions.forEach(opt => {
    opt.addEventListener('change', () => {
      document.querySelectorAll('.delivery-option').forEach(o => o.classList.remove('selected'));
      opt.closest('.delivery-option')?.classList.add('selected');
      if (shippingAddrGroup) {
        shippingAddrGroup.style.display = opt.value === 'pickup' ? 'none' : 'block';
      }
    });
  });

  // Notification panel
  const notifBtn = document.getElementById('notifBtn');
  const notifPanel = document.getElementById('notifPanel');
  if (notifBtn && notifPanel) {
    notifBtn.addEventListener('click', e => {
      e.stopPropagation();
      notifPanel.classList.toggle('open');
    });
    document.addEventListener('click', () => notifPanel?.classList.remove('open'));
  }
});

// ── CSRF helper ───────────────────────────────────────────────────────────────
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content
      || document.querySelector('input[name="csrf_token"]')?.value || '';
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function showToast(title, body, type = '') {
  const stack = document.getElementById('toastStack');
  if (!stack) return;
  const el = document.createElement('div');
  el.className = `flash flash--${type || 'info'}`;
  el.innerHTML = `<span><strong>${escHtml(title)}</strong>${body ? ' — ' + escHtml(body) : ''}</span><button class="flash__close" onclick="this.parentElement.remove()">×</button>`;
  stack.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 5000);
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

document.addEventListener('click', (event) => {
  const btn = event.target.closest('.js-add-to-cart');
  if (!btn) return;
  event.preventDefault();
  const listingId = btn.dataset.cartId;
  if (listingId) addToCart(listingId);
});

// ── Add to Cart ───────────────────────────────────────────────────────────────
function addToCart(listingId) {
  const btn = document.querySelector(`[data-cart-id="${listingId}"]`);
  if (btn) { btn.disabled = true; btn.textContent = 'Adding…'; }

  const fd = new FormData();
  fd.append('csrf_token', getCsrfToken());

  fetch(`/cart/add/${listingId}`, { method: 'POST', body: fd })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        showToast('Added to cart!', '', 'success');
        if (btn) btn.textContent = '✓ In Cart';
      } else {
        showToast('Error', data.error || 'Could not add to cart.', 'danger');
        if (btn) { btn.disabled = false; btn.textContent = '🛒 Add to Cart'; }
      }
    })
    .catch(() => {
      if (btn) { btn.disabled = false; btn.textContent = '🛒 Add to Cart'; }
    });
}

// ── Price suggestion (live update) ────────────────────────────────────────────
function updatePriceSuggestion(cardId) {
  const cond = document.getElementById('conditionSelect')?.value || 'near_mint';
  fetch(`/api/price-suggestion?card_id=${encodeURIComponent(cardId)}&condition=${cond}`)
    .then(r => r.json())
    .then(data => {
      const el = document.getElementById('suggestedPrice');
      const hint = document.getElementById('priceHint');
      if (el) el.textContent = data.has_data ? `NZ$${data.suggested_price.toFixed(2)}` : 'N/A';
      if (hint) hint.textContent = data.explanation || '';
    });
}

// ── SocketIO ──────────────────────────────────────────────────────────────────
let socket;
function initSocketIO() {
  socket = io({ transports: ['websocket', 'polling'] });
  socket.on('connect', () => console.log('[BhrisTCG] Socket connected'));
  socket.on('new_message', data => {
    showToast(`Message from ${data.sender_username}`, data.body?.slice(0, 60), 'info');
    appendLiveMessage(data, false);
  });
  socket.on('message_sent', data => appendLiveMessage(data, true));
  socket.on('notification', data => {
    showToast(data.title, data.body, 'info');
    updateNotifBadge();
  });
}

function appendLiveMessage(data, isSent) {
  const chat = document.getElementById('chatMessages');
  if (!chat) return;
  const partnerId = chat.dataset.partnerId;
  if (!partnerId) return;
  const otherId = isSent ? data.recipient_id : data.sender_id;
  if (String(otherId) !== String(partnerId)) return;
  const el = document.createElement('div');
  el.className = `msg-bubble ${isSent ? 'msg-bubble--sent' : 'msg-bubble--recv'} fade-up`;
  el.innerHTML = `<div class="msg-bubble__body">${escHtml(data.body)}</div><div class="msg-bubble__time">just now</div>`;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

// ── Chat send ─────────────────────────────────────────────────────────────────
function setupChat(recipientId) {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSendBtn');
  if (!input || !sendBtn) return;

  const doSend = () => {
    const body = input.value.trim();
    if (!body || body.length > 1000) return;
    input.value = '';

    if (socket?.connected) {
      socket.emit('send_message', { recipient_id: recipientId, body });
    } else {
      const fd = new FormData();
      fd.append('recipient_id', recipientId);
      fd.append('body', body);
      fd.append('csrf_token', getCsrfToken());
      fetch('/message/send', { method: 'POST', body: fd })
        .then(r => r.json())
        .then(d => { if (d.message) appendLiveMessage(d.message, true); });
    }
  };

  sendBtn.addEventListener('click', doSend);
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doSend(); } });

  const chat = document.getElementById('chatMessages');
  if (chat) chat.scrollTop = chat.scrollHeight;
}

// ── Notifications ─────────────────────────────────────────────────────────────
function loadNotifications() {
  fetch('/api/notifications')
    .then(r => r.json())
    .then(data => {
      const badge = document.getElementById('bellBadge');
      if (badge && data.unread_count > 0) badge.classList.add('visible');
      renderNotifList(data.notifications);
    })
    .catch(() => {});
}

function updateNotifBadge() {
  const badge = document.getElementById('bellBadge');
  if (badge) badge.classList.add('visible');
}

function renderNotifList(notifs) {
  const list = document.getElementById('notifList');
  if (!list || !notifs?.length) return;
  list.innerHTML = notifs.map(n => `
    <div class="convo-item ${n.is_read ? '' : 'active'}" style="cursor:${n.link?'pointer':'default'}"
         onclick="${n.link ? `window.location='${n.link}'` : ''}">
      <div class="convo-item__content">
        <div class="convo-item__name">${escHtml(n.title)}</div>
        ${n.body ? `<div class="convo-item__preview">${escHtml(n.body)}</div>` : ''}
      </div>
    </div>
  `).join('');
}

function markNotifsRead() {
  fetch('/api/notifications/read', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrfToken() }
  });
  document.getElementById('bellBadge')?.classList.remove('visible');
}
