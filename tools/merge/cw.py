"""Minimal Clausewitz script parser that keeps exact source spans.

parse(text) -> list[Node] for one level. Node fields:
  key, op, kind ('block'|'value'|'bare'), start, end (span of whole entry
  without leading comments/whitespace), bstart, bend (inside braces for blocks),
  vstart, vend (value span for 'value' nodes), lead (span start incl. leading
  comments / blank lines since previous node end).
"""
import re

class Node:
    __slots__ = ('key', 'op', 'kind', 'start', 'end', 'bstart', 'bend', 'vstart', 'vend', 'lead')

    def __repr__(self):
        return f'<{self.kind} {self.key!r} {self.start}:{self.end}>'


def _skip_ws_comments(t, i, n):
    while i < n:
        c = t[i]
        if c in ' \t\r\n﻿':
            i += 1
        elif c == '#':
            while i < n and t[i] != '\n':
                i += 1
        else:
            break
    return i


def _read_token(t, i, n):
    """read a word/quoted string starting at i; returns end index"""
    if t[i] == '"':
        j = i + 1
        while j < n and t[j] != '"':
            j += 1
        return min(j + 1, n)
    j = i
    while j < n and t[j] not in ' \t\r\n={}#"':
        j += 1
    if j == i:  # lone odd char
        j = i + 1
    return j


def find_close(t, i, n):
    """i points just after '{'; return index of matching '}' (or n)"""
    depth = 1
    while i < n:
        c = t[i]
        if c == '#':
            while i < n and t[i] != '\n':
                i += 1
            continue
        if c == '"':
            i += 1
            while i < n and t[i] != '"':
                i += 1
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n


def parse(t, s=0, e=None):
    n = len(t) if e is None else e
    out = []
    i = s
    prev_end = s
    while True:
        i = _skip_ws_comments(t, i, n)
        if i >= n:
            break
        c = t[i]
        if c == '}':
            i += 1
            continue
        if c == '{':
            # anonymous block (e.g. in lists)
            nd = Node()
            nd.key = ''; nd.op = ''; nd.kind = 'block'
            nd.start = i; nd.bstart = i + 1
            nd.bend = find_close(t, i + 1, n)
            nd.end = min(nd.bend + 1, n)
            nd.vstart = nd.vend = -1
            nd.lead = prev_end
            out.append(nd); i = nd.end; prev_end = i
            continue
        ks = i
        ke = _read_token(t, i, n)
        key = t[ks:ke]
        j = _skip_ws_comments(t, ke, n)
        nd = Node()
        nd.key = key; nd.start = ks; nd.lead = prev_end
        if j < n and t[j] in '=<>' :
            # operator
            oj = j
            if t[j] in '<>' and j + 1 < n and t[j + 1] == '=':
                j += 2
            else:
                j += 1
            nd.op = t[oj:j]
            j = _skip_ws_comments(t, j, n)
            if j < n and t[j] == '{':
                nd.kind = 'block'
                nd.bstart = j + 1
                nd.bend = find_close(t, j + 1, n)
                nd.end = min(nd.bend + 1, n)
                nd.vstart = nd.vend = -1
            elif j < n:
                ve = _read_token(t, j, n)
                nd.kind = 'value'
                nd.vstart, nd.vend = j, ve
                nd.end = ve
                nd.bstart = nd.bend = -1
                # handle   key = rgb { 1 2 3 }  /  hsv {}
                k = _skip_ws_comments(t, ve, n)
                if k < n and t[k] == '{' and t[j:ve] in ('rgb', 'hsv', 'list', 'range'):
                    be = find_close(t, k + 1, n)
                    nd.kind = 'value'
                    nd.end = min(be + 1, n)
                    nd.vend = nd.end
            else:
                nd.kind = 'value'; nd.vstart = nd.vend = n; nd.end = n
                nd.bstart = nd.bend = -1
        else:
            nd.op = ''
            nd.kind = 'bare'
            nd.end = ke
            nd.vstart = nd.vend = -1
            nd.bstart = nd.bend = -1
        out.append(nd)
        i = nd.end
        prev_end = i
    return out


def children(t, nd):
    return parse(t, nd.bstart, nd.bend) if nd.kind == 'block' else []


def get_scalar(t, nd, key):
    """first scalar value of `key` among direct children"""
    for c in children(t, nd):
        if c.kind == 'value' and c.key == key:
            return t[c.vstart:c.vend].strip('"')
    return None
