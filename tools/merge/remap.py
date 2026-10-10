"""Strip references to provinces that do not exist on the Ante Bellum map (id > MAXA)."""
import re
import cw

MAXA = 5210
MAXV = 8911


def oor(s):
    s = s.strip().strip('"')
    return s.isdigit() and MAXA < int(s) <= MAXV

TRIG_SCALAR = {'owns', 'owns_core_province', 'owns_or_non_sovereign_subject_of', 'owns_or_vassal_of',
               'has_discovered', 'controls', 'capital', 'province_id', 'is_core', 'is_capital',
               'owns_or_subject_of', 'is_claimed_by_country', 'has_building_in_province'}
EFF_SCALAR = {'add_permanent_claim', 'add_claim', 'set_capital', 'goto', 'add_core', 'remove_claim',
              'remove_core', 'change_owner', 'discover_province', 'add_to_trade_company', 'cede_province',
              'add_unit_construction', 'destroy_great_project'}
TRIG_BLOCKS = {'limit', 'trigger', 'potential', 'allow', 'can_select', 'provinces_to_highlight', 'ai_will_do',
               'mean_time_to_happen', 'can_fire', 'visible', 'available', 'trigger_if', 'trigger_else',
               'trigger_else_if', 'custom_trigger_tooltip', 'modifier', 'ai_importance', 'ai_acceptance',
               'will_lose_if_removed', 'can_use_authority', 'is_valid', 'valid', 'can_be_removed'}
EFF_BLOCKS = {'immediate', 'effect', 'option', 'after', 'on_start', 'on_end', 'on_progress', 'hidden_effect',
              'tooltip', 'on_completion', 'on_removal', 'on_add', 'on_remove', 'on_discover'}
SKIP_PARENTS = {'random_list', 'random', 'weight', 'chance'}
LIST_KEYS = {'provinces', 'members', 'path', 'holy_sites', 'province_ids'}
# statements wrapping `province = N`
PROV_WRAPPERS = {'add_permanent_claim_province', 'add_claim_province', 'add_province_claim',
                 'remove_province_claim', 'discover_province'}


def ctx(path):
    for k in reversed(path):
        if k in TRIG_BLOCKS:
            return 'T'
        if k in EFF_BLOCKS:
            return 'E'
    return 'E'


class Remap:
    def __init__(self):
        self.removed_nodes = set()  # trade node names removed
        self.stats = {}

    def bump(self, k):
        self.stats[k] = self.stats.get(k, 0) + 1

    def walk(self, t, nodes, path, edits, top=False, fname=''):
        for nd in nodes:
            key = nd.key
            parent = path[-1] if path else ''
            # --- province-scope block
            if nd.kind == 'block' and key.isdigit() and oor(key) and parent not in SKIP_PARENTS:
                self._replace(t, nd, ctx(path), edits, f'province {key}')
                continue
            if nd.kind == 'value' and key in TRIG_SCALAR | EFF_SCALAR and oor(t[nd.vstart:nd.vend]):
                c = 'T' if key in TRIG_SCALAR and key not in EFF_SCALAR else ('E' if key in EFF_SCALAR and key not in TRIG_SCALAR else ctx(path))
                self._replace(t, nd, c, edits, f'{key} = {t[nd.vstart:nd.vend]}')
                continue
            if nd.kind == 'value' and key == 'province' and oor(t[nd.vstart:nd.vend]):
                # inside wrapper block handled at the wrapper; stray -> drop
                self._replace(t, nd, ctx(path), edits, 'province')
                continue
            if nd.kind == 'block':
                if key in PROV_WRAPPERS:
                    ch = cw.children(t, nd)
                    if any(c.key == 'province' and c.kind == 'value' and oor(t[c.vstart:c.vend]) for c in ch):
                        self._replace(t, nd, ctx(path), edits, key)
                        continue
                if key in LIST_KEYS:
                    self._fix_list(t, nd, edits)
                    continue
                ch = cw.children(t, nd)
                self.walk(t, ch, path + [key], edits, False, fname)

    def _replace(self, t, nd, c, edits, what):
        self.bump('trigger->always=no' if c == 'T' else 'effect removed')
        j = t.find(chr(10), nd.end)
        rest = t[nd.end:j if j >= 0 else len(t)]
        tail_ok = rest.strip() == ''
        note = f' # [VU] {what} not on Ante Bellum map' if tail_ok else ''
        if c == 'T':
            edits.append((nd.start, nd.end, 'always = no' + note))
        else:
            edits.append((nd.start, nd.end, ('# [VU] removed: ' + what + ' (not on Ante Bellum map)') if tail_ok else ''))

    def _fix_list(self, t, nd, edits):
        body = t[nd.bstart:nd.bend]
        if '{' in body:
            return
        def sub(m):
            if oor(m.group(0)):
                self.bump('list ids removed')
                return ''
            return m.group(0)
        nb = re.sub(r'(?<![\w.])\d+(?![\w.])', sub, body)
        if nb != body:
            nb = re.sub(r'[ \t]{2,}', ' ', nb)
            edits.append((nd.bstart, nd.bend, nb))


