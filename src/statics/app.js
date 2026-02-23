const app = document.getElementById("app");
const messagesDiv = document.getElementById("messages");
const input = document.getElementById("input");
const btn = document.getElementById("sendBtn");
const aliasInput = document.getElementById("alias");
const wsStatus = document.getElementById("wsStatus");
const meBadge = document.getElementById("meBadge");
const bottombar = document.getElementById("bottombar");
const aliasWrap = document.getElementById("aliasWrap");

const ALIAS_KEY = "chat_alias_v1";

let ws = null;
let offlineMode = false;

function two(n) {
  return String(n).padStart(2, "0");
}

function nowTime() {
  const d = new Date();
  return two(d.getHours()) + ":" + two(d.getMinutes());
}

function scrollToBottom(instant = false) {
  requestAnimationFrame(() => {
    messagesDiv.scrollTo({
      top: messagesDiv.scrollHeight,
      behavior: instant ? "auto" : "smooth",
    });
  });
}

function setupKeyboardFix() {
  if (!window.visualViewport || !app || !bottombar) return;

  const apply = () => {
    const vv = window.visualViewport;
    app.style.height = vv.height + "px";
    const extra = Math.max(0, window.innerHeight - vv.height - vv.offsetTop);

    bottombar.style.paddingBottom = `calc(10px + env(safe-area-inset-bottom) + ${extra}px)`;
  };

  window.visualViewport.addEventListener("resize", () => {
    apply();
    scrollToBottom(true);
  });

  window.visualViewport.addEventListener("scroll", apply);

  apply();
}

function initAliasUI() {
  const saved = localStorage.getItem(ALIAS_KEY);

  if (saved && saved.trim()) {
    aliasInput.value = saved;
    hideAliasInput();
    meBadge.textContent = "Me: " + saved;
  } else {
    showAliasInput();
    meBadge.textContent = "Me: Unknown";
  }
}

function hideAliasInput() {
  if (!aliasInput) return;
  if (aliasWrap) aliasWrap.style.display = "none";
  else aliasInput.style.display = "none";
}

function showAliasInput() {
  if (!aliasInput) return;
  if (aliasWrap) aliasWrap.style.display = "";
  else aliasInput.style.display = "";
}

function getMyAlias() {
  const saved = localStorage.getItem(ALIAS_KEY);
  if (saved && saved.trim()) return saved.trim();
  return aliasInput.value.trim() || "Unknown";
}

function ensureAliasSavedOnce() {
  const existing = localStorage.getItem(ALIAS_KEY);
  if (existing && existing.trim()) return true;

  const candidate = (aliasInput.value || "").trim();

  if (!candidate) return false;
  if (candidate.length < 2) return false;
  if (candidate.length > 20) return false;

  localStorage.setItem(ALIAS_KEY, candidate);
  meBadge.textContent = "Me: " + candidate;
  hideAliasInput();
  return true;
}

function addMessage(msg) {
  const myAlias = getMyAlias();
  const isMe = (msg.username || "Unknown").trim() === myAlias.trim();

  const row = document.createElement("div");
  row.className = "msg-row " + (isMe ? "me" : "other");

  const bubble = document.createElement("div");
  bubble.className = "msg " + (isMe ? "me" : "other");

  const meta = document.createElement("div");
  meta.className = "meta";

  const user = document.createElement("div");
  user.className = "user";
  user.textContent = msg.username || "Unknown";

  const time = document.createElement("div");
  time.className = "time";
  time.textContent = msg.time || nowTime();

  meta.appendChild(user);
  meta.appendChild(time);

  const text = document.createElement("div");
  text.className = "text";
  text.textContent = msg.content || "";

  bubble.appendChild(meta);
  bubble.appendChild(text);
  row.appendChild(bubble);

  messagesDiv.appendChild(row);
  scrollToBottom();
}

async function loadMessages() {
  try {
    const res = await fetch("/api/messages", { cache: "no-store" });
    if (!res.ok) throw new Error("API not ok");

    const data = await res.json();
    messagesDiv.innerHTML = "";

    (data.messages || []).forEach((m) => {
      addMessage({
        content: m.message ?? m.content ?? "",
        username: m.username ?? "Unknown",
        time: "",
      });
    });

    scrollToBottom(true);
  } catch (err) {
    offlineMode = true;
    wsStatus.textContent = "حالت آفلاین (بدون API)";
    messagesDiv.innerHTML = "";
  }
}

function connectWS() {
  try {
    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${location.host}/ws`);

    ws.onopen = () => {
      offlineMode = false;
      wsStatus.textContent = "آنلاین";
    };

    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        addMessage(data);
      } catch {
        console.error("WS parse error:", e.data);
      }
    };

    ws.onerror = () => {
      offlineMode = true;
      wsStatus.textContent = "WS در دسترس نیست";
    };

    ws.onclose = () => {
      if (!offlineMode) wsStatus.textContent = "قطع شد";
    };
  } catch (e) {
    offlineMode = true;
    wsStatus.textContent = "WS در دسترس نیست";
  }
}

function sendMessage() {
  const text = (input.value || "").trim();
  if (!text) return;

  const ok = ensureAliasSavedOnce();
  if (!ok) {
    alert("نام مستعار معتبر وارد کن (۲ تا ۲۰ کاراکتر)");
    showAliasInput();
    aliasInput.focus();
    return;
  }

  const alias = getMyAlias();
  const msg = { content: text, username: alias, time: nowTime() };

  if (ws && ws.readyState === WebSocket.OPEN && !offlineMode) {
    ws.send(JSON.stringify(msg));
  } else {
    addMessage(msg);
  }

  input.value = "";
  input.focus();
}

window.addEventListener("DOMContentLoaded", async () => {
  setupKeyboardFix();
  initAliasUI();

  if (localStorage.getItem(ALIAS_KEY)) input.focus();

  await loadMessages();
  connectWS();

  btn.addEventListener("click", sendMessage);

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  input.addEventListener("focus", () => scrollToBottom(true));

  if (!localStorage.getItem(ALIAS_KEY)) {
    aliasInput.addEventListener("focus", () => scrollToBottom(true));
    aliasInput.focus();
  }
});
