"""Build data/courses.json — a pool of current Harvard GSD + MIT courses, tagged by discipline.

Sources
  Harvard GSD: public WordPress API  https://www.gsd.harvard.edu/wp-json/wp/v2/gsd-courses
  MIT:         Subject listing       https://student.mit.edu/catalog/m<DEPT><a-z>.html

Run:  python3 scripts/build_courses.py
"""
import html, json, re, sys, time, urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
OUT = Path(__file__).resolve().parent.parent / "data" / "courses.json"

# GSD terms from fall 2025 on
GSD_TERMS = re.compile(r"-(fall-2025|spring-2026|fall-2026|spring-2027|january-2026|january-2027)/?$")
# MIT departments that interdisciplinary designers tend to cross into
MIT_DEPTS = ["4", "11", "MAS", "CMS", "STS", "21A", "21M", "21W", "21H", "24", "9", "1", "2", "6", "16", "15"]
MIT_PER_DEPT_CAP = 60   # keep big departments (6, 15) from swamping the pool

# ── discipline tagging (same 8 keys as Chloeverse) ──────────────────────────
KW = {
    "arch":   r"architect|urban|\bcit(y|ies)\b|landscape|built environment|housing|real estate|preservation|neighborhood",
    "design": r"design|studio|interaction|interface|fabricat|prototyp|visuali[sz]|craft|graphic|tangible|furniture",
    "art":    r"\bart\b|\barts\b|artist|music|film|cinema|video|photograph|perform|theater|theatre|sound|drawing|paint|sculpt|exhibition|curat|aesthetic|poetry",
    "hum":    r"histor|theor|philosoph|cultur|literat|writing|ethic|critic|religio|narrative|humanit|language|memory|archive|colonial",
    "soc":    r"social|societ|polic|econom|politic|governance|community|justice|equity|health|labor|public policy|psycholog|behavio|anthropolog|\blaw\b|financ|market|organi[sz]ation",
    "sci":    r"ecolog|biolog|climate|environmental science|chemi|physics\b|geolog|carbon|soil|botan|species|brain|neuro|cognit|ocean",
    "eng":    r"engineer|structur|robot|mechani|materials?\b|construction|manufactur|energy|sensor|electr|circuit|infrastructure|aero|thermal",
    "cs":     r"comput|\bai\b|artificial intelligence|machine learning|\bdata\b|code|coding|programm|algorithm|software|digital|network|simulat|generative|neural|cyber",
}
DEPT_DEFAULT = {  # fallback tag by department/prefix
    "architecture": "arch", "landscape-architecture": "arch", "urban-planning-and-design": "arch",
    "4": "arch", "11": "arch", "MAS": "design", "CMS": "hum", "STS": "hum", "21A": "soc", "21M": "art",
    "21W": "hum", "21H": "hum", "24": "hum", "9": "sci", "1": "eng", "2": "eng", "6": "cs", "16": "eng", "15": "soc",
}

def tag(title, desc, dept):
    score = {}
    for k, rx in KW.items():
        t = len(re.findall(rx, title, re.I)) * 3 + len(re.findall(rx, desc, re.I))
        if t: score[k] = t
    d = DEPT_DEFAULT.get(dept)
    if d: score[d] = score.get(d, 0) + 3
    ranked = sorted(score, key=score.get, reverse=True)
    top = score[ranked[0]] if ranked else 0
    return [k for k in ranked if score[k] >= max(2, top * 0.34)][:4] or ([d] if d else ["design"])

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace"), r.headers

def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

SKIP = re.compile(r"thesis|independent study|doctoral|dissertation|reading and research|research in|special (problems|studies|subject)|^(architecture|landscape architecture|urban planning|urban design) (i|ii|iii|iv)\b|tutorial|internship|practicum|undergraduate research|graduate research|seminar in .*research", re.I)

# ── Harvard GSD ─────────────────────────────────────────────────────────────
def gsd():
    out, page, pages = [], 1, 1
    while page <= pages:
        body, hdr = get(f"https://www.gsd.harvard.edu/wp-json/wp/v2/gsd-courses?per_page=100&page={page}"
                        "&orderby=date&order=desc&_fields=link,title,excerpt,class_list")
        pages = int(hdr.get("X-WP-TotalPages") or 1)
        batch = json.loads(body)
        hit = 0
        for c in batch:
            m = GSD_TERMS.search(c["link"])
            if not m: continue
            hit += 1
            term = m.group(1)
            cls = c.get("class_list", [])
            dept = next((x[len("department-"):] for x in cls if x.startswith("department-")), "")
            ctype = next((x[len("course_type-"):].replace("-", " ") for x in cls if x.startswith("course_type-")), "")
            title, desc = text(c["title"]["rendered"]), text(c["excerpt"]["rendered"]).replace(" […]", "…")
            if SKIP.search(title): continue
            out.append({"school": "Harvard GSD", "code": "", "name": title, "dept": dept.replace("-", " ").title(),
                        "type": ctype.title(), "term": term.replace("-", " ").title(),
                        "year": int(term[-4:]) - (1 if term.startswith("spring") or term.startswith("january") else 0),
                        "link": c["link"], "desc": desc[:320], "tags": tag(title, desc, dept)})
        print(f"GSD page {page}/{pages}: {hit} in range", file=sys.stderr)
        if page > 3 and hit == 0: break        # sorted newest-first; stop once past the window
        page += 1; time.sleep(0.4)
    return out

# ── MIT ─────────────────────────────────────────────────────────────────────
ENTRY = re.compile(r'<a name="([^"]+)"></a>\s*<p><h3>(.*?)</h3>(.*?)<!--end-->', re.S)
def mit():
    out = []
    for dept in MIT_DEPTS:
        got = []
        for letter in "abcdefgh":
            url = f"https://student.mit.edu/catalog/m{dept}{letter}.html"
            try: body, _ = get(url)
            except Exception: break
            entries = ENTRY.findall(body)
            if not entries: break
            for code, h3, rest in entries:
                if re.search(r"Not offered (regularly|academic year)", rest): continue
                title = text(re.sub(r"^\S+\s+", "", h3.split("<br>")[0]))
                if SKIP.search(title): continue
                parts = rest.split('alt="______"')
                desc = text(re.split(r"<br>(Fall|Spring|Summer|IAP):|<br>No textbook", parts[-1])[0]) if parts else ""
                desc = re.sub(r'^[^>]*>\s*', '', desc).strip()
                if len(desc) < 40: continue
                got.append({"school": "MIT", "code": code, "name": title, "dept": dept, "type": "",
                            "term": "2026–27", "year": 2026, "link": f"{url}#{code}",
                            "desc": desc[:320], "tags": tag(title, desc, dept)})
            time.sleep(0.3)
        # spread the cap across the department instead of taking only the intro subjects
        step = max(1, len(got) // MIT_PER_DEPT_CAP)
        got = got[::step][:MIT_PER_DEPT_CAP]
        print(f"MIT {dept}: {len(got)}", file=sys.stderr)
        out += got
    return out

if __name__ == "__main__":
    courses = gsd() + mit()
    seen, uniq = set(), []
    for c in courses:
        key = (c["school"], c["name"].lower())
        if key in seen: continue
        seen.add(key); uniq.append(c)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"built": time.strftime("%Y-%m-%d"), "courses": uniq}, ensure_ascii=False, indent=0))
    print(f"wrote {len(uniq)} courses → {OUT}", file=sys.stderr)
