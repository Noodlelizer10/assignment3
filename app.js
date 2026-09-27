const storageKey = "commonplace-posts";
const form = document.querySelector("#post-form");
const textInput = document.querySelector("#post-text");
const characterCount = document.querySelector("#character-count");
const feed = document.querySelector("#feed");
const emptyState = document.querySelector("#empty-state");
const sortButton = document.querySelector("#sort-button");

const starterPosts = [
  { id: "starter-1", author: "Maya Chen", initials: "MC", text: "A reminder that small progress is still progress. Taking the long way today.", createdAt: Date.now() - 1000 * 60 * 18, likes: 12, liked: false },
  { id: "starter-2", author: "Alex Rivera", initials: "AR", text: "Just made the best grilled cheese of my life. The secret was patience.", createdAt: Date.now() - 1000 * 60 * 47, likes: 8, liked: false },
];

let posts = loadPosts();
let newestFirst = true;

function loadPosts() {
  try {
    const savedPosts = JSON.parse(localStorage.getItem(storageKey));
    return Array.isArray(savedPosts) ? savedPosts : starterPosts;
  } catch {
    return starterPosts;
  }
}

function savePosts() {
  localStorage.setItem(storageKey, JSON.stringify(posts));
}

function formatTime(timestamp) {
  const seconds = Math.max(0, Math.floor((Date.now() - timestamp) / 1000));
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function renderPosts() {
  const visiblePosts = [...posts].sort((first, second) => newestFirst
    ? second.createdAt - first.createdAt
    : first.createdAt - second.createdAt);
  feed.innerHTML = "";
  emptyState.hidden = visiblePosts.length > 0;

  visiblePosts.forEach((post, index) => {
    const article = document.createElement("article");
    article.className = "post";
    article.style.animationDelay = `${index * 60}ms`;
    article.innerHTML = `
      <div class="post-meta">
        <div class="avatar">${escapeHtml(post.initials)}</div>
        <div>
          <div class="post-author">${escapeHtml(post.author)}</div>
          <div class="post-time">${formatTime(post.createdAt)}</div>
        </div>
      </div>
      <p class="post-text">${escapeHtml(post.text)}</p>
      <div class="post-actions">
        <button class="action-button ${post.liked ? "liked" : ""}" data-action="like" data-id="${post.id}" type="button">${post.liked ? "Liked" : "Like"} &middot; ${post.likes}</button>
        <button class="action-button" data-action="share" data-id="${post.id}" type="button">Share</button>
      </div>
    `;
    feed.append(article);
  });
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value;
  return element.innerHTML;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = textInput.value.trim();
  if (!text) return;

  posts.unshift({
    id: globalThis.crypto?.randomUUID?.() ?? String(Date.now()),
    author: "Jordan Davis",
    initials: "JD",
    text,
    createdAt: Date.now(),
    likes: 0,
    liked: false,
  });
  savePosts();
  form.reset();
  characterCount.textContent = "0";
  renderPosts();
});

textInput.addEventListener("input", () => {
  characterCount.textContent = textInput.value.length;
});

feed.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const post = posts.find((item) => item.id === button.dataset.id);
  if (!post) return;

  if (button.dataset.action === "like") {
    post.liked = !post.liked;
    post.likes += post.liked ? 1 : -1;
    savePosts();
    renderPosts();
  }

  if (button.dataset.action === "share") {
    const shareText = `${post.author}: ${post.text}`;
    try {
      await navigator.clipboard.writeText(shareText);
      button.textContent = "Copied";
      setTimeout(() => { button.textContent = "Share"; }, 1400);
    } catch {
      button.textContent = "Copy unavailable";
    }
  }
});

sortButton.addEventListener("click", () => {
  newestFirst = !newestFirst;
  sortButton.innerHTML = `${newestFirst ? "Newest" : "Oldest"} <span aria-hidden="true">${newestFirst ? "&#8595;" : "&#8593;"}</span>`;
  renderPosts();
});

renderPosts();
