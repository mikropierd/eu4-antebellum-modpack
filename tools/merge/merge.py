import os, re, sys, shutil, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import cw, remap

V = '/home/user/Victorum-Enhanced'
A = '/home/user/eu4-antebellum-modpack'
INCLUDE = ['common', 'decisions', 'events', 'missions', 'interface', 'localisation', 'customizable_localization']
EXCLUDE_PREFIX = ['common/bookmarks/']
WRAPPERS = {'guiTypes', 'spriteTypes', 'objectTypes', 'positionTypes', 'bitmapfonts', 'fonts', 'lightTypes',
            'country_decisions', 'province_decisions'}
TEXT_EXT = ('.txt', '.gui', '.gfx')
REMAP_DIRS = ('common/', 'decisions/', 'events/', 'missions/')

rm = remap.Remap()
report = collections.defaultdict(list)


def rd(p):
    return open(p, 'rb').read().decode('latin-1')


def wr(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(t.encode('latin-1'))


def keyof(t, nd):
    k = nd.key
    if nd.kind == 'bare':
        return (k, 'bare')
    if k.startswith('@'):
        return (k,)
    if nd.kind == 'value':
        return (k, t[nd.vstart:nd.vend]) if k in ('namespace', 'defined', 'texturefile') else (k,)
    for sub in ('id', 'name'):
        v = cw.get_scalar(t, nd, sub)
        if v is not None:
            return (k, v)
    return (k,)


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'#[^\n]*', '', s)).strip()


TOK = re.compile(r"[A-Za-z_][\w.\-']{2,}")
AONLY = set()


def a_ids(text):
    out = set()
    for w in TOK.findall(text):
        if w in AONLY or ('.' in w and w.split('.')[0] in AONLY):
            out.add(w)
    return out


def inject(vt, vn, at, an):
    """return new text of V block vn with A-specific children from an re-added"""
    vch, ach = cw.parse(vt, vn.bstart, vn.bend), cw.parse(at, an.bstart, an.bend)
    vbody = vt[vn.bstart:vn.bend]
    vnorm = norm(vbody)
    edits, adds = [], []
    for a in ach:
        atext = at[a.start:a.end]
        ids = a_ids(atext)
        if not ids:
            continue
        if not {i for i in ids if i not in vbody}:
            continue
        if norm(atext) in vnorm:
            continue
        ka = keyof(at, a)
        cands = [v for v in vch if keyof(vt, v) == ka]
        if a.kind == 'block' and len(cands) == 1 and cands[0].kind == 'block' and a.key != '':
            new = inject(vt, cands[0], at, a)
            if new != vt[cands[0].bstart:cands[0].bend]:
                edits.append((cands[0].bstart, cands[0].bend, new))
        else:
            ls = at.rfind(chr(10), 0, a.start) + 1
            indent = re.match(r'[ 	]*', at[ls:a.start]).group(0) if not at[ls:a.start].strip() else '	'
            adds.append(indent + atext)
            report['injected'].append((vn.key, a.key))
    out = vbody
    for s, e, r in sorted(edits, key=lambda x: -x[0]):
        out = out[:s - vn.bstart] + r + out[e - vn.bstart:]
    if adds:
        trail = out[len(out.rstrip()):]
        out = out.rstrip() + chr(10) + chr(10).join(adds) + (trail if chr(10) in trail else chr(10))
    return out


def block_merge(vt, at, fname, depth=0):
    """V wins on equal keys; A-only top-level entries are appended."""
    vn, an = cw.parse(vt), cw.parse(at)
    def occ(txt, nodes):
        seen = collections.Counter(); res = []
        for n in nodes:
            k = keyof(txt, n); seen[k] += 1
            res.append(k if seen[k] == 1 else k + (seen[k],))
        return res
    vks = occ(vt, vn); aks = occ(at, an)
    vkeys = dict(zip(vks, vn))
    extras, edits = [], []
    no_extras = fname.startswith('common/technologies/')
    # wrapper recursion (same wrapper key in both, single or many)
    avail_w = {n.key: n for n in vn if n.kind == 'block' and n.key in WRAPPERS}
    for n, k in zip(an, aks):
        if n.kind == 'block' and n.key in WRAPPERS and n.key in avail_w and depth < 2:
            w = avail_w[n.key]
            inner_v = vt[w.bstart:w.bend]
            inner_a = at[n.bstart:n.bend]
            merged = block_merge(inner_v, inner_a, fname, depth + 1)
            edits.append((w.bstart, w.bend, merged))
            continue
        if k in vkeys:
            vnode = vkeys[k]
            if norm(vt[vnode.start:vnode.end]) != norm(at[n.start:n.end]):
                report['v_won'].append((fname, ' '.join(map(str, k))))
                if vnode.kind == 'block' and n.kind == 'block':
                    new = inject(vt, vnode, at, n)
                    if new != vt[vnode.bstart:vnode.bend]:
                        edits.append((vnode.bstart, vnode.bend, new))
            continue
        if no_extras:
            continue
        seg = at[n.lead:n.end].strip('\r\n')
        extras.append(seg)
        report['a_only'].append((fname, ' '.join(map(str, k))))
    out = vt
    for s, e, r in sorted(edits, key=lambda x: -x[0]):
        out = out[:s] + r + out[e:]
    if extras:
        out = out.rstrip() + '\n\n' + ('# ===== Ante Bellum additions (not in Victorum) =====\n' if depth == 0 else '') + '\n\n'.join(extras) + '\n'
        if depth > 0:
            out = '\n' + out.lstrip('\n')
    return out


