#!/usr/bin/env python3
"""国外代理纯域名合并脚本（仓库 passionsu-su/gfw-proxy-domain）。
下载各开源规则库的代理/GFW 域名 -> 清洗 -> 去重 -> 剔除国内直连冲突 -> 输出 TXT、stats.json、README.md。
用法: python3 build.py   (输出到当前目录)
"""
import os, re, json, time, base64, datetime, urllib.request, concurrent.futures as cf

OUT = os.getcwd()
REPO_RAW = "https://raw.githubusercontent.com/passionsu-su/gfw-proxy-domain/main/"
LS = "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/"
LC = "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/"
BM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/"
ACL = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/"
SOURCES = [  # (名称, URL, 格式)
    ("Loyalsoldier proxy-list", LS + "proxy-list.txt", "auto"),
    ("Loyalsoldier gfw", LS + "gfw.txt", "auto"),
    ("Loyalsoldier clash-rules proxy", LC + "proxy.txt", "auto"),
    ("Loyalsoldier clash-rules gfw", LC + "gfw.txt", "auto"),
    ("gfwlist", "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt", "gfwlist"),
    ("blackmatrix7 Global_Domain", BM + "Global/Global_Domain.list", "auto"),
    ("blackmatrix7 Proxy_Domain", BM + "Proxy/Proxy_Domain.list", "auto"),
    ("ACL4SSR ProxyGFWlist", ACL + "ProxyGFWlist.list", "auto"),
    ("ACL4SSR ProxyLite", ACL + "ProxyLite.list", "auto"),
    ("Johnshall sr_top500_banlist", "https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/release/sr_top500_banlist.conf", "proxyrules"),
]
LAZY = "https://raw.githubusercontent.com/LOWERTOP/Shadowrocket/main/lazy.conf"
LAZY_INLINE = "LOWERTOP lazy.conf 内联 PROXY"
# 国内直连列表：完全相同的域名从代理列表中剔除，避免冲突
CHINA = "https://raw.githubusercontent.com/passionsu-su/china-direct-domain/main/china-direct-domains-full.txt"

DOM = re.compile(r"^(?=.{1,253}$)([a-z0-9_]([a-z0-9_-]{0,61}[a-z0-9])?\.)*[a-z0-9_]([a-z0-9_-]{0,61}[a-z0-9])?$")
IPV4 = re.compile(r"^\d+(\.\d+){3}$")
RULE_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "HOST", "HOST-SUFFIX"}
JSD_HOSTS = ["cdn", "fastly", "testingcf", "gcore"]


def jsdelivr(url):
    m = re.match(r"https?://raw\.githubusercontent\.com/([^/]+)/([^/]+)/(?:refs/heads/)?([^/]+)/(.+)", url)
    if not m:
        return []
    path = f"gh/{m.group(1)}/{m.group(2)}@{m.group(3)}/{m.group(4)}"
    return [f"https://{h}.jsdelivr.net/{path}" for h in JSD_HOSTS]


def _fetch(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 gfw-proxy-domain"})
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read().decode("utf-8", "ignore")
            if not t.strip():
                raise RuntimeError("empty response")
            return t
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"{type(last).__name__}: {last}")


def fetch(url, tries=3):
    """先下 raw.githubusercontent.com，失败则依次改用 jsDelivr 镜像。"""
    errs = []
    for i, u in enumerate([url] + jsdelivr(url)):
        try:
            return _fetch(u, tries if i == 0 else 2)
        except Exception as e:
            errs.append(f"{u.split('/')[2]}: {e}")
    raise RuntimeError("; ".join(errs))


def clean(d):
    d = d.strip().strip("'\"").lower()
    for p in ("full:", "domain:", "+."):
        if d.startswith(p):
            d = d[len(p):]
    d = d.lstrip(".*").rstrip(".")
    if not d or "." not in d or IPV4.match(d) or not DOM.match(d):
        return None
    return d


