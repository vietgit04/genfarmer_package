#!/usr/bin/env python3
"""Build the GenFarmer automation guide into one self-contained HTML file.

    python3 build.py            -> dist/genfarmer-automation-guide.html

Content lives in content/*.py, styling and behaviour in template/, screenshots in images/.
"""
import base64
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "content"))

from common import (DEFAULT_LANG, FIELDS, LANG_NAMES, LANGS, P, SUPPORT_URL, TABS, UI, UPDATED,  # noqa: E402
                    VERSION, X_WORD, L)
from pages import ACC, APK, HOME, META, REF, RULES, SCRIPT, STORE  # noqa: E402
from platforms import FEAT, PKG_SUM, PLATFORMS  # noqa: E402

OUT = os.path.join(ROOT, "dist", "genfarmer-automation-guide.html")
GIF = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
PF = {p["id"]: p for p in PLATFORMS}

# ---------------------------------------------------------------- page order

GROUPS = [("start", ["home", "contents", "accounts", "rules"])]
for p in PLATFORMS:
    GROUPS.append((p["id"], [f"{p['id']}-{k}" for k in ("apk", "store", "login", "trust", "boost")]))
GROUPS.append(("ref", ["ref-matrix", "ref-fields", "ref-files"]))
ORDER = [pid for _, ids in GROUPS for pid in ids]
TABOF = {pid: tab for tab, ids in GROUPS for pid in ids}


def kind_of(pid):
    """'fb-trust' -> ('trust', platform); 'home' -> ('home', None)"""
    head, _, rest = pid.partition("-")
    if head in PF:
        return rest, PF[head]
    return pid, None


# ---------------------------------------------------------------- text helpers

def fill(text, **kw):
    for k, v in kw.items():
        text = text.replace("{" + k + "}", str(v))
    return text


def t(d, lang, **kw):
    return fill(d[lang] if isinstance(d, dict) else d, **kw)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def pkw(p, lang, **extra):
    """Placeholder values for a platform."""
    if p is None:
        return extra
    return dict(p=p["name"], P=p["upper"], id=p["id"], **extra)


# ---------------------------------------------------------------- markup helpers