def yml_parse(t):
    lines = t.splitlines()
    keys = {}
    for i, l in enumerate(lines):
        m = re.match(r'^\s*([\w.\-\']+):\d*\s', l)
        if m:
            keys[m.group(1)] = i
    return lines, keys


def yml_merge(vt, at, fname):
    vl, vk = yml_parse(vt)
    al, ak = yml_parse(at)
    add = []
    for k, i in ak.items():
        if k not in vk:
            add.append(al[i])
        elif al[i].strip() != vl[vk[k]].strip():
            report['yml_conflict'].append((fname, k))
    out = vt.rstrip('\n')
    if add:
        out += '\n\n # ===== Ante Bellum additions =====\n' + '\n'.join(add)
    return out + '\n'


def rdu(p):
    return open(p, 'rb').read().decode('utf-8-sig')


def wru(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(('﻿' + t).encode('utf-8'))


def load_aonly():
    import subprocess
    tok = TOK
    vtok = set()
    for d in ['common', 'decisions', 'events', 'missions', 'interface']:
        for root, _, fs in os.walk(V + '/' + d):
            for f in fs:
                if f.endswith(('.txt', '.gui', '.gfx')):
                    vtok.update(tok.findall(rd(os.path.join(root, f))))
    files = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=A, capture_output=True, text=True).stdout.split(chr(10))
    for rel in files:
        if rel.split('/')[0] in ('common', 'decisions', 'events', 'missions', 'interface') and rel.endswith(('.txt', '.gui', '.gfx')):
            t = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=A, capture_output=True).stdout.decode('latin-1')
            for nd in cw.parse(t):
                k = nd.key
                if nd.kind == 'block' and k not in vtok and len(k) > 3 and not k.isdigit():
                    AONLY.add(k)
                if nd.kind == 'block':
                    for sub in ('id', 'name'):
                        v = cw.get_scalar(t, nd, sub)
                        if v and v not in vtok and not v.isdigit():
                            AONLY.add(v)
                if nd.kind == 'value' and k == 'namespace':
                    AONLY.add(t[nd.vstart:nd.vend])



RETAG = {}