def parse_gfwlist(text):
    t = text.strip()
    if not t.startswith("[AutoProxy") and "||" not in t[:2000]:
        t = base64.b64decode("".join(t.split()) + "==").decode("utf-8", "ignore")
    out = []
    for l in t.splitlines():
        l = l.strip()
        if not l or l[0] in "![" or l.startswith("@@") or (l.startswith("/") and l.endswith("/")):
            continue
        l = l.lstrip("|")
        l = re.sub(r"^[a-z]+://", "", l)
        host = re.split(r"[/:%^*?]", l, 1)[0]
        if "*" in l.split("/")[0]:
            continue
        if d := clean(host):
            out.append(d)
    return out


def parse(text, fmt, policy=None):
    """policy: 只收第三段为该策略的规则（用于 conf 文件）。"""
    if fmt == "gfwlist":
        return parse_gfwlist(text)
    out = []
    for raw in text.splitlines():
        l = raw.strip()
        if not l or l[0] in "#!;[":
            continue
        if l.startswith("- "):
            l = l[2:].strip().strip("'\"")
        if l.startswith(("regexp:", "keyword:", "payload:", "include:")):
            continue
        if "," in l:
            p = [x.strip() for x in l.split(",")]
            if p[0].upper() not in RULE_TYPES or len(p) < 2:
                continue
            if policy and (len(p) < 3 or p[2].upper() != policy):
                continue
            d = clean(p[1])
        else:
            if policy:
                continue
            d = clean(l.split()[0].split("@")[0])
        if d:
            out.append(d)
    return out


def main():
    results, failed, retry, urls = {}, [], [], {LAZY_INLINE: LAZY}
    jobs = list(SOURCES)
    try:
        lazy = fetch(LAZY)
        results[LAZY_INLINE] = parse(lazy, "rules", policy="PROXY")
        for l in lazy.splitlines():
            p = [x.strip() for x in l.strip().split(",")]
            if len(p) >= 3 and p[0].upper() == "RULE-SET" and p[2].upper() == "PROXY":
                jobs.append((f"LOWERTOP RULE-SET {p[1].rsplit('/', 1)[-1]}", p[1], "auto"))
    except Exception as e:
        failed.append(f"LOWERTOP lazy.conf ({e})")

    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(fetch, u): (n, f, u) for n, u, f in jobs}
        for fu in cf.as_completed(futs):
            n, f, u = futs[fu]
            urls[n] = u
            try:
                results[n] = parse(fu.result(), f, "PROXY" if f == "proxyrules" else None)
            except Exception as e:
                retry.append((n, u, f))
    if retry:
        time.sleep(15)
    for n, u, f in retry:
        try:
            results[n] = parse(fetch(u), f, "PROXY" if f == "proxyrules" else None)
        except Exception as e2:
            failed.append(f"{n} ({e2})")

    full = set()
    for v in results.values():
        full.update(v)
    removed = 0
    try:
        china = set(fetch(CHINA).split())
        removed = len(full & china)
        full -= china
    except Exception as e:
        failed.append(f"国内直连冲突表 ({e})")

    keep = set()
    for d in sorted(full, key=lambda x: x.count(".")):
        parts = d.split(".")
        if not any(".".join(parts[i:]) in keep for i in range(1, len(parts))):
            keep.add(d)
    if len(full) < 20000:
        raise SystemExit(f"Too few domains ({len(full)}), aborting. Failed: {failed}")

    open(os.path.join(OUT, "gfw-proxy-domains.txt"), "w").write("\n".join(sorted(keep)) + "\n")
    open(os.path.join(OUT, "gfw-proxy-domains-full.txt"), "w").write("\n".join(sorted(full)) + "\n")
    upd = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    order = [n for n, _, _ in jobs] + [LAZY_INLINE]
    stats = {"updated": upd.strftime("%Y-%m-%d %H:%M CST"), "full": len(full), "compact": len(keep),
             "removed_china_conflicts": removed,
             "sources": {n: len(results[n]) for n in order if n in results}, "failed": failed}
    json.dump(stats, open(os.path.join(OUT, "stats.json"), "w"), ensure_ascii=False, indent=2)
    write_readme(stats, urls, order)
    print(json.dumps(stats, ensure_ascii=False, indent=1))