def icon(name, cls="ic", sw="1.9"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"><use href="#i-{name}"/></svg>')


SIZES = {}
BRAND = {"brand-logo": "logo.png", "brand-mark": "mark.png", "brand-cover": "cover.jpg"}


def img_size(h):
    if h not in SIZES:
        from PIL import Image
        path = os.path.join(ROOT, "images", "brand", BRAND[h]) if h in BRAND else os.path.join(ROOT, "images", h + ".jpg")
        with Image.open(path) as im:
            SIZES[h] = im.size
    return SIZES[h]


USED_IMGS = set()


def img(h, alt="", cls=None):
    USED_IMGS.add(h)
    w, hh = img_size(h)
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{GIF}" data-img="{h}" alt="{html.escape(alt, quote=True)}" width="{w}" height="{hh}" loading="lazy">'


def fig(h, alt="", cap=None):
    w, _ = img_size(h)
    cls = "fig sm" if w < 900 else "fig"
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="{cls}">{img(h, alt)}{c}</figure>'


def hint(body, kind="", ic=None):
    ic = ic or {"": "info", "warn": "warn", "danger": "danger", "ok": "ok"}[kind]
    k = f" {kind}" if kind else ""
    return (f'<div class="hint{k}">\n  {icon(ic, sw="2")}\n  <div>{body}</div>\n</div>')


def step(text, *figs, extra=""):
    return f'<li class="step"><p>{text}</p>{extra}{"".join(figs)}</li>'


def stepper(items, start=0):
    st = f' style="counter-reset:st {start}"' if start else ""
    return f'<ol class="stepper"{st}>\n' + "\n".join(items) + "\n</ol>"


def table(head, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join("<tr>" + "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl{(" " + cls) if cls else ""}"><table>\n<thead><tr>{th}</tr></thead>\n<tbody>{body}</tbody>\n</table></div>'


def h2(lang, pid, anchor, text):
    return f'<h2 id="{lang}--{pid}--{anchor}">{text}</h2>'


def flow(nodes, n):
    out = []
    for b, span, i, hl in nodes:
        out.append(f'<div class="fnode{" hl" if hl else ""}"><b>{b}</b><span>{span}</span>{f"<i>{i}</i>" if i else ""}</div>')
    return f'<div class="flow n{n}">' + "".join(out) + "</div>"


def ul(items, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- fields

def field_name(key, lang):
    n = FIELDS[key]["name"]
    return f"<code>{n}</code>" if isinstance(n, str) else f"<strong>{n[lang]}</strong>"


def field_desc(spec, lang, p):
    key, x = spec if isinstance(spec, tuple) else (spec, None)
    d = t(FIELDS[key]["d"], lang, p=p["name"] if p else "")
    if x:
        one, many = X_WORD[x][lang]
        d = fill(d, x=one, xs=many)
    return d


def fields_table(specs, lang, p):
    rows = []
    for i, spec in enumerate(specs, 1):
        key = spec[0] if isinstance(spec, tuple) else spec
        rows.append([f'<td class="n">{i}</td>', field_name(key, lang), field_desc(spec, lang, p)])
    return table(["#", t(UI["col_field"], lang), t(UI["col_enter"], lang)], rows, "fields")


# ---------------------------------------------------------------- page bodies

def page_home(lang):
    o = []
    o.append(f"<p>{t(HOME['intro'], lang)}</p>")
    o.append(flow([(t(b, lang), t(s, lang), t(i, lang), k == 3) for k, (b, s, i) in enumerate(HOME["flow"])], 4))
    o.append(hint(t(HOME["read_first"], lang)))
    o.append(f'<div class="sect-head">{h2(lang, "home", "platforms", t(HOME["platforms"], lang))}</div>')
    cards = []
    for p in PLATFORMS:
        n = 1 + len(p["trust"]["fns"]) + len(p["boost"]["fns"])
        li = [f"<strong>AUTO LOGIN</strong>: {html.escape(p['login']['label'])}",
              "<strong>TRUST</strong>: " + ", ".join(html.escape(f["label"]) for f in p["trust"]["fns"]),
              "<strong>BOOST</strong>: " + ", ".join(html.escape(f["label"]) for f in p["boost"]["fns"])]
        cover = p["store"]["trust"][2]
        cards.append(
            f'<a class="card" href="#/{p["id"]}-apk"><div class="card-cover">{img(cover, "GENFARMER " + p["upper"] + " TRUST")}</div>'
            f'<div class="card-body">{icon("grid", sw="1.8")}<div class="ttl">{p["name"]}</div>'
            f'<div class="meta">{t(HOME["card_meta"], lang, n=n)}</div>{ul(li, "clist")}'
            f'<div class="dsc"><span class="go">{t(HOME["card_go"], lang, p=p["name"])} →</span></div></div></a>')
    o.append('<div class="cards three">' + "".join(cards) + "</div>")
    o.append(h2(lang, "home", "where", t(HOME["where"], lang)))
    apk_links = " · ".join(f'<a href="#/{p["id"]}-apk">{p["name"]}</a>' for p in PLATFORMS)
    rows = [[t(HOME["w_install"], lang), apk_links],
            [t(HOME["w_accounts"], lang), f'<a href="#/accounts">{t(META["accounts"]["title"], lang)}</a>'],
            [t(HOME["w_matrix"], lang), f'<a href="#/ref-matrix">{t(META["ref-matrix"]["title"], lang)}</a>'],
            [t(HOME["w_fields"], lang), f'<a href="#/ref-fields">{t(META["ref-fields"]["title"], lang)}</a>'],
            [t(HOME["w_files"], lang), f'<a href="#/ref-files">{t(META["ref-files"]["title"], lang)}</a>']]
    o.append(table([t(HOME["col_want"], lang), t(HOME["col_go"], lang)], rows))
    return "\n".join(o)


def page_title(pid, lang):
    kind, p = kind_of(pid)
    m = META[kind]
    n = len(p[kind]["fns"]) if p and kind in ("trust", "boost") else 0
    return t(m["title"], lang, **pkw(p, lang, n=n)), t(m["lede"], lang, **pkw(p, lang, n=n))


def nav_label(pid, lang):
    kind, p = kind_of(pid)
    return t(META[kind]["nav"], lang, **pkw(p, lang))


def page_contents(lang):
    o = []
    for tab, ids in GROUPS:
        o.append(h2(lang, "contents", tab, t(TABS[tab], lang)))
        rows = []
        for pid in ids:
            title, lede = page_title(pid, lang)
            rows.append([f'<a href="#/{pid}">{title}</a>', lede])
        o.append(table([t(UI["col_page"], lang), t(UI["col_covers"], lang)], rows))
    return "\n".join(o)


def page_accounts(lang):
    A = ACC
    o = [hint(t(A["prepare"], lang) + " " + t(A["one_table"], lang), "warn"),
         hint(t(P["one_acc"], lang), "warn")]
    o.append(h2(lang, "accounts", "format", t(A["h_format"], lang)))
    o.append(f"<p>{t(A['format_p'], lang)}</p>")
    o.append("<pre><code>mchthytrinh3863|clonie@hhh|KACTPZ2ZALLYMZ2EKNSC4SIEZXHSVPAN|20250218</code></pre>")
    o.append(f"<p>{t(A['first3'], lang)}</p>")
    o.append(table([t(UI["col_value"], lang), t(UI["col_meaning"], lang)], [
        ["<code>mchthytrinh3863</code>", t(A["v_uid"], lang)],
        ["<code>clonie@hhh</code>", t(A["v_pass"], lang)],
        ["<code>KACTPZ2ZALLYMZ2EKNSC4SIEZXHSVPAN</code>", t(A["v_2fa"], lang)],
        ["<code>20250218</code>", t(A["v_rest"], lang)]]))

    def mapping(fields):
        return ul([f"{t(A['data_n'], lang, n=i)}: <code>{f}</code>" for i, f in enumerate(fields, 1)])

    o.append(h2(lang, "accounts", "import", t(A["h_import"], lang)))
    s = [step(t(A["s1"], lang), fig("d511ab434d", strip_tags(t(A["s1"], lang)))),
         step(t(A["s2"], lang), fig("fa8c15366b", strip_tags(t(A["s2"], lang)))),
         step(t(A["s3"], lang), fig("014f44948f", strip_tags(t(A["s3"], lang)))),
         step(t(A["s4"], lang), fig("6601f367c1", strip_tags(t(A["s4"], lang)))),
         step(t(A["s5"], lang), fig("0fa6e73d98", strip_tags(t(A["s5"], lang)))),
         step(t(A["s6"], lang), fig("626afe362d", strip_tags(t(A["s6"], lang)))),
         step(t(A["s7"], lang), fig("a50bbcd2cf", strip_tags(t(A["s7"], lang))), extra=mapping(["UID", "PASSWORD", "2FA"])),
         step(t(A["s8"], lang), fig("5888683299", strip_tags(t(A["s8"], lang))))]
    o.append(stepper(s))
    o.append(f"<p>{t(A['added'], lang)}</p>" + fig("12c0001e1b", strip_tags(t(A["added"], lang))))

    o.append(h2(lang, "accounts", "bind", t(A["h_bind"], lang)))
    s = [step(t(A[k], lang), fig(h, strip_tags(t(A[k], lang)))) for k, h in
         [("s9", "94b115eb37"), ("s10", "dd02a5f3aa"), ("s11", "99cdc490d0"), ("s12", "30ebc58570"),
          ("s13", "73217d1baf"), ("s14", "099f293b96")]]
    o.append(stepper(s, start=8))
    o.append(hint(t(A["bound"], lang), "ok"))

    o.append(h2(lang, "accounts", "hotmail", t(A["h_hotmail"], lang)))
    o.append(f"<p>{t(A['hotmail_p'], lang)}</p>")
    o.append("<pre><code>username|passtiktok|email|password|refresh_token|client_id|cookie</code></pre>")
    s = [step(t(A["s1"], lang), fig("d511ab434d", strip_tags(t(A["s1"], lang)))),
         step(t(A["s2"], lang), fig("fa8c15366b", strip_tags(t(A["s2"], lang)))),
         step(t(A["s3"], lang), fig("014f44948f", strip_tags(t(A["s3"], lang)))),
         step(t(A["h4"], lang), fig("d797306b8c", strip_tags(t(A["h4"], lang)))),
         step(t(A["h5"], lang), fig("567e3a0a45", strip_tags(t(A["h5"], lang))), extra=hint(t(A["h5w"], lang), "warn")),
         step(t(A["s4"], lang), fig("6601f367c1", strip_tags(t(A["s4"], lang)))),
         step(t(A["s5"], lang), fig("0fa6e73d98", strip_tags(t(A["s5"], lang)))),
         step(t(A["s6"], lang), fig("626afe362d", strip_tags(t(A["s6"], lang)))),
         step(t(A["s7"], lang), fig("5079bab5d3", strip_tags(t(A["s7"], lang))),
              extra=mapping(["UID", "PASSWORD", "email", "password_email", "refresh_token", "client_id"])),
         step(t(A["s8"], lang), fig("5888683299", strip_tags(t(A["s8"], lang))))]
    o.append(stepper(s))
    o.append(f"<p>{t(A['added'], lang)}</p>" + fig("12c0001e1b", strip_tags(t(A["added"], lang))))
    o.append(hint(t(A["hotmail_bind"], lang)))
    return "\n".join(o)


def page_rules(lang):
    R = RULES
    anyp = t(R["any_p"], lang)
    o = [h2(lang, "rules", "check", t(R["h_check"], lang)),
         ul([t(P[k], lang, p=anyp) for k in ("chk_net", "chk_acc", "chk_proxy", "chk_lang")], "checklist"),
         h2(lang, "rules", "one", t(R["h_one"], lang)),
         hint(t(P["one_acc"], lang), "warn"),
         h2(lang, "rules", "path", t(R["h_path"], lang)),
         f"<p>{t(R['path_p'], lang)}</p>",
         flow([(str(i), t(a, lang), t(b, lang), i == 6) for i, (a, b) in enumerate(R["flow"], 1)], 6),
         f"<p>{t(P['s_watch'], lang)}</p>",
         h2(lang, "rules", "ai", t(R["h_ai"], lang)),
         f"<p>{t(R['ai_p'], lang)}</p>",
         hint(t(R["ai_more"], lang))]
    return "\n".join(o)


def page_apk(p, lang):
    kw = pkw(p, lang)
    a = p["apk_imgs"]
    link = f'<p><a href="{p["apk"]}" target="_blank" rel="noopener">{html.escape(p["apk"])}</a></p>'
    s = [step(t(APK["a1"], lang, **kw), extra=link)]
    for k, h in zip(("a2", "a3", "a4", "a5", "a6", "a7"), a):
        txt = t(APK[k], lang, **kw)
        s.append(step(txt, fig(h, strip_tags(txt))))
    return stepper(s) + "\n" + hint(t(APK["next"], lang, **kw), "ok", ic="ok")


def pkg_name(p, k):
    return {"login": f"AUTO LOGIN {p['upper']}", "trust": f"GENFARMER {p['upper']} TRUST",
            "boost": f"GENFARMER {p['upper']} BOOST"}[k]


def page_store(p, lang):
    kw = pkw(p, lang)
    pid = p["id"] + "-store"
    o = [h2(lang, pid, "packages", t(STORE["h_three"], lang))]
    rows = []
    for k in ("login", "trust", "boost"):
        sk = p["boost_sum"] if k == "boost" else k
        rows.append([f'<a href="#/{p["id"]}-{k}"><strong>{pkg_name(p, k)}</strong></a>', t(PKG_SUM[sk], lang, **kw)])
    o.append(table([t(UI["col_package"], lang), t(UI["col_does"], lang)], rows))
    o.append(h2(lang, pid, "open", t(STORE["h_open"], lang)))
    o.append(stepper([step(t(STORE["o1"], lang), fig("db70dd0d22", strip_tags(t(STORE["o1"], lang)))),
                      step(t(STORE["o2"], lang), fig("a50f3581e3", strip_tags(t(STORE["o2"], lang))))]))
    o.append(hint(t(STORE["repeat"], lang)))
    for k in ("login", "trust", "boost"):
        pk = pkg_name(p, k)
        i3, i4, done = p["store"][k]
        o.append(h2(lang, pid, k, pk))
        s3 = t(STORE["o3"], lang, pkg=pk, **kw)
        s4 = t(STORE["o4"], lang)
        o.append(stepper([step(s3, fig(i3, strip_tags(s3))), step(s4, fig(i4, strip_tags(s4)))], start=2))
        cap = t(STORE["done"], lang, pkg=pk)
        o.append(f"<p>{cap}</p>" + fig(done, cap))
    return "\n".join(o)


def features_and_notes(p, lang, keys, pid):
    kw = pkw(p, lang)
    notes = ul([t(P[k], lang, **kw) for k in ("chk_net", "chk_acc", "chk_proxy", "chk_lang")])
    return "\n".join([
        h2(lang, pid, "features", t(UI["features"], lang)),
        ul([t(FEAT[k], lang, **kw) for k in keys], "ticks"),
        hint(f"<p><strong>{t(UI['notes'], lang)}</strong></p>{notes}", "warn"),
        hint(t(P["one_acc"], lang), "warn"),
    ])


def opening_steps(p, lang, pkg, select, config):
    kw = pkw(p, lang)
    items = []
    for key, h in (("s_am", "b78e27a292"), ("s_table", "5f04c35f55"), ("s_setup", "56d029e17d"),
                   ("s_select", select), ("s_config", config)):
        txt = t(P[key], lang, pkg=pkg, **kw)
        items.append(step(txt, fig(h, strip_tags(txt))))
    return items


def page_login(p, lang):
    kw = pkw(p, lang)
    pid = p["id"] + "-login"
    lg = p["login"]
    o = [hint(t(SCRIPT["need_acc"], lang)), features_and_notes(p, lang, ["login"], pid)]
    o.append(h2(lang, pid, "run", t(SCRIPT["h_run_login"], lang, **kw)))
    items = opening_steps(p, lang, pkg_name(p, "login"), lg["select"], lg["config"])
    items.append(step(t(SCRIPT["fill_login"], lang), fig(lg["fields_img"], t(SCRIPT["fill_login"], lang)),
                      extra=fields_table(lg["fields"], lang, p)))
    items.append(step(t(P["s_save"], lang), fig(lg["save"], "SAVE")))
    items.append(step(t(P["s_rows"], lang), fig(lg["rows"], strip_tags(t(P["s_rows"], lang)))))
    run = t(P["s_run"], lang, label=html.escape(lg["label"]))
    items.append(step(run, *[fig(h, strip_tags(run)) for h in lg["run"]]))
    o.append(stepper(items))
    if lg.get("hotmail"):
        o.append(hint(t(SCRIPT["hotmail_login"], lang)))
    o.append(f"<p>{t(P['s_watch'], lang)}</p>" + fig(p["watch"], "CONTROL CENTER"))
    return "\n".join(o)


def page_script(p, lang, k):
    kw = pkw(p, lang)
    pid = f"{p['id']}-{k}"
    sc = p[k]
    pkg = pkg_name(p, k)
    o = [features_and_notes(p, lang, sc["features"], pid)]
    o.append(h2(lang, pid, "open", t(UI["open_pkg"], lang)))
    o.append(stepper(opening_steps(p, lang, pkg, sc["select"], sc["config"])))
    o.append(hint(t(SCRIPT["same_open"], lang)))
    for n, f in enumerate(sc["fns"], 1):
        o.append(h2(lang, pid, f["key"], f'{t(UI["fn_label"], lang, n=n)}: {t(f["title"], lang)}'))
        o.append(f"<p>{t(f['desc'], lang, **kw)}</p>")
        o.append(f'<p class="pathline">{t(SCRIPT["in_menu"], lang, label=html.escape(f["label"]))}</p>')
        items = [step(t(P["s_fill"], lang), fig(f["img_config"], t(P["s_fill"], lang)),
                      extra=fields_table(f["fields"], lang, p)),
                 step(t(P["s_save"], lang), fig(f["img_save"], "SAVE"))]
        c = f["custom"]
        if c:
            gear, addf, copy, paste = c["imgs"]
            txt = [t(P["s_gear"], lang), t(P["s_addf"], lang, f=c["f"]), t(P[c["copy"]], lang), t(P["s_paste"], lang, f=c["f"])]
            items += [step(txt[0], fig(gear, strip_tags(txt[0]))),
                      step(txt[1], fig(addf, strip_tags(txt[1])), extra=hint(t(P["w_addf"], lang, f=c["f"]), "warn")),
                      step(txt[2], fig(copy, strip_tags(txt[2]))),
                      step(txt[3], fig(paste, strip_tags(txt[3])))]
        items.append(step(t(P["s_rows"], lang), fig(f["img_rows"], strip_tags(t(P["s_rows"], lang)))))
        run = t(P["s_run"], lang, label=html.escape(f["label"]))
        items.append(step(run, *[fig(h, strip_tags(run)) for h in f["img_run"]]))
        o.append(stepper(items))
        watch = f"<p>{t(P['s_watch'], lang)}</p>"
        o.append(watch + (fig(p["watch"], "CONTROL CENTER") if n == 1 else ""))
    return "\n".join(o)


def script_rows(p, lang):
    """(package key, anchor, title, label, desc, fields) for every function of a platform."""
    kw = pkw(p, lang)
    out = [("login", "run", pkg_name(p, "login"), p["login"]["label"], t(FEAT["login"], lang, **kw), p["login"]["fields"])]
    for k in ("trust", "boost"):
        for f in p[k]["fns"]:
            out.append((k, f["key"], t(f["title"], lang), f["label"], t(f["desc"], lang, **kw), f["fields"]))
    return out


def page_matrix(lang):
    total = sum(1 + len(p["trust"]["fns"]) + len(p["boost"]["fns"]) for p in PLATFORMS)
    o = [f"<p>{t(REF['matrix_scripts'], lang, n=total, s=3 * len(PLATFORMS))}</p>"]
    for p in PLATFORMS:
        o.append(h2(lang, "ref-matrix", p["id"], p["name"]))
        rows = []
        for k, anchor, title, label, desc, _ in script_rows(p, lang):
            rows.append([f'<strong>{k.upper()}</strong>', f'<a href="#/{p["id"]}-{k}/{anchor}">{title}</a>',
                         f"<code>{html.escape(label)}</code>", desc])
        o.append(table([t(UI["col_package"], lang), t(UI["col_function"], lang), t(UI["col_menu"], lang),
                        t(UI["col_does"], lang)], rows, "matrix"))
    return "\n".join(o)


FIELD_GROUPS = [
    (L("Common fields", "Trường dùng chung", "Campos comunes", "共通の項目"),
     ["threads", "apikey", "apikey_caption", "language", "topic_nurture", "topic_related", "topic_interest", "topic_ai",
      "topic_reup", "topic_msg", "topic_media", "topic_live", "topic_videos"]),
    (L("Targets", "Đối tượng tương tác", "Objetivos", "やり取りの対象"),
     ["links_posts", "links_profiles", "live_link", "views_per", "views_per_opt"]),
    (L("Guiding the AI", "Định hướng cho AI", "Guiar a la IA", "AI への指示"),
     ["aiguide", "action_rate", "goal", "goal_live", "goal_msg", "goal_media", "video_goals", "video_goals_live",
      "portrait", "portrait_live", "post_sample", "comment_sample", "msg_template", "caption_tpl", "caption_mode"]),
    (L("Files and folders", "File và folder", "Archivos y carpetas", "ファイルとフォルダー"),
     ["file_comment", "file_or_ai", "x_pick", "x_file", "folder_images_opt", "img_pick", "folder_avatar",
      "folder_media", "folder_videos"]),
    (L("Posting options", "Tuỳ chọn đăng bài", "Opciones de publicación", "投稿のオプション"),
     ["share_story", "ai_video", "delete_after", "hashtags", "video_count"]),
    (L("Login", "Đăng nhập", "Inicio de sesión", "ログイン"), ["captcha"]),
]


def field_usage(lang):
    use = {}
    for p in PLATFORMS:
        for k, anchor, title, _, _, fields in script_rows(p, lang):
            for spec in fields:
                key = spec[0] if isinstance(spec, tuple) else spec
                link = f'<a href="#/{p["id"]}-{k}/{anchor}">{p["name"]} · {title}</a>'
                use.setdefault(key, [])
                if link not in use[key]:
                    use[key].append(link)
    return use


def page_fields(lang):
    use = field_usage(lang)
    listed = {k for _, ks in FIELD_GROUPS for k in ks}
    missing = set(FIELDS) - listed
    assert not missing, f"fields not grouped: {missing}"
    o = []
    for gi, (gname, keys) in enumerate(FIELD_GROUPS, 1):
        o.append(h2(lang, "ref-fields", f"g{gi}", t(gname, lang)))
        rows = []
        for key in keys:
            d = t(FIELDS[key]["d"], lang, p="Facebook / Instagram / TikTok")
            words = [X_WORD[x][lang] for x in ("name", "bio", "username")]
            d = fill(d, x=" / ".join(dict.fromkeys(w[0] for w in words)), xs=" / ".join(dict.fromkeys(w[1] for w in words)))
            rows.append([field_name(key, lang), d, "<br>".join(use.get(key, []))])
        o.append(table([t(UI["col_field"], lang), t(UI["col_meaning"], lang), t(UI["col_used_by"], lang)], rows, "fieldref"))
    return "\n".join(o)


def page_files(lang):
    use = field_usage(lang)
    o = [h2(lang, "ref-files", "rules", t(REF["files_rules"], lang)),
         ul([t(REF[k], lang) for k in ("f1", "f2", "f3", "f4")], "checklist"),
         h2(lang, "ref-files", "example", t(REF["h_example"], lang)),
         f"<pre><code>{html.escape(t(REF['example'], lang))}</code></pre>",
         h2(lang, "ref-files", "which", t(REF["h_which"], lang))]
    xs = " / ".join(dict.fromkeys(X_WORD[x][lang][1] for x in ("name", "bio", "username")))
    rows = [[t(REF["comments"], lang), field_name("file_comment", lang), "<br>".join(use["file_comment"])],
            [xs, f'<strong>{t(FIELDS["x_file"]["name"], lang)}</strong>', "<br>".join(use["x_file"])]]
    o.append(table([t(REF["col_file"], lang), t(UI["col_field"], lang), t(UI["col_used_by"], lang)], rows))
    o.append(h2(lang, "ref-files", "fb", t(REF["h_fbcols"], lang)))
    o.append(f"<p>{t(REF['fbcols_p'], lang)}</p>")
    return "\n".join(o)


def body_of(pid, lang):
    kind, p = kind_of(pid)
    if p:
        return {"apk": page_apk, "store": page_store, "login": page_login}.get(kind, None)(p, lang) \
            if kind in ("apk", "store", "login") else page_script(p, lang, kind)
    return {"home": page_home, "contents": page_contents, "accounts": page_accounts, "rules": page_rules,
            "ref-matrix": page_matrix, "ref-fields": page_fields, "ref-files": page_files}[pid](lang)


# ---------------------------------------------------------------- page shell

def section(pid, lang):
    title, lede = page_title(pid, lang)
    tab = TABOF[pid]
    crumb = t(TABS[tab], lang)
    first = GROUPS[[g for g, _ in GROUPS].index(tab)][1][0]
    i = ORDER.index(pid)
    nav = []
    if i > 0:
        q = ORDER[i - 1]
        nav.append(f'<a href="#/{q}"><span class="k">{t(UI["prev"], lang)}</span><span class="v">{nav_full(q, lang)}</span></a>')
    else:
        nav.append("<span></span>")
    if i < len(ORDER) - 1:
        q = ORDER[i + 1]
        nav.append(f'<a class="next" href="#/{q}"><span class="k">{t(UI["next"], lang)}</span><span class="v">{nav_full(q, lang)}</span></a>')
    cover = ""
    if pid == "home":
        cover = (f'<div class="cover">{img("brand-cover", "", "bg")}<span class="shade"></span><div class="cover-in"><div class="cover-txt">'
                 f'<div class="w1">{t(HOME["cover_w1"], lang)}</div><div class="w2">{t(HOME["cover_w2"], lang, v=VERSION)}</div>'
                 f'</div></div></div>')
    return f'''
<!-- ==================== {lang} / {pid} ==================== -->
<section class="page" id="p-{lang}-{pid}" lang="{lang}" data-title="{html.escape(strip_tags(title), quote=True)}" data-crumb="{html.escape(crumb, quote=True)}" hidden>
  {cover}
  <div class="wrap">
    <div class="crumb"><a href="#/{first}">{crumb}</a></div>
    <h1 class="title">{title}</h1>
    <p class="lede">{lede}</p>
    <div class="doc">
{body_of(pid, lang)}
    </div>
    <div class="pagenav">{"".join(nav)}</div>
    <p class="updated">{t(UPDATED, lang)}</p>
  </div>
</section>'''


def nav_full(pid, lang):
    kind, p = kind_of(pid)
    return f"{p['name']} · {nav_label(pid, lang)}" if p else nav_label(pid, lang)


def spans(d, **kw):
    """One span per language; JS shows the active one."""
    return "".join(f'<span data-l="{l}"{"" if l == DEFAULT_LANG else " hidden"}>{t(d, l, **kw)}</span>' for l in LANGS)


def sidebar():
    groups = []
    icons = {"apk": "box", "store": "grid", "login": "id", "trust": "spark", "boost": "bot"}
    for tab, ids in GROUPS:
        links = []
        for pid in ids:
            kind, p = kind_of(pid)
            ic = icons.get(kind) if p else META[pid]["icon"]
            links.append(f'<a class="nav-a" href="#/{pid}" data-nav="{pid}">{icon(ic)}{spans(META[kind]["nav"], **pkw(p, DEFAULT_LANG))}</a>')
        groups.append(f'<div class="side-grp" data-tab="{tab}"><div class="side-lbl">{spans(TABS[tab])}</div>' + "".join(links) + "</div>")
    return "\n".join(groups)


def tabs():
    return "\n".join(f'<a class="tab-l" href="#/{ids[0]}" data-tab="{tab}">{spans(TABS[tab])}</a>' for tab, ids in GROUPS)


def lang_menu():
    return "".join(f'<button type="button" role="menuitemradio" data-set-lang="{l}" aria-checked="false">'
                   f'<span>{LANG_NAMES[l]}</span><span class="code">{l.upper()}</span></button>' for l in LANGS)


EXTRA_CSS = """
/* ---------- automation guide additions ---------- */
:root{--font:Inter,"Noto Sans JP",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.langwrap{position:relative}
.langbtn{height:36px;display:inline-flex;align-items:center;gap:6px;padding:0 10px;border:1px solid var(--line);
  border-radius:var(--r);background:var(--surface);color:var(--text);font:inherit;font-size:13px;font-weight:650;cursor:pointer}
.langbtn:hover{border-color:var(--line-strong);background:var(--surface-2)}
.langbtn svg{width:16px;height:16px;color:var(--muted)}
.langmenu{position:absolute;right:0;top:calc(100% + 6px);min-width:176px;padding:6px;z-index:90;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);box-shadow:0 14px 34px rgba(15,17,21,.14)}
.langmenu button{display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;padding:8px 10px;
  border:0;border-radius:6px;background:none;color:var(--text);font:inherit;font-size:14px;cursor:pointer;text-align:left}
.langmenu button:hover{background:var(--surface-2)}
.langmenu button .code{font-size:11.5px;color:var(--muted-2);font-weight:600}
.langmenu button[aria-checked="true"]{color:var(--blue);font-weight:650}
.step>p:first-child{margin:1px 0 10px;color:var(--ink)}
.step .fig{margin:12px 0 4px}
.step .hint{margin:12px 0}
.step ul{margin:6px 0 10px}
.fig.sm img{max-width:min(100%,560px)}
.fig figcaption{padding:9px 14px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
.tbl.fields td:nth-child(2){white-space:nowrap}
.tbl.fieldref td:first-child{white-space:nowrap}
.tbl.fieldref td:last-child{font-size:13.5px;min-width:180px}
.tbl.matrix td:nth-child(3) code{white-space:nowrap}
.doc ul.ticks{list-style:none;padding-left:0}
.doc ul.ticks li{position:relative;padding-left:26px}
.doc ul.ticks li::before{content:"";position:absolute;left:3px;top:.55em;width:11px;height:6px;
  border-left:2px solid var(--i-ok);border-bottom:2px solid var(--i-ok);transform:rotate(-45deg)}
.hint ul{margin:6px 0 0;padding-left:18px}
.hint li{margin:3px 0}
.cards.three{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.card .go{color:var(--blue);font-weight:600}
a.card:hover{border-color:var(--line-strong);text-decoration:none}
.card-cover img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;object-position:top left}
.pagenav>span{display:block}
@media (max-width:640px){
  .tbl.fields td:nth-child(2),.tbl.fieldref td:first-child{white-space:normal}
}
"""

GLOBE = '<g id="i-globe"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/></g>'


def build():
    css = open(os.path.join(ROOT, "template", "style.css"), encoding="utf-8").read()
    css = css.replace("   GenFarmer Support Center\n", "   GenFarmer Automation Guide (built on the Support Center design)\n", 1)
    icons = open(os.path.join(ROOT, "template", "icons.svg"), encoding="utf-8").read()
    icons = icons.replace("</defs>", GLOBE + "\n</defs>")
    js = open(os.path.join(ROOT, "template", "app.js"), encoding="utf-8").read()

    sections = [section(pid, lang) for lang in LANGS for pid in ORDER]

    # images: screenshots + brand assets
    imgs = {}
    for h in sorted(USED_IMGS):
        if h.startswith("brand-"):
            continue
        with open(os.path.join(ROOT, "images", h + ".jpg"), "rb") as f:
            imgs[h] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    for name, fn in BRAND.items():
        mime = "png" if fn.endswith(".png") else "jpeg"
        with open(os.path.join(ROOT, "images", "brand", fn), "rb") as f:
            imgs[name] = f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()
    unused = sorted(set(os.path.splitext(n)[0] for n in os.listdir(os.path.join(ROOT, "images")) if n.endswith(".jpg")) - USED_IMGS)

    strs = {"search_ph": UI["search_ph"], "no_result": UI["no_result"], "burger": UI["menu"], "themeBtn": UI["theme"],
            "langBtn": UI["lang"]}
    data = ("var PAGES = %s;\nvar TABOF = %s;\nvar LANGS = %s;\nvar DEFAULT_LANG = %s;\nvar STR = %s;\nvar DOC_TITLE = %s;\n" % (
        json.dumps(ORDER), json.dumps(TABOF), json.dumps(LANGS), json.dumps(DEFAULT_LANG),
        json.dumps(strs, ensure_ascii=False), json.dumps(UI["doc_title"], ensure_ascii=False)))

    page = f'''<!doctype html>
<html lang="{DEFAULT_LANG}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{UI["doc_title"][DEFAULT_LANG]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{css}
{EXTRA_CSS}
</style>
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
{icons}
</svg>

<header class="hdr">
  <button class="iconbtn burger" id="burger" aria-label="{UI["menu"][DEFAULT_LANG]}"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><use href="#i-menu"/></svg></button>
  <a class="hdr-brand" href="#/home">
    {img("brand-logo", "GenFarmer").replace(' loading="lazy"', "")}
    <span class="sub">{spans(UI["brand_sub"])}</span>
  </a>
  <div class="hdr-mid">
    <button class="searchbtn" id="openSearch">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><use href="#i-search"/></svg>
      <span class="lbl">{spans(UI["search"])}</span>
      <span class="kbd"><span>Ctrl</span><span>K</span></span>
    </button>
  </div>
  <div class="hdr-right">
    <div class="langwrap">
      <button class="langbtn" id="langBtn" aria-haspopup="menu" aria-expanded="false" aria-label="{UI["lang"][DEFAULT_LANG]}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><use href="#i-globe"/></svg>
        <span id="langCode">{DEFAULT_LANG.upper()}</span>
      </button>
      <div class="langmenu" id="langMenu" role="menu" hidden>{lang_menu()}</div>
    </div>
    <button class="iconbtn" id="themeBtn" aria-label="{UI["theme"][DEFAULT_LANG]}">
      <svg class="ic-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><use href="#i-sun"/></svg>
      <svg class="ic-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" hidden><use href="#i-moon"/></svg>
    </button>
    <a class="hdr-cta" href="{SUPPORT_URL}" target="_blank" rel="noopener">{spans(UI["support"])}</a>
  </div>
</header>

<nav class="tabsnav">
{tabs()}
</nav>

<div class="scrim" id="scrim"></div>

<div class="shell">

  <nav class="side" id="side">
    <div class="side-card">
{sidebar()}
    </div>
    <div class="side-foot">
      {img("brand-mark", "").replace(' loading="lazy"', "")}
      {spans(UI["version"], v=VERSION)}
    </div>
  </nav>

  <main class="main" id="main">
{"".join(sections)}
  </main>

  <aside class="toc">
    <div class="toc-h">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><use href="#i-list"/></svg>
      {spans(UI["on_page"])}
    </div>
    <div id="tocList"></div>
  </aside>

</div>

<div class="ovl" id="ovl" hidden>
  <div class="modal" role="dialog" aria-modal="true" aria-label="Search">
    <input id="q" type="text" placeholder="{UI["search_ph"][DEFAULT_LANG]}" autocomplete="off" spellcheck="false">
    <div class="results" id="results"></div>
  </div>
</div>

<script>
/* screenshots and brand images, embedded so the file works on its own */
var IMGS = {json.dumps(imgs)};
</script>
<script>
{data}
{js}
</script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    size = os.path.getsize(OUT) / 1048576
    print(f"{OUT}\n  {len(ORDER)} pages x {len(LANGS)} languages, {len(imgs)} images, {size:.1f} MB")
    if unused:
        print(f"  note: {len(unused)} images in images/ are not used: {', '.join(unused)}")


if __name__ == "__main__":
    build()