def pick_retags():
    """V tags that collide with different countries in the Ante Bellum modpack get a new tag in V content."""
    import subprocess
    def tags(root, git):
        d = {}
        base = 'common/country_tags'
        if git:
            fl = [l for l in subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD', base], cwd=root, capture_output=True, text=True).stdout.split(chr(10)) if l]
            get = lambda f: subprocess.run(['git', 'show', 'HEAD:' + f], cwd=root, capture_output=True).stdout.decode('latin-1')
        else:
            fl = [os.path.join(base, f) for f in os.listdir(os.path.join(root, base))]
            get = lambda f: rd(os.path.join(root, f))
        for f in fl:
            for l in get(f).splitlines():
                m = re.match(r'^\s*([A-Z0-9]{3})\s*=\s*"?([^"\s#]+)', l)
                if m:
                    d[m.group(1)] = m.group(2).lower()
        return d
    a, v = tags(A, True), tags(V, False)
    used = set(a) | set(v)
    col = [t for t in a if t in v and a[t] != v[t]]
    cand = iter(c for c in ['XC%s' % ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] if c not in used)
    for t in sorted(col):
        RETAG[t] = next(cand)
    report['retag'] = dict(RETAG)


def retag_txt(t):
    for o, n in RETAG.items():
        t = re.sub(r'(?<![A-Za-z0-9])' + o + r'(?![A-Za-z0-9])', n, t)
    return t


def retag_yml(t):
    for o, n in RETAG.items():
        t = re.sub(r'(?m)^(\s*)' + o + r'(?=(_\w+)?:)', lambda m: m.group(1) + n, t)
    return t


def cross_dups():
    """same key defined in an A-origin file and a Victorum-origin file: Victorum wins, A-specific extras injected"""
    W = {'country_decisions', 'province_decisions'}
    defs = collections.defaultdict(lambda: collections.defaultdict(list))
    for root, _, fs in os.walk(A):
        if '/.git' in root:
            continue
        for f in fs:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, A)
            parts = rel.split('/')
            if parts[0] not in ('common', 'missions') or not rel.endswith('.txt') or len(parts) < 3 and parts[0] == 'common':
                continue
            d = '/'.join(parts[:2]) if parts[0] == 'common' else 'missions'
            if d in ('common/technologies', 'common/countries', 'common/country_tags', 'common/province_names', 'common/cultures', 'common/on_actions', 'common/bookmarks'):
                continue
            t = rd(p)
            for n in cw.parse(t):
                if n.kind == 'block':
                    defs[d][n.key].append(rel)
    done = 0
    for d, m in defs.items():
        for k, fs in m.items():
            fs = sorted(set(fs))
            af = [f for f in fs if not os.path.exists(os.path.join(V, f))]
            vf = [f for f in fs if os.path.exists(os.path.join(V, f))]
            if not af or not vf:
                continue
            vp = os.path.join(A, vf[0]); vt = rd(vp)
            vnode = next((n for n in cw.parse(vt) if n.kind == 'block' and n.key == k), None)
            if vnode is None:
                continue
            for f in af:
                ap = os.path.join(A, f); at = rd(ap)
                anode = next((n for n in cw.parse(at) if n.kind == 'block' and n.key == k), None)
                if anode is None:
                    continue
                new = inject(vt, vnode, at, anode)
                if new != vt[vnode.bstart:vnode.bend]:
                    vt = vt[:vnode.bstart] + new + vt[vnode.bend:]
                    vnode = next(n for n in cw.parse(vt) if n.kind == 'block' and n.key == k)
                at = at[:anode.start] + '# [merge] ' + k + ' now defined in ' + vf[0] + ' (Victorum wins; Ante Bellum-specific parts merged there)' + at[anode.end:]
                wr(ap, at)
                report['cross_dups'].append((d, k, f, vf[0]))
                done += 1
            wr(vp, vt)
    return done


GFX_PREFIX = re.compile(r'(?i)^(vu_|me_|_me_|gme_|ge_|000_|zzz_expanded|holyorder|macrobuild|tcp_|general_stuff|missionicons_vu)')


def copy_gfx():
    lower = {}
    for root, _, fs in os.walk(V + '/gfx'):
        for f in fs:
            p = os.path.join(root, f)
            lower[os.path.relpath(p, V).lower()] = os.path.relpath(p, V)
    n = size = 0
    seen = set()
    for f in sorted(os.listdir(V + '/interface')):
        if not f.endswith('.gfx') or not GFX_PREFIX.match(f):
            continue
        t = rd(os.path.join(V, 'interface', f))
        for m in re.finditer(r'(?i)(?:texturefile|effectfile|textureFile\d*)\s*=\s*"([^"]+)"', t):
            r = m.group(1).replace(chr(92), '/')
            real = lower.get(r.lower())
            if not real or real in seen or real.startswith(('gfx/models', 'gfx/loadingscreens')):
                continue
            seen.add(real)
            dst = os.path.join(A, real)
            if os.path.exists(dst):
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(V, real), dst)
            n += 1; size += os.path.getsize(dst)
    # flags
    fl = 0
    for f in os.listdir(V + '/gfx/flags'):
        src = os.path.join(V, 'gfx/flags', f)
        if not os.path.isfile(src):
            continue
        stem = f.split('.')[0]
        new = f
        for o, nw in RETAG.items():
            if stem == o or stem.startswith(o + '_'):
                new = nw + f[len(o):]
        dst = os.path.join(A, 'gfx/flags', new)
        if os.path.exists(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst); fl += 1; size += os.path.getsize(dst)
    print('gfx textures', n, 'flags', fl, 'MB', round(size / 1e6, 1))



