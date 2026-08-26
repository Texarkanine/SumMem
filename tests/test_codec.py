"""Identity codec: note bytes, digests, leaf-set ids, canonical trees."""

from __future__ import annotations

import hashlib
import json

import pytest
from conftest import load_summem


def test_note_file_bytes_appends_newline():
    """Note file bytes are UTF-8 of the text plus one trailing newline."""
    m = load_summem()
    assert m.note_file_bytes("hello") == b"hello\n"


def test_note_digest_is_sha256_of_file_bytes():
    """Digest is lowercase hex SHA-256 of those file bytes."""
    m = load_summem()
    raw = m.note_file_bytes("hello")
    assert m.note_digest(raw) == hashlib.sha256(raw).hexdigest()


def test_leafset_id_singleton_hashes_hex_ascii():
    """A singleton leaf-set id is SHA-256 of that digest's hex as ASCII."""
    m = load_summem()
    digest = m.note_digest(m.note_file_bytes("hello"))
    assert m.leafset_id([digest]) == hashlib.sha256(digest.encode("ascii")).hexdigest()


def test_leafset_id_sorts_and_concatenates_without_delimiter():
    """Two digests sort as ASCII, concatenate with no delimiter, then SHA-256."""
    m = load_summem()
    a = m.note_digest(m.note_file_bytes("alpha"))
    b = m.note_digest(m.note_file_bytes("beta"))
    join = "".join(sorted((a, b)))
    expected = hashlib.sha256(join.encode("ascii")).hexdigest()
    assert m.leafset_id([a, b]) == expected
    assert m.leafset_id([b, a]) == expected
    comma = hashlib.sha256(f"{min(a, b)},{max(a, b)}".encode("ascii")).hexdigest()
    assert m.leafset_id([a, b]) != comma


def test_leafset_id_hashes_utf8_chinese_file_bytes():
    """Chinese notes hash as UTF-8 file bytes, not JSON \\uXXXX escapes."""
    m = load_summem()
    raw = "你好".encode("utf-8") + b"\n"
    assert m.note_file_bytes("你好") == raw
    digest = hashlib.sha256(raw).hexdigest()
    assert m.note_digest(raw) == digest
    uxxxx = "\\u4f60\\u597d".encode("ascii") + b"\n"
    assert m.note_digest(raw) != hashlib.sha256(uxxxx).hexdigest()
    assert m.leafset_id([digest]) == hashlib.sha256(digest.encode("ascii")).hexdigest()


def test_dumps_tree_one_note_exact_bytes():
    """One note child dumps to canonical JSON with a trailing newline."""
    m = load_summem()
    tree = m.Tree(kids=[m.NoteChild(name="20260101T000000Z-aaaaaaaaaaaaaaaa", text="hello")])
    expected = (
        b'{"c":[{"name":"20260101T000000Z-aaaaaaaaaaaaaaaa","text":"hello","type":"note"}]}\n'
    )
    assert m.dumps_tree(tree) == expected


def test_dumps_tree_keeps_chinese_not_uescaped():
    """Canonical JSON keeps UTF-8 characters; it does not emit \\uXXXX."""
    m = load_summem()
    tree = m.Tree(kids=[m.NoteChild(name="n1", text="你好")])
    raw = m.dumps_tree(tree)
    assert "你好".encode("utf-8") in raw
    assert b"\\u4f60" not in raw
    assert raw.endswith(b"\n")
    as_text = raw.decode("utf-8").rstrip("\n")
    assert json.loads(as_text)["c"][0]["text"] == "你好"


def test_dumps_tree_nested_nap_exact_bytes():
    """A nap child's id is the leaf-set of the original notes in its nested tree."""
    m = load_summem()
    d1 = m.note_digest(m.note_file_bytes("alpha"))
    d2 = m.note_digest(m.note_file_bytes("beta"))
    nid = m.leafset_id([d1, d2])
    inner = m.Tree(
        kids=[
            m.NoteChild(name="a", text="alpha"),
            m.NoteChild(name="b", text="beta"),
        ]
    )
    outer = m.Tree(kids=[m.NapChild(id=nid, sum="caption", tree=inner)])
    expected = (
        '{"c":[{"id":"'
        + nid
        + '","sum":"caption","tree":{"c":[{"name":"a","text":"alpha","type":"note"},'
        '{"name":"b","text":"beta","type":"note"}]},"type":"nap"}]}\n'
    ).encode("utf-8")
    assert m.dumps_tree(outer) == expected


def test_loads_tree_round_trip():
    """loads_tree(dumps_tree(t)) round-trips note and nested nap trees."""
    m = load_summem()
    inner = m.Tree(
        kids=[
            m.NoteChild(name="a", text="alpha"),
            m.NoteChild(name="b", text="你好"),
        ]
    )
    d1 = m.note_digest(m.note_file_bytes("alpha"))
    d2 = m.note_digest(m.note_file_bytes("你好"))
    outer = m.Tree(
        kids=[
            m.NoteChild(name="c", text="gamma"),
            m.NapChild(id=m.leafset_id([d1, d2]), sum="pair", tree=inner),
        ]
    )
    assert m.loads_tree(m.dumps_tree(outer)) == outer