def page(url):
    m = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+)", url)
    if not m:
        return url, url, url
    o, r, b, p = m.groups()
    return f"{o}/{r}", f"https://github.com/{o}/{r}", f"https://github.com/{o}/{r}/blob/{b}/{p}"


def write_readme(st, urls, order):
    failed_names = {x.split(" (")[0] for x in st["failed"]}
    nsrc = len(order)
    L = ["# gfw-proxy-domain", "",
         "合并多个开源规则库的国外代理（GFW / Proxy）域名，去掉前缀、正则、关键词和 IP 类规则，统一小写、校验格式后去重，并剔除与国内直连列表完全相同的域名，输出一行一个的纯域名。每天北京时间 02:45 由 GitHub Actions 自动更新。", "",
         f"最近更新：{st['updated']}　上游来源：{nsrc} 个（成功 {nsrc - len(failed_names & set(order))}，失败 {len(failed_names & set(order))}）", "",
         "## 文件", "",
         "| 文件 | 说明 | 条数 | 链接 |", "| --- | --- | ---: | --- |",
         f"| gfw-proxy-domains.txt | 精简版（父域名已在列表时去掉子域名） | {st['compact']:,} | [raw]({REPO_RAW}gfw-proxy-domains.txt) |",
         f"| gfw-proxy-domains-full.txt | 完整去重版 | {st['full']:,} | [raw]({REPO_RAW}gfw-proxy-domains-full.txt) |",
         f"| stats.json | 各来源条数与失败来源 | - | [raw]({REPO_RAW}stats.json) |", "",
         "## 上游规则库", "",
         "| # | 来源 | 规则库 | 文件 | 有效域名数 | 状态 |", "| ---: | --- | --- | --- | ---: | --- |"]
    for i, n in enumerate(order, 1):
        u = urls.get(n, "")
        repo, home, blob = page(u)
        fname = u.rsplit("/", 1)[-1] if u else "-"
        cnt = st["sources"].get(n)
        status = "⚠️ 下载失败" if n in failed_names else ("正常" if cnt else "无内容")
        L.append(f"| {i} | {n} | [{repo}]({home}) | [{fname}]({blob}) | {cnt or 0:,} | {status} |")
    L += ["", "有效域名数为从该文件解析出的合法域名条数（含与其他来源重叠的部分）。LOWERTOP 的规则集由 lazy.conf 中所有 `RULE-SET ...,PROXY` 动态解析，Johnshall 只取策略为 Proxy 的规则，lazy.conf 变化时来源会随之增减。", "",
          "## 处理规则", "",
          "- gfwlist 先 Base64 解码，按 AutoProxy 语法取主机名，跳过 @@ 白名单和正则",
          "- 去掉开头的点和 full: / domain: / +. 前缀",
          "- 丢弃 regexp: / keyword: / DOMAIN-KEYWORD / IP-CIDR / GEOIP / USER-AGENT 等非域名规则",
          "- 统一小写，校验域名格式（需含点，排除纯 IP），去重",
          f"- 与 [china-direct-domain](https://github.com/passionsu-su/china-direct-domain) 完整版完全相同的域名会被剔除（本次 {st['removed_china_conflicts']:,} 条）",
          "- 精简版：父域名已收录时去掉其子域名",
          "- raw.githubusercontent.com 下载失败时自动改用 jsDelivr 镜像，仍失败的来源 15 秒后重试一次",
          "- 某个来源失败时用其余来源继续，失败项写入 stats.json；总数少于 20,000 时本次不提交", ""]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