def gate_missions():
    """Ante Bellum mission trees take precedence for the same tag+slot; Victorum trees get NOT = { <AB potential> }."""
    def series(rel):
        t = rd(os.path.join(A, rel)); out = []
        for n in cw.parse(t):
            if n.kind != 'block':
                continue
            slot = cw.get_scalar(t, n, 'slot')
            if slot is None:
                continue
            pot = next((c for c in cw.children(t, n) if c.key == 'potential' and c.kind == 'block'), None)
            tags = set()
            if pot:
                ptxt = t[pot.bstart:pot.bend]
                tags = set(re.findall(r'(?:original_)?tag\s*=\s*([A-Z0-9]{3})', ptxt))
            out.append((n, slot, tags, pot))
        return t, out
    a_ser = collections.defaultdict(list)
    mfiles = [os.path.join('missions', f) for f in os.listdir(os.path.join(A, 'missions')) if f.endswith('.txt')]
    for rel in mfiles:
        if os.path.exists(os.path.join(V, rel)):
            continue
        t, ss = series(rel)
        for n, slot, tags, pot in ss:
            if pot is None or not tags:
                continue
            inner = t[pot.bstart:pot.bend].strip()
            for tg in tags:
                a_ser[(tg, slot)].append((n.key, inner))
    done = 0
    for rel in mfiles:
        if not os.path.exists(os.path.join(V, rel)):
            continue
        t, ss = series(rel)
        edits = []
        for n, slot, tags, pot in ss:
            if pot is None:
                continue
            nots = {}
            for tg in tags:
                for k, inner in a_ser.get((tg, slot), []):
                    nots[k] = inner
            if not nots:
                continue
            add = ''.join(chr(10) + '		# [merge] Ante Bellum tree ' + k + ' takes precedence' + chr(10) + '		NOT = {' + chr(10) + inner + chr(10) + '		}' for k, inner in nots.items()) + chr(10) + '	'
            edits.append((pot.bend, pot.bend, add))
            done += 1
            report['gated'].append((rel, n.key, sorted(nots)))
        for s, e, r in sorted(edits, key=lambda x: -x[0]):
            t = t[:s] + r + t[e:]
        if edits:
            wr(os.path.join(A, rel), t)
    return done


def main():
    load_aonly()
    pick_retags()
    gone = set()
    # pass 1: trade nodes removed
    for root, _, fs in os.walk(V + '/common/tradenodes'):
        for f in fs:
            gone |= remap.tradenode_pass1(rd(os.path.join(root, f)))
    report['tradenodes_removed'] = sorted(gone)
    files = []
    for d in INCLUDE:
        for root, _, fs in os.walk(os.path.join(V, d)):
            for f in fs:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, V)
                if any(rel.startswith(x) for x in EXCLUDE_PREFIX):
                    continue
                files.append(rel)
    files.sort()
    n = collections.Counter()
    for rel in files:
        vp, ap = os.path.join(V, rel), os.path.join(A, rel)
        ext = os.path.splitext(rel)[1].lower()
        exists = os.path.exists(ap)
        if ext == '.yml':
            vt = retag_yml(rdu(vp))
            if exists:
                wru(ap, yml_merge(vt, rdu(ap), rel)); n['yml_merged'] += 1
            else:
                wru(ap, vt); n['yml_new'] += 1
            continue
        if ext in TEXT_EXT or ext == '.lua':
            vt = rd(vp)
            if rel.startswith(('common/', 'decisions/', 'events/', 'missions/')) and ext == '.txt':
                vt = retag_txt(vt)
            if rel.startswith(REMAP_DIRS) and ext == '.txt':
                if rel.startswith('common/tradenodes/'):
                    vt = remap.tradenode_pass2(vt, gone, rm)
                elif rel.startswith('common/great_projects/'):
                    vt = remap.remap_text(remap.greatproj_pass(vt, rm), rm, rel)
                else:
                    vt = remap.remap_text(vt, rm, rel)
                    if rel.startswith('common/province_names/'):
                        vt = strip_province_names(vt)
            if exists and ext != '.lua':
                out = block_merge(vt, rd(ap), rel); n['merged'] += 1
            else:
                out = vt; n['new' if not exists else 'replaced'] += 1
            wr(ap, out)
            continue
        os.makedirs(os.path.dirname(ap), exist_ok=True)
        shutil.copyfile(vp, ap); n['raw'] += 1
    n['cross_dups'] = cross_dups()
    n['gated_series'] = gate_missions()
    lua = os.path.join(A, 'common/defines/01_tlw.lua')
    if os.path.exists(lua):
        os.rename(lua, os.path.join(A, 'common/defines/zz_01_tlw.lua'))
    copy_gfx()
    json.dump({k: v for k, v in report.items()}, open('/tmp/claude-0/-home-user/1f71c29d-3371-549a-adfe-f028567f4302/scratchpad/merge_report.json', 'w'), indent=1)
    print(dict(n)); print(rm.stats)
    print({k: len(v) for k, v in report.items()})


def strip_province_names(t):
    def sub(m):
        return '' if remap.oor(m.group(2)) else m.group(0)
    return re.sub(r'(?m)^([ \t]*)(\d+)[ \t]*=[ \t]*"[^"\n]*"[^\n]*(?:\n|\Z)', lambda m: '' if remap.oor(m.group(2)) else m.group(0), t)


if __name__ == '__main__':
    main()