def test_loads_tree_ignores_unknown_fields():
    """loads_tree ignores unknown keys, including leftover v and kids beside c."""
    m = load_summem()
    tree = m.Tree(kids=[m.NoteChild(name="n1", text="hello")])
    payload = {
        "c": [{"name": "n1", "text": "hello", "type": "note", "extra": True}],
        "v": 1,
        "kids": [],
        "noise": 0,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    assert m.loads_tree(raw) == tree


def test_loads_tree_rejects_kids_key_without_c():
    """loads_tree of kids/v without c raises."""
    m = load_summem()
    with pytest.raises((KeyError, ValueError)):
        m.loads_tree(b'{"kids":[],"v":1}\n')


def test_loads_tree_rejects_child_missing_type():
    """loads_tree of a child object without type raises."""
    m = load_summem()
    with pytest.raises(ValueError):
        m.loads_tree(b'{"c":[{"name":"n1","text":"hello"}]}\n')


def test_loads_tree_rejects_unknown_type():
    """loads_tree of a child with type pack raises; it does not become a nap."""
    m = load_summem()
    raw = (
        b'{"c":[{"id":"ab","sum":"s","tree":{"c":[]},"type":"pack"}]}\n'
    )
    with pytest.raises(ValueError):
        m.loads_tree(raw)


def test_variant_tag_is_16_lowercase_hex():
    """
    variant_tag returns 16 lowercase hex characters for a pair of buffers.
    Identical inputs match. The digest is SHA-256 of the domain tag plus
    length-prefixed tree bytes and caption bytes, truncated to 16 hex.
    """
    m = load_summem()
    tree_bytes = b'{"c":[]}\n'
    caption_bytes = b"pair\n"
    tag = m.variant_tag(tree_bytes, caption_bytes)
    payload = (
        b"SumMem nap pair v1\0"
        + len(tree_bytes).to_bytes(8, "big")
        + tree_bytes
        + len(caption_bytes).to_bytes(8, "big")
        + caption_bytes
    )
    expected = hashlib.sha256(payload).hexdigest()[:16]
    assert tag == expected
    assert len(tag) == 16
    assert all(c in "0123456789abcdef" for c in tag)
    assert m.variant_tag(tree_bytes, caption_bytes) == tag


def test_variant_tag_changes_with_caption_or_tree():
    """Same tree with a different caption, or same caption with a different tree, yields a different tag."""
    m = load_summem()
    tree_a = b'{"c":[{"name":"n1","text":"alpha","type":"note"}]}\n'
    tree_b = b'{"c":[{"name":"n1","text":"beta","type":"note"}]}\n'
    cap_a = b"one\n"
    cap_b = b"two\n"
    assert m.variant_tag(tree_a, cap_a) != m.variant_tag(tree_a, cap_b)
    assert m.variant_tag(tree_a, cap_a) != m.variant_tag(tree_b, cap_a)


def test_variant_tag_length_prefixes_are_unambiguous():
    """Length prefixes keep b'ab'+b'c' from matching b'a'+b'bc'."""
    m = load_summem()
    assert m.variant_tag(b"ab", b"c") != m.variant_tag(b"a", b"bc")


def test_nap_stem_is_five_part():
    """nap_stem is {seq}-{leafset}-{grain}-{tag} and tag equals variant_tag of those bytes."""
    m = load_summem()
    seq = "20260101T000000Z-" + "a" * 16
    leafset = "b" * 64
    grain = 2
    tree_bytes = b'{"c":[]}\n'
    caption_bytes = b"pair\n"
    stem = m.nap_stem(seq, leafset, grain, tree_bytes, caption_bytes)
    tag = m.variant_tag(tree_bytes, caption_bytes)
    assert stem == f"{seq}-{leafset}-{grain}-{tag}"
    parsed = m._parse_nap_stem(stem)
    assert parsed is not None
    stamp, rand, got_leafset, got_grain, got_tag = parsed
    assert f"{stamp}-{rand}" == seq
    assert got_leafset == leafset
    assert got_grain == grain
    assert got_tag == tag


def test_parse_nap_stem_four_and_five_part():
    """Four-part stems parse with variant ''; five-part stems expose the 16-hex variant."""
    m = load_summem()
    stamp = "20260101T000000Z"
    rand = "a" * 16
    leafset = "b" * 64
    four = f"{stamp}-{rand}-{leafset}-2"
    five = f"{four}-{'c' * 16}"
    assert m._parse_nap_stem(four) == (stamp, rand, leafset, 2, "")
    assert m._parse_nap_stem(five) == (stamp, rand, leafset, 2, "c" * 16)


def test_parse_nap_stem_rejects_bad_shape():
    """3-part, 6-part, non-hex variant, and non-digit grain stems parse as None."""
    m = load_summem()
    stamp = "20260101T000000Z"
    rand = "a" * 16
    leafset = "b" * 64
    four = f"{stamp}-{rand}-{leafset}-2"
    five = f"{four}-{'c' * 16}"
    three = f"{stamp}-{rand}-{leafset}"
    six = f"{five}-{'d' * 16}"
    non_hex = f"{four}-{'g' * 16}"
    non_digit = f"{stamp}-{rand}-{leafset}-xx-{'c' * 16}"
    assert m._parse_nap_stem(three) is None
    assert m._parse_nap_stem(six) is None
    assert m._parse_nap_stem(non_hex) is None
    assert m._parse_nap_stem(non_digit) is None


def test_child_nap_stem_returns_stem_and_pair_bytes():
    """child_nap_stem serializes the NapChild once and names it with nap_stem."""
    m = load_summem()
    left = m.NoteChild(name="20260101T000001Z-" + "a" * 16, text="alpha")
    right = m.NoteChild(name="20260101T000002Z-" + "b" * 16, text="beta")
    tree = m.Tree(kids=[left, right])
    child = m.NapChild(id="c" * 64, sum="pair", tree=tree)
    stem, tree_bytes, caption_bytes = m.child_nap_stem(child)
    assert tree_bytes == m.dumps_tree(tree)
    assert caption_bytes == m.note_file_bytes("pair")
    assert stem == m.nap_stem(left.name, child.id, 2, tree_bytes, caption_bytes)
