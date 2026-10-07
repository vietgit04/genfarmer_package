(function(){
  "use strict";

  /* PAGES, TABOF, LANGS, DEFAULT_LANG, STR, DOC_TITLE and IMGS are injected by build.py */
  var root = document.documentElement;
  var lang = DEFAULT_LANG;

  /* ---------- images: assign only when a page is shown ---------- */
  function paintImages(scope){
    var els = scope.querySelectorAll("img[data-img]");
    for (var i = 0; i < els.length; i++) {
      var k = els[i].getAttribute("data-img");
      if (IMGS[k] && els[i].getAttribute("src") !== IMGS[k]) els[i].src = IMGS[k];
    }
  }
  paintImages(document.querySelector(".hdr"));
  paintImages(document.querySelector(".side"));

  /* ---------- theme ---------- */
  var sun = document.querySelector("#themeBtn .ic-sun");
  var moon = document.querySelector("#themeBtn .ic-moon");
  function paintTheme(){
    var dark = root.getAttribute("data-theme") !== "light";
    sun.hidden = !dark;
    moon.hidden = dark;
  }
  try{
    var saved = localStorage.getItem("gf-theme");
    if(saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  }catch(e){}
  paintTheme();
  document.getElementById("themeBtn").addEventListener("click", function(){
    var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try{ localStorage.setItem("gf-theme", next); }catch(e){}
    paintTheme();
  });

  /* ---------- mobile drawer ---------- */
  var scrim = document.getElementById("scrim");
  function closeNav(){ document.body.classList.remove("nav-open"); }
  document.getElementById("burger").addEventListener("click", function(){ document.body.classList.toggle("nav-open"); });
  scrim.addEventListener("click", closeNav);

  /* ---------- language ---------- */
  var langBtn = document.getElementById("langBtn");
  var langMenu = document.getElementById("langMenu");
  function paintLang(){
    root.setAttribute("lang", lang);
    Array.prototype.forEach.call(document.querySelectorAll("[data-l]"), function(el){
      el.hidden = el.getAttribute("data-l") !== lang;
    });
    Array.prototype.forEach.call(langMenu.querySelectorAll("[data-set-lang]"), function(b){
      b.setAttribute("aria-checked", b.getAttribute("data-set-lang") === lang ? "true" : "false");
    });
    document.getElementById("langCode").textContent = lang.toUpperCase();
    q.placeholder = STR.search_ph[lang];
    ["burger","themeBtn","langBtn"].forEach(function(id){
      document.getElementById(id).setAttribute("aria-label", STR[id][lang]);
    });
  }
  function setLang(next){
    if(LANGS.indexOf(next) === -1 || next === lang) return;
    lang = next;
    try{ localStorage.setItem("gf-lang", lang); }catch(e){}
    var r = parseHash();
    location.hash = "#/" + lang + "/" + r.id + (r.anchor ? "/" + r.anchor : "");
  }
  function closeLangMenu(){ langMenu.hidden = true; langBtn.setAttribute("aria-expanded", "false"); }
  langBtn.addEventListener("click", function(e){
    e.stopPropagation();
    var open = langMenu.hidden;
    langMenu.hidden = !open;
    langBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  langMenu.addEventListener("click", function(e){
    var b = e.target.closest("[data-set-lang]");
    if(!b) return;
    closeLangMenu();
    setLang(b.getAttribute("data-set-lang"));
  });
  document.addEventListener("click", function(e){ if(!langMenu.hidden && !e.target.closest(".langwrap")) closeLangMenu(); });

  /* ---------- toc ---------- */
  var tocList = document.getElementById("tocList");
  var tocHead = document.querySelector(".toc-h");
  var tocLinks = [];
  function buildToc(page){
    tocList.innerHTML = "";
    tocLinks = [];
    var hs = page.querySelectorAll(".doc h2[id]");
    tocHead.hidden = hs.length === 0;
    Array.prototype.forEach.call(hs, function(h){
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      a.addEventListener("click", function(ev){
        ev.preventDefault();
        h.scrollIntoView({behavior:"smooth", block:"start"});
      });
      tocList.appendChild(a);
      tocLinks.push({a:a, h:h});
    });
    spy();
  }
  function spy(){
    if(!tocLinks.length) return;
    var best = 0;
    for(var i=0;i<tocLinks.length;i++){
      if(tocLinks[i].h.getBoundingClientRect().top <= 140) best = i;
    }
    for(var j=0;j<tocLinks.length;j++) tocLinks[j].a.classList.toggle("on", j === best);
  }
  var ticking = false;
  window.addEventListener("scroll", function(){
    if(ticking) return;
    ticking = true;
    requestAnimationFrame(function(){ spy(); ticking = false; });
  }, {passive:true});

  /* ---------- router: #/[lang/]page[/anchor] ---------- */
  function parseHash(){
    var segs = (location.hash || "").replace(/^#\/?/, "").split("/").filter(Boolean);
    var l = null;
    if(segs.length && LANGS.indexOf(segs[0]) !== -1) l = segs.shift();
    var id = (segs[0] || "home").toLowerCase();
    if(PAGES.indexOf(id) === -1) id = "home";
    return {lang:l, id:id, anchor:segs[1] || ""};
  }
  var shown = null;
  function route(){
    var r = parseHash();
    if(r.lang) lang = r.lang;
    paintLang();
    var active = document.getElementById("p-" + lang + "-" + r.id);
    if(shown && shown !== active) shown.hidden = true;
    active.hidden = false;
    paintImages(active);
    Array.prototype.forEach.call(document.querySelectorAll(".nav-a[data-nav]"), function(a){
      a.classList.toggle("on", a.getAttribute("data-nav") === r.id);
    });
    var tab = TABOF[r.id] || "start";
    Array.prototype.forEach.call(document.querySelectorAll(".tab-l"), function(t){
      t.classList.toggle("on", t.getAttribute("data-tab") === tab);
    });
    buildToc(active);
    document.title = active.getAttribute("data-title") + " | " + DOC_TITLE[lang];
    closeNav();
    var target = r.anchor ? document.getElementById(lang + "--" + r.id + "--" + r.anchor) : null;
    if(target){
      requestAnimationFrame(function(){ target.scrollIntoView({block:"start"}); spy(); });
    }else if(shown !== active || !r.anchor){
      window.scrollTo(0, 0);
    }
    shown = active;
    if(index.lang !== lang) index = {lang:null, items:[]};
  }
  window.addEventListener("hashchange", route);

  /* ---------- search (index built per language, on first use) ---------- */
  var index = {lang:null, items:[]};
  function buildIndex(){
    var items = [];
    PAGES.forEach(function(p){
      var el = document.getElementById("p-" + lang + "-" + p);
      if(!el) return;
      var title = el.getAttribute("data-title");
      var crumb = el.getAttribute("data-crumb");
      var doc = el.querySelector(".doc");
      var lede = el.querySelector(".lede");
      items.push({href:"#/" + p, title:title, path:crumb,
        text:((lede ? lede.textContent : "") + " " + (doc ? doc.textContent : "")).replace(/\s+/g," ").trim()});
      if(doc){
        Array.prototype.forEach.call(doc.querySelectorAll("h2[id]"), function(h){
          var buf = [];
          var n = h.nextElementSibling;
          while(n && n.tagName !== "H2"){ buf.push(n.textContent); n = n.nextElementSibling; }
          items.push({href:"#/" + p + "/" + h.id.split("--")[2], title:h.textContent, path:crumb + " · " + title,
            text:buf.join(" ").replace(/\s+/g," ").trim()});
        });
      }
    });
    index = {lang:lang, items:items};
  }
  function fold(s){ return s.toLowerCase().normalize("NFD").replace(/[̀-゙゚ͯ]/g, "").replace(/đ/g, "d"); }

  var ovl = document.getElementById("ovl");
  var q = document.getElementById("q");
  var results = document.getElementById("results");
  var sel = 0;

  function esc(s){ return s.replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); }
  function hl(s, term){
    if(!term) return esc(s);
    var i = fold(s).indexOf(term);
    if(i === -1) return esc(s);
    return esc(s.slice(0,i)) + "<mark>" + esc(s.slice(i, i+term.length)) + "</mark>" + esc(s.slice(i+term.length));
  }
  function snippet(text, term){
    var i = fold(text).indexOf(term);
    if(i === -1) return text.slice(0,150);
    var from = Math.max(0, i - 55);
    return (from > 0 ? "…" : "") + text.slice(from, from + 170);
  }
  function render(term){
    if(index.lang !== lang) buildIndex();
    results.innerHTML = "";
    sel = 0;
    var t = fold(term.trim());
    var hits;
    if(!t){
      hits = index.items.filter(function(e){ return e.path.indexOf("·") === -1; }).slice(0, 12);
    }else{
      hits = index.items.filter(function(e){
        return fold(e.title).indexOf(t) !== -1 || fold(e.text).indexOf(t) !== -1;
      }).sort(function(a,b){
        var at = fold(a.title).indexOf(t) !== -1 ? 0 : 1;
        var bt = fold(b.title).indexOf(t) !== -1 ? 0 : 1;
        return at - bt;
      }).slice(0, 24);
    }
    if(!hits.length){
      results.innerHTML = '<div class="res-empty">' + esc(STR.no_result[lang]) + ' &ldquo;' + esc(term) + '&rdquo;</div>';
      return;
    }
    hits.forEach(function(e, i){
      var a = document.createElement("a");
      a.className = "res" + (i === 0 ? " sel" : "");
      a.href = e.href;
      a.innerHTML = '<div class="rt">' + hl(e.title, t) + '</div>' +
                    '<div class="rp">' + esc(e.path) + '</div>' +
                    (t ? '<div class="rs">' + hl(snippet(e.text, t), t) + '</div>' : "");
      a.addEventListener("click", closeSearch);
      results.appendChild(a);
    });
  }
  function move(d){
    var items = results.querySelectorAll(".res");
    if(!items.length) return;
    items[sel].classList.remove("sel");
    sel = (sel + d + items.length) % items.length;
    items[sel].classList.add("sel");
    items[sel].scrollIntoView({block:"nearest"});
  }
  function openSearch(){
    ovl.hidden = false;
    q.value = "";
    render("");
    q.focus();
  }
  function closeSearch(){ ovl.hidden = true; }

  document.getElementById("openSearch").addEventListener("click", openSearch);
  ovl.addEventListener("mousedown", function(e){ if(e.target === ovl) closeSearch(); });
  q.addEventListener("input", function(){ render(q.value); });
  q.addEventListener("keydown", function(e){
    if(e.key === "ArrowDown"){ e.preventDefault(); move(1); }
    else if(e.key === "ArrowUp"){ e.preventDefault(); move(-1); }
    else if(e.key === "Enter"){
      var items = results.querySelectorAll(".res");
      if(items[sel]){ e.preventDefault(); items[sel].click(); }
    }
  });
  document.addEventListener("keydown", function(e){
    if((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")){ e.preventDefault(); openSearch(); }
    else if(e.key === "Escape"){ if(!ovl.hidden) closeSearch(); closeLangMenu(); }
  });

  /* ---------- start ---------- */
  try{
    var savedLang = localStorage.getItem("gf-lang");
    if(LANGS.indexOf(savedLang) !== -1) lang = savedLang;
  }catch(e){}
  route();
})();
