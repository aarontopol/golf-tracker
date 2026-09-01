/* Crossword Corner — app logic */
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const screens = {
    home: $("screen-home"),
    list: $("screen-list"),
    puzzle: $("screen-puzzle"),
  };
  const ghost = $("ghost-input");
  const DIFF_LABEL = { easy: "Easy", medium: "Medium" };

  // ------------------------------------------------------------------
  // persistence
  // ------------------------------------------------------------------
  const keyFor = (diff, idx) => `xw:${diff}:${idx}`;

  function loadState(diff, idx) {
    try {
      const raw = localStorage.getItem(keyFor(diff, idx));
      if (raw) return JSON.parse(raw);
    } catch (e) { /* corrupted or unavailable — treat as fresh */ }
    return null;
  }

  function saveState(diff, idx, state) {
    try {
      localStorage.setItem(keyFor(diff, idx), JSON.stringify(state));
    } catch (e) { /* storage full/unavailable — play on without saving */ }
  }

  function summarize(diff) {
    const total = PUZZLES[diff].length;
    let done = 0, progress = 0;
    for (let i = 0; i < total; i++) {
      const s = loadState(diff, i);
      if (!s) continue;
      if (s.done) done++;
      else if ((s.l || []).some((ch) => ch)) progress++;
      else if (s.t > 0) progress++;
    }
    return { total, done, progress, fresh: total - done - progress };
  }

  // ------------------------------------------------------------------
  // navigation
  // ------------------------------------------------------------------
  function show(name) {
    for (const k in screens) screens[k].hidden = k !== name;
    stopFireworks();
    window.scrollTo(0, 0);
  }

  function showHome() {
    stopTimer(true);
    for (const diff of ["easy", "medium"]) {
      const s = summarize(diff);
      $("stats-" + diff).innerHTML =
        `<b>${s.done}</b> completed &nbsp;·&nbsp; <b>${s.progress}</b> in progress<br>` +
        `<b>${s.fresh}</b> not started of ${s.total}`;
    }
    show("home");
  }

  function showList(diff) {
    stopTimer(true);
    cur.diff = diff;
    $("list-title").textContent = DIFF_LABEL[diff] + " Puzzles";
    const holder = $("puzzle-grid-list");
    holder.innerHTML = "";
    PUZZLES[diff].forEach((_, i) => {
      const s = loadState(diff, i);
      const tile = document.createElement("button");
      tile.className = "puzzle-tile";
      tile.textContent = i + 1;
      if (s && s.done) {
        tile.classList.add("done");
        const t = document.createElement("span");
        t.className = "tile-time";
        t.textContent = fmtTime(s.dt || s.t || 0);
        tile.appendChild(t);
      } else if (s && ((s.l || []).some((ch) => ch) || s.t > 0)) {
        tile.classList.add("progress");
      }
      tile.addEventListener("click", () => showPuzzle(diff, i));
      holder.appendChild(tile);
    });
    show("list");
  }

  // ------------------------------------------------------------------
  // puzzle model
  // ------------------------------------------------------------------
  const cur = {
    diff: null, idx: null, p: null, size: 0,
    letters: [],          // user letters per cell index (r*size+c), "" empty
    marks: [],            // "" | "wrong" | "revealed"
    entries: [],          // {dir,num,clue,cells:[idx],answer}
    cellEntries: {},      // idx -> {a: entry, d: entry}
    active: null,         // active entry
    activeCell: -1,
    elapsed: 0, done: false,
    interval: null, dirty: false,
  };

  function buildModel(diff, idx) {
    const p = PUZZLES[diff][idx];
    cur.diff = diff; cur.idx = idx; cur.p = p; cur.size = p.s;
    const st = loadState(diff, idx);
    cur.letters = new Array(p.s * p.s).fill("");
    cur.marks = new Array(p.s * p.s).fill("");
    cur.elapsed = 0; cur.done = false;
    if (st) {
      (st.l || []).forEach((ch, i) => { if (ch) cur.letters[i] = ch; });
      (st.m || []).forEach((m, i) => { if (m === "revealed") cur.marks[i] = m; });
      cur.elapsed = st.t || 0;
      cur.done = !!st.done;
      if (cur.done) cur.elapsed = st.dt || st.t || 0;
    }
    cur.entries = [];
    cur.cellEntries = {};
    const addEntries = (list, dir) => {
      for (const [num, r, c, len, clue] of list) {
        const cells = [];
        let answer = "";
        for (let i = 0; i < len; i++) {
          const rr = dir === "a" ? r : r + i;
          const cc = dir === "a" ? c + i : c;
          const ix = rr * p.s + cc;
          cells.push(ix);
          answer += p.g[rr][cc];
        }
        const entry = { dir, num, clue, cells, answer };
        cur.entries.push(entry);
        for (const ix of cells) {
          if (!cur.cellEntries[ix]) cur.cellEntries[ix] = {};
          cur.cellEntries[ix][dir] = entry;
        }
      }
    };
    addEntries(p.a, "a");
    addEntries(p.d, "d");
  }

  function persist() {
    const st = {
      l: cur.letters, t: cur.elapsed, done: cur.done,
      m: cur.marks.map((m) => (m === "revealed" ? m : "")),
    };
    if (cur.done) st.dt = cur.elapsed;
    saveState(cur.diff, cur.idx, st);
    cur.dirty = false;
  }

  const solutionAt = (ix) => {
    const r = Math.floor(ix / cur.size), c = ix % cur.size;
    return cur.p.g[r][c];
  };
  const isOpen = (ix) => solutionAt(ix) !== ".";

  // ------------------------------------------------------------------
  // rendering
  // ------------------------------------------------------------------
  let cellEls = [];

  function renderPuzzle() {
    $("puzzle-title").textContent = `${DIFF_LABEL[cur.diff]} #${cur.idx + 1}`;
    const board = $("board");
    board.innerHTML = "";
    board.style.gridTemplateColumns = `repeat(${cur.size}, 1fr)`;
    cellEls = [];
    const numAt = {};
    for (const [num, r, c] of cur.p.a) numAt[r * cur.size + c] = num;
    for (const [num, r, c] of cur.p.d) numAt[r * cur.size + c] = num;
    for (let ix = 0; ix < cur.size * cur.size; ix++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      if (isOpen(ix)) {
        cell.classList.add("open");
        if (numAt[ix]) {
          const n = document.createElement("span");
          n.className = "num";
          n.textContent = numAt[ix];
          cell.appendChild(n);
        }
        const l = document.createElement("span");
        l.className = "letter";
        cell.appendChild(l);
        cell.addEventListener("pointerdown", (e) => {
          e.preventDefault();
          clickCell(ix);
        });
      }
      board.appendChild(cell);
      cellEls.push(cell);
    }
    renderClues();
    refreshCells();
    // select first across entry (first empty cell if any)
    selectEntry(cur.entries.find((en) => en.dir === "a") || cur.entries[0]);
    updateTimerDisplay();
  }

  function renderClues() {
    for (const [dir, holderId] of [["a", "clues-across"], ["d", "clues-down"]]) {
      const ol = $(holderId);
      ol.innerHTML = "";
      for (const en of cur.entries.filter((e) => e.dir === dir)) {
        const li = document.createElement("li");
        li.innerHTML = `<span class="clue-num">${en.num}</span>${escapeHtml(en.clue)} <span style="color:#9b968f">(${en.answer.length})</span>`;
        li.addEventListener("click", () => selectEntry(en, true));
        en.li = li;
        ol.appendChild(li);
      }
    }
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function refreshCells() {
    for (let ix = 0; ix < cellEls.length; ix++) {
      if (!isOpen(ix)) continue;
      const el = cellEls[ix];
      el.querySelector(".letter").textContent = cur.letters[ix];
      el.classList.toggle("wrong", cur.marks[ix] === "wrong");
      el.classList.toggle("revealed", cur.marks[ix] === "revealed");
      el.classList.remove("sel-word", "sel-cell");
    }
    if (cur.active) {
      for (const ix of cur.active.cells) cellEls[ix].classList.add("sel-word");
    }
    if (cur.activeCell >= 0) cellEls[cur.activeCell].classList.add("sel-cell");
    for (const en of cur.entries) {
      const filled = en.cells.every((ix) => cur.letters[ix]);
      en.li.classList.toggle("solved", filled);
      en.li.classList.toggle("active", en === cur.active);
    }
    updateActiveClueBar();
  }

  function updateActiveClueBar() {
    const bar = $("active-clue");
    if (!cur.active) { bar.textContent = ""; return; }
    const dirName = cur.active.dir === "a" ? "Across" : "Down";
    bar.innerHTML = `<b>${cur.active.num} ${dirName}:</b> ${escapeHtml(cur.active.clue)} (${cur.active.answer.length})`;
  }

  // ------------------------------------------------------------------
  // selection & input
  // ------------------------------------------------------------------
  function clickCell(ix) {
    focusGhost();
    const both = cur.cellEntries[ix] || {};
    if (ix === cur.activeCell) {
      // toggle direction when tapping the same cell
      const otherDir = cur.active && cur.active.dir === "a" ? "d" : "a";
      if (both[otherDir]) cur.active = both[otherDir];
    } else {
      cur.activeCell = ix;
      const prefDir = cur.active ? cur.active.dir : "a";
      cur.active = both[prefDir] || both[prefDir === "a" ? "d" : "a"] || null;
    }
    refreshCells();
  }

  function selectEntry(en, fromClueList) {
    if (!en) return;
    cur.active = en;
    const firstEmpty = en.cells.find((ix) => !cur.letters[ix]);
    cur.activeCell = firstEmpty !== undefined ? firstEmpty : en.cells[0];
    if (fromClueList) focusGhost();
    refreshCells();
  }

  function focusGhost() {
    ghost.value = "";
    ghost.focus({ preventScroll: true });
  }

  function setLetter(ix, ch) {
    if (cur.done) return;
    cur.letters[ix] = ch;
    if (cur.marks[ix] === "wrong") cur.marks[ix] = "";
    cur.dirty = true;
  }

  function advance(step) {
    if (!cur.active) return;
    const pos = cur.active.cells.indexOf(cur.activeCell);
    const next = pos + step;
    if (next >= 0 && next < cur.active.cells.length) {
      cur.activeCell = cur.active.cells[next];
    } else if (step > 0) {
      nextEntry(1);
      return;
    }
    refreshCells();
  }

  function nextEntry(step) {
    if (!cur.active) return;
    const i = cur.entries.indexOf(cur.active);
    const n = cur.entries.length;
    selectEntry(cur.entries[(i + step + n) % n]);
  }

  function typeLetter(ch) {
    if (cur.activeCell < 0 || cur.done) return;
    setLetter(cur.activeCell, ch.toUpperCase());
    // move to next empty cell in the word, else next cell, else next clue
    const cells = cur.active ? cur.active.cells : [cur.activeCell];
    const pos = cells.indexOf(cur.activeCell);
    let moved = false;
    for (let j = pos + 1; j < cells.length; j++) {
      if (!cur.letters[cells[j]]) { cur.activeCell = cells[j]; moved = true; break; }
    }
    if (!moved && pos < cells.length - 1) { cur.activeCell = cells[pos + 1]; moved = true; }
    refreshCells();
    checkWin(false);
    // word finished — hop to the next clue
    if (!moved && !cur.done) nextEntry(1);
  }

  function backspace() {
    if (cur.activeCell < 0 || cur.done) return;
    if (cur.letters[cur.activeCell]) {
      setLetter(cur.activeCell, "");
    } else {
      advance(-1);
      if (cur.activeCell >= 0) setLetter(cur.activeCell, "");
    }
    refreshCells();
  }

  function moveCursor(dr, dc) {
    if (cur.activeCell < 0) return;
    let r = Math.floor(cur.activeCell / cur.size), c = cur.activeCell % cur.size;
    while (true) {
      r += dr; c += dc;
      if (r < 0 || c < 0 || r >= cur.size || c >= cur.size) return;
      const ix = r * cur.size + c;
      if (isOpen(ix)) {
        cur.activeCell = ix;
        const both = cur.cellEntries[ix] || {};
        const prefDir = dr !== 0 ? "d" : "a";
        cur.active = both[prefDir] || both[prefDir === "a" ? "d" : "a"] || cur.active;
        refreshCells();
        return;
      }
    }
  }

  document.addEventListener("keydown", (e) => {
    if (screens.puzzle.hidden || !$("win-modal").hidden) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (/^[a-zA-Z]$/.test(e.key)) { e.preventDefault(); typeLetter(e.key); }
    else if (e.key === "Backspace" || e.key === "Delete") { e.preventDefault(); backspace(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); moveCursor(0, -1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); moveCursor(0, 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); moveCursor(-1, 0); }
    else if (e.key === "ArrowDown") { e.preventDefault(); moveCursor(1, 0); }
    else if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      if (cur.activeCell >= 0) clickCell(cur.activeCell);
    } else if (e.key === "Tab") {
      e.preventDefault();
      nextEntry(e.shiftKey ? -1 : 1);
    }
  });

  // mobile keyboards deliver letters through the hidden input
  ghost.addEventListener("input", () => {
    const v = ghost.value;
    ghost.value = "";
    const ch = v.slice(-1);
    if (/[a-zA-Z]/.test(ch)) typeLetter(ch);
  });

  // ------------------------------------------------------------------
  // check / reveal / clear
  // ------------------------------------------------------------------
  function checkCells(cells) {
    let wrong = 0, blank = 0;
    for (const ix of cells) {
      if (!cur.letters[ix]) { blank++; continue; }
      if (cur.letters[ix] !== solutionAt(ix)) {
        cur.marks[ix] = "wrong";
        wrong++;
      }
    }
    cur.dirty = true;
    refreshCells();
    return { wrong, blank };
  }

  $("btn-check-clue").addEventListener("click", () => {
    if (!cur.active || cur.done) return;
    const { wrong, blank } = checkCells(cur.active.cells);
    if (wrong) toast(`${wrong} letter${wrong > 1 ? "s" : ""} wrong in this clue — marked in red.`);
    else if (blank) toast("No mistakes so far — but the clue isn't finished.");
    else toast("This clue is 100% correct! ✅");
  });

  $("btn-check-puzzle").addEventListener("click", () => {
    if (cur.done) return;
    const cells = [];
    for (let ix = 0; ix < cur.size * cur.size; ix++) if (isOpen(ix)) cells.push(ix);
    const { wrong, blank } = checkCells(cells);
    if (wrong) toast(`${wrong} letter${wrong > 1 ? "s" : ""} wrong — marked in red.`);
    else if (blank) toast(`No mistakes yet! ${blank} square${blank > 1 ? "s" : ""} still empty.`);
    else toast("Everything is correct! 🎉");
  });

  $("btn-reveal-clue").addEventListener("click", () => {
    if (!cur.active || cur.done) return;
    for (const ix of cur.active.cells) {
      if (cur.letters[ix] !== solutionAt(ix)) {
        cur.letters[ix] = solutionAt(ix);
        cur.marks[ix] = "revealed";
      }
    }
    cur.dirty = true;
    refreshCells();
    checkWin(true);
  });

  $("btn-clear").addEventListener("click", () => {
    if (!confirm("Clear all your answers and restart the timer for this puzzle?")) return;
    cur.letters.fill("");
    cur.marks.fill("");
    cur.elapsed = 0;
    cur.done = false;
    persist();
    refreshCells();
    updateTimerDisplay();
    startTimer();
  });

  // ------------------------------------------------------------------
  // completion + fireworks
  // ------------------------------------------------------------------
  function checkWin(announceMistakes) {
    if (cur.done) return;
    let full = true, correct = true;
    for (let ix = 0; ix < cur.size * cur.size; ix++) {
      if (!isOpen(ix)) continue;
      if (!cur.letters[ix]) { full = false; break; }
      if (cur.letters[ix] !== solutionAt(ix)) correct = false;
    }
    if (!full) return;
    if (!correct) {
      if (!checkWin.nagged) {
        checkWin.nagged = true;
        toast("The grid is full, but something's off. Try “Check Puzzle”!");
      }
      return;
    }
    cur.done = true;
    stopTimer(false);
    persist();
    refreshCells();
    $("win-time").innerHTML = `You solved it in <b>${fmtTime(cur.elapsed)}</b>`;
    $("win-modal").hidden = false;
    launchFireworks();
  }

  $("win-list").addEventListener("click", () => {
    $("win-modal").hidden = true;
    showList(cur.diff);
  });
  $("win-next").addEventListener("click", () => {
    $("win-modal").hidden = true;
    const total = PUZZLES[cur.diff].length;
    // next unfinished puzzle after this one (wrapping), else just the next
    let next = (cur.idx + 1) % total;
    for (let k = 0; k < total; k++) {
      const i = (cur.idx + 1 + k) % total;
      const s = loadState(cur.diff, i);
      if (!s || !s.done) { next = i; break; }
    }
    showPuzzle(cur.diff, next);
  });

  // --- fireworks ---
  const fwCanvas = $("fireworks");
  const fwCtx = fwCanvas.getContext("2d");
  let fwParticles = [], fwRunning = false, fwEndAt = 0;

  function stopFireworks() {
    fwRunning = false;
    fwParticles = [];
    fwCanvas.hidden = true;
  }

  function launchFireworks() {
    fwCanvas.width = window.innerWidth;
    fwCanvas.height = window.innerHeight;
    fwCanvas.hidden = false;
    fwParticles = [];
    fwRunning = true;
    fwEndAt = performance.now() + 5200;
    let bursts = 0;
    const burstTimer = setInterval(() => {
      if (bursts++ > 8 || !fwRunning) { clearInterval(burstTimer); return; }
      burst(
        fwCanvas.width * (0.15 + Math.random() * 0.7),
        fwCanvas.height * (0.12 + Math.random() * 0.45)
      );
    }, 420);
    burst(fwCanvas.width / 2, fwCanvas.height / 3);
    requestAnimationFrame(fwFrame);
  }

  function burst(x, y) {
    const hue = Math.floor(Math.random() * 360);
    const n = 70 + Math.floor(Math.random() * 40);
    for (let i = 0; i < n; i++) {
      const angle = (Math.PI * 2 * i) / n + Math.random() * 0.1;
      const speed = 1.5 + Math.random() * 4.5;
      fwParticles.push({
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1,
        decay: 0.008 + Math.random() * 0.012,
        hue: hue + Math.random() * 40 - 20,
      });
    }
  }

  function fwFrame(now) {
    if (!fwRunning) return;
    fwCtx.clearRect(0, 0, fwCanvas.width, fwCanvas.height);
    fwParticles = fwParticles.filter((p) => p.life > 0);
    for (const p of fwParticles) {
      p.x += p.vx; p.y += p.vy;
      p.vy += 0.045; // gravity
      p.vx *= 0.985; p.vy *= 0.985;
      p.life -= p.decay;
      fwCtx.globalAlpha = Math.max(p.life, 0);
      fwCtx.fillStyle = `hsl(${p.hue}, 95%, ${45 + p.life * 25}%)`;
      fwCtx.beginPath();
      fwCtx.arc(p.x, p.y, 2 + p.life * 1.5, 0, Math.PI * 2);
      fwCtx.fill();
    }
    fwCtx.globalAlpha = 1;
    if (now > fwEndAt && fwParticles.length === 0) {
      fwRunning = false;
      fwCanvas.hidden = true;
      return;
    }
    requestAnimationFrame(fwFrame);
  }

  // ------------------------------------------------------------------
  // timer — only runs while the puzzle is on screen AND the tab is visible
  // ------------------------------------------------------------------
  function fmtTime(sec) {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = sec % 60;
    return h
      ? `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`
      : `${m}:${String(s).padStart(2, "0")}`;
  }

  function updateTimerDisplay() {
    $("timer").textContent = fmtTime(cur.elapsed);
    $("timer").classList.toggle("paused", document.hidden && !cur.done);
  }

  function startTimer() {
    stopTicker();
    if (cur.done) return;
    cur.interval = setInterval(() => {
      if (document.hidden || screens.puzzle.hidden || cur.done) return;
      cur.elapsed++;
      cur.dirty = true;
      updateTimerDisplay();
      if (cur.elapsed % 5 === 0) persist();
    }, 1000);
  }

  function stopTicker() {
    if (cur.interval) { clearInterval(cur.interval); cur.interval = null; }
  }

  function stopTimer(save) {
    stopTicker();
    if (save && cur.p && cur.dirty !== undefined) persist();
  }

  document.addEventListener("visibilitychange", () => {
    if (!screens.puzzle.hidden) {
      updateTimerDisplay();
      if (document.hidden) persist();
    }
  });
  window.addEventListener("beforeunload", () => {
    if (!screens.puzzle.hidden && cur.p) persist();
  });

  // ------------------------------------------------------------------
  // toast
  // ------------------------------------------------------------------
  let toastTimeout = null;
  function toast(msg) {
    const t = $("toast");
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => { t.hidden = true; }, 2600);
  }

  // ------------------------------------------------------------------
  // wire-up
  // ------------------------------------------------------------------
  function showPuzzle(diff, idx) {
    stopTimer(true);
    checkWin.nagged = false;
    buildModel(diff, idx);
    renderPuzzle();
    show("puzzle");
    startTimer();
    if (cur.done) {
      $("win-time").innerHTML = `You solved it in <b>${fmtTime(cur.elapsed)}</b>`;
    }
  }

  document.querySelectorAll(".diff-card").forEach((card) =>
    card.addEventListener("click", () => showList(card.dataset.diff))
  );
  $("list-back").addEventListener("click", showHome);
  $("puzzle-back").addEventListener("click", () => showList(cur.diff));

  showHome();
})();
