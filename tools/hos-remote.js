/* HOS remote control (inlined into every game by tools/inline_remote.py; edit here, then re-run it).
   ?admin=false (the normal OBS overlay URL) = the clean overlay. It owns all game state.
   ?view=remote = a controller for that overlay: it mirrors the overlay's control panel and forwards
   clicks, typing and keys over a BroadcastChannel. Both pages must run in the same browser profile
   (two windows of one browser, or an OBS dock and an OBS browser source that share storage).
   Nothing runs unless one of those two view modes is in the URL. */
(function () {
  'use strict';
  var qs = new URLSearchParams(location.search);
  var view = qs.get('view');
  var isRemote = view === 'remote';
  var isOverlay = !isRemote && qs.get('admin') === 'false';
  if ((!isRemote && !isOverlay) || typeof BroadcastChannel !== 'function') return;
  var ch = new BroadcastChannel('hos-remote:' + location.pathname.replace(/index\.html$/, ''));
  var panel = function () { return document.getElementById('admin-panel') || document.getElementById('panel'); };
  var pathOf = function (root, el) {
    var p = [];
    while (el && el !== root) {
      var par = el.parentElement;
      if (!par) return null;
      p.unshift(Array.prototype.indexOf.call(par.children, el));
      el = par;
    }
    return el === root ? p : null;
  };
  var atPath = function (root, p) {
    var el = root;
    for (var i = 0; el && p && i < p.length; i++) el = el.children[p[i]];
    return el || null;
  };

  if (isOverlay) {
    var root = panel();
    if (!root) return;
    var timer = 0, remoteSeen = 0, lastStage = '';
    var stageText = function () {
      var own = {};                                            // some games park the panel off-screen: drop its lines
      (root.innerText || '').split('\n').forEach(function (s) { own[s.trim()] = 1; });
      var t = (document.body.innerText || '').split('\n').map(function (s) { return s.trim(); })
        .filter(function (s) { return s && !own[s] && s !== '⚙'; });
      return t.slice(0, 4).join(' · ').slice(0, 160);
    };
    var snap = function () {
      timer = 0;
      if (Date.now() - remoteSeen > 10000) return;            // nobody listening: cost nothing
      var c = root.cloneNode(true);
      var src = root.querySelectorAll('input,textarea,select'), dst = c.querySelectorAll('input,textarea,select');
      for (var i = 0; i < src.length; i++) {
        var s = src[i], d = dst[i];
        if (s.tagName === 'TEXTAREA') d.textContent = s.value;
        else if (s.tagName === 'SELECT') {
          for (var j = 0; j < s.options.length; j++) {
            if (j === s.selectedIndex) d.options[j].setAttribute('selected', ''); else d.options[j].removeAttribute('selected');
          }
        } else if (s.type === 'checkbox' || s.type === 'radio') {
          if (s.checked) d.setAttribute('checked', ''); else d.removeAttribute('checked');
        } else if (s.type !== 'file') d.setAttribute('value', s.value);
      }
      c.querySelectorAll('script,iframe,object,embed').forEach(function (n) { n.remove(); });
      c.querySelectorAll('*').forEach(function (n) {             // markup only: no inline handlers cross over
        for (var k = n.attributes.length - 1; k >= 0; k--) if (/^on/i.test(n.attributes[k].name)) n.removeAttribute(n.attributes[k].name);
      });
      lastStage = stageText();
      ch.postMessage({ t: 'snap', html: c.innerHTML, stage: lastStage });
    };
    var queue = function () { if (!timer) timer = setTimeout(snap, 120); };
    new MutationObserver(queue).observe(root, { subtree: true, childList: true, attributes: true, characterData: true });
    setInterval(function () {                                  // stage line and keepalive
      if (Date.now() - remoteSeen > 10000) return;
      if (stageText() !== lastStage) queue();
    }, 1000);
    setInterval(queue, 3000);
    var fire = function (el, type, init) { el.dispatchEvent(new KeyboardEvent(type, init)); };
    ch.onmessage = function (e) {
      var m = e.data || {};
      if (m.t === 'hello') { remoteSeen = Date.now(); queue(); return; }
      remoteSeen = Date.now();
      if (m.t === 'key') {
        var tgt = (m.path && atPath(root, m.path)) || document.body;
        var init = { key: m.key, code: m.code, shiftKey: !!m.shift, ctrlKey: !!m.ctrl, bubbles: true, cancelable: true };
        fire(tgt, 'keydown', init); fire(tgt, 'keyup', init);
        queue();
        return;
      }
      var el = m.path && atPath(root, m.path);
      if (!el) return;
      if (m.t === 'click') el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
      else if (m.t === 'set') {
        if ('value' in el) el.value = m.value;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        if (m.change) el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      queue();
    };
    return;
  }

  // ---- remote (controller) ----
  // Swap the panel only after the game's own init (DOMContentLoaded/load) has bound its elements.
  if (document.readyState !== 'complete') { window.addEventListener('load', function () { setTimeout(startRemote, 0); }); }
  else setTimeout(startRemote, 0);
  function startRemote() {
  var orig = panel();
  if (!orig) return;
  var host = orig.cloneNode(false);                           // same id/class, so the game's CSS styles it
  orig.remove();
  document.body.appendChild(host);                            // body child: escapes any parent stacking context
  document.documentElement.classList.add('hos-remote');
  var css = document.createElement('style');
  css.textContent =
    '.hos-remote #admin-panel,.hos-remote aside#panel{position:fixed!important;top:44px!important;right:0!important;bottom:0!important;left:auto!important;' +
    'width:min(440px,100vw)!important;max-width:100vw!important;height:auto!important;transform:none!important;display:block!important;' +
    'visibility:visible!important;opacity:1!important;overflow:auto!important;z-index:2147483646!important;margin:0!important}' +
    '#hos-remote-bg{position:fixed;inset:0;z-index:2147483640;background:#0b0b14;color:#cfd0e6;font:15px system-ui,-apple-system,"Segoe UI",sans-serif}' +
    '#hos-remote-bar{position:fixed;top:0;left:0;right:0;height:44px;z-index:2147483647;display:flex;align-items:center;gap:10px;padding:0 14px;' +
    'background:#151527;border-bottom:1px solid #2a2a44;color:#e8e8f6;font:600 14px system-ui,-apple-system,"Segoe UI",sans-serif;white-space:nowrap;overflow:hidden}' +
    '#hos-remote-bar i{width:10px;height:10px;border-radius:50%;background:#e0a030;flex:none}#hos-remote-bar.on i{background:#3ddc84}' +
    '#hos-remote-bar span{overflow:hidden;text-overflow:ellipsis;font-weight:400;color:#b8b9d4}' +
    '#hos-remote-card{position:absolute;top:68px;left:24px;right:calc(min(440px,100vw) + 24px);max-width:560px;line-height:1.5}' +
    '#hos-remote-card h2{margin:0 0 8px;font-size:20px;color:#fff}#hos-remote-card code{background:#22223a;padding:2px 6px;border-radius:4px;word-break:break-all}' +
    '#hos-remote-stage{margin-top:18px;padding:14px;border:1px solid #2a2a44;border-radius:10px;background:#12121f;color:#fff;font-size:18px;min-height:1.5em}';
  document.head.appendChild(css);
  var overlayUrl = location.origin + location.pathname + '?admin=false&bg=transparent';
  var bg = document.createElement('div');
  bg.id = 'hos-remote-bg';
  bg.innerHTML = '<div id="hos-remote-card"><h2>Remote control</h2>' +
    '<div>The game itself runs in your overlay. Point an OBS Browser Source (or a second browser window) at:</div>' +
    '<p><code></code></p><div>Every button you press here happens there. Watch the overlay for the result.</div>' +
    '<div id="hos-remote-stage"></div></div>';
  bg.querySelector('code').textContent = overlayUrl;
  var bar = document.createElement('div');
  bar.id = 'hos-remote-bar';
  bar.innerHTML = '<i></i><b>Remote</b><span></span>';
  document.body.appendChild(bg);
  document.body.appendChild(bar);
  var stageEl = bg.querySelector('#hos-remote-stage'), barText = bar.querySelector('span');
  var lastSnap = 0, lastLocal = 0, lastHtml = '';
  var setStatus = function () {
    var on = Date.now() - lastSnap < 7000;
    bar.classList.toggle('on', on);
    barText.textContent = on ? 'connected to the overlay' : 'waiting for the overlay (open this game with ?admin=false in the same browser or OBS)';
  };
  var render = function (m) {
    lastSnap = Date.now();
    stageEl.textContent = m.stage || '';
    setStatus();
    if (m.html === lastHtml) return;
    lastHtml = m.html;
    var a = document.activeElement, ap = a && host.contains(a) ? pathOf(host, a) : null;
    var av = ap && 'value' in a ? a.value : null, s0 = null, s1 = null;
    try { s0 = a.selectionStart; s1 = a.selectionEnd; } catch (_) {}
    var scrolls = [[[], host.scrollTop]];
    host.querySelectorAll('*').forEach(function (n) { if (n.scrollTop > 0) scrolls.push([pathOf(host, n), n.scrollTop]); });
    host.innerHTML = m.html;
    scrolls.forEach(function (s) { var n = atPath(host, s[0]); if (n) n.scrollTop = s[1]; });
    if (ap) {
      var n = atPath(host, ap);
      if (n && n.tagName === a.tagName) {
        if (av !== null && Date.now() - lastLocal < 400) n.value = av;   // keep what is being typed right now
        n.focus();
        try { if (s0 !== null) n.setSelectionRange(s0, s1); } catch (_) {}
      }
    }
  };
  ch.onmessage = function (e) { var m = e.data || {}; if (m.t === 'snap') render(m); };
  var hello = function () { ch.postMessage({ t: 'hello' }); setStatus(); };
  hello();
  setInterval(hello, 3000);

  var TEXTY = /^(text|search|number|email|url|tel|password|range|color|date|time)$/;
  var isField = function (el) {
    return !!el && (el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || (el.tagName === 'INPUT' && TEXTY.test(el.type || 'text')));
  };
  var send = function (el, msg) {
    var p = pathOf(host, el);
    if (!p) return;
    msg.path = p;
    ch.postMessage(msg);
  };
  var elOf = function (t) { return t && t.nodeType === 1 ? t : t && t.parentElement; };
  // Capture on window runs before the game's own listeners, so nothing executes in this page.
  window.addEventListener('click', function (e) {
    var t = elOf(e.target);
    if (!t || !host.contains(t)) return;
    e.stopImmediatePropagation();
    if (isField(t)) return;                                   // just focusing a field
    e.preventDefault();
    send(t, { t: 'click' });
  }, true);
  window.addEventListener('input', function (e) {
    var t = elOf(e.target);
    if (!host.contains(t) || !isField(t)) return;
    e.stopImmediatePropagation();
    lastLocal = Date.now();
    send(t, { t: 'set', value: t.value });
  }, true);
  window.addEventListener('change', function (e) {
    var t = elOf(e.target);
    if (!host.contains(t) || !isField(t)) return;
    e.stopImmediatePropagation();
    send(t, { t: 'set', value: t.value, change: true });
  }, true);
  window.addEventListener('keydown', function (e) {
    var t = elOf(e.target), inField = host.contains(t) && isField(t);
    e.stopImmediatePropagation();                             // never run this page's own shortcuts
    if (e.key === 'Tab' || e.ctrlKey || e.metaKey || e.altKey) return;
    if (inField && e.key !== 'Enter' && e.key !== 'Escape') return;   // normal typing stays local, sent via input
    if (!inField && (e.key === 'g' || e.key === 'G')) return; // would show the overlay's panel on stream
    if (!inField && e.target === document.body) e.preventDefault();
    if (inField && e.key === 'Enter') lastLocal = 0;          // the overlay usually clears the field: take its value
    ch.postMessage({ t: 'key', key: e.key, code: e.code, shift: e.shiftKey, ctrl: false, path: inField ? pathOf(host, t) : null });
  }, true);
  }
})();