def apply_edits(t, edits):
    edits = sorted(edits, key=lambda e: e[0], reverse=True)
    for e in edits:
        s, en, rep = e[0], e[1], e[2]
        t = t[:s] + rep + t[en:]
    return t


_STR = re.compile(r'"[^"\n]*"')
_TRIG = re.compile(r'\b(' + '|'.join(sorted(TRIG_SCALAR)) + r')\s*=\s*(\d+)\b')


def fix_strings(t, rm):
    """province triggers embedded in quoted strings (e.g. simple_dynamic_effect limits)"""
    def sub_str(m):
        s = m.group(0)
        if '=' not in s:
            return s
        def sub_t(mm):
            if oor(mm.group(2)):
                rm.bump('embedded string triggers')
                return 'always = no'
            return mm.group(0)
        return _TRIG.sub(sub_t, s)
    return _STR.sub(sub_str, t)


def remap_text(t, rm, fname=''):
    nodes = cw.parse(t)
    edits = []
    rm.walk(t, nodes, [], edits, True, fname)
    if edits:
        t = apply_edits(t, edits)
    return fix_strings(t, rm)


# ---- tradenodes -----------------------------------------------------------
def tradenode_pass1(t):
    """returns names of nodes whose location is off-map"""
    gone = set()
    for nd in cw.parse(t):
        if nd.kind != 'block':
            continue
        loc = cw.get_scalar(t, nd, 'location')
        if loc is not None and oor(loc):
            gone.add(nd.key)
    return gone


def tradenode_pass2(t, gone, rm):
    edits = []
    for nd in cw.parse(t):
        if nd.kind != 'block':
            continue
        if nd.key in gone:
            edits.append((nd.start, nd.end, f'# [VU] trade node {nd.key} removed: location not on Ante Bellum map'))
            rm.bump('tradenodes removed')
            continue
        for c in cw.children(t, nd):
            if c.kind == 'block' and c.key == 'outgoing':
                nm = cw.get_scalar(t, c, 'name')
                if nm in gone:
                    edits.append((c.start, c.end, '# [VU] outgoing link removed (target node off map)'))
                    rm.bump('tradenode links removed')
                    continue
                for g in cw.children(t, c):
                    if g.kind == 'block' and g.key == 'path':
                        rm._fix_list(t, g, edits)
            elif c.kind == 'block' and c.key == 'members':
                rm._fix_list(t, c, edits)
    return apply_edits(t, edits)


def greatproj_pass(t, rm):
    """drop monuments whose starting province is not on the Ante Bellum map"""
    edits = []
    for nd in cw.parse(t):
        if nd.kind != 'block':
            continue
        st = cw.get_scalar(t, nd, 'start')
        if st is not None and oor(st):
            edits.append((nd.start, nd.end, f'# [VU] great project {nd.key} removed: start province {st} not on Ante Bellum map'))
            rm.bump('great projects removed')
    return apply_edits(t, edits) if edits else t
