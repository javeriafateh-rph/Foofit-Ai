"""
matching.py
Turns a user's foot profile into a ranked list of shoes, instead of the old
"must match every field exactly or show nothing" approach.

Foot-shape terminology, briefly:
- Egyptian foot: big toe is the longest, toes slope down in length after it.
  Generally comfortable in shoes with some taper/point at the front, or an
  anatomical wide box that still gives the big toe room to lead.
- Greek foot: second toe is the longest. Needs extra length/room right at
  the second toe — round or wide-anatomical toe boxes accommodate this
  better than a sharply pointed or square one.
- Roman / Square foot: toes are close to even in length. Square or
  wide-anatomical toe boxes match this shape most naturally.

These are general fit-comfort patterns, not medical facts about any
individual foot — treat them as a helpful starting point, not a diagnosis.
"""

TOE_SHAPE_TO_BOX = {
    "Egyptian (big toe longest)": ["Pointed", "Wide-Anatomical", "Round"],
    "Greek (second toe longest)": ["Round", "Wide-Anatomical", "Square"],
    "Roman / Square (toes even length)": ["Square", "Wide-Anatomical", "Round"],
    "Not sure": ["Round", "Wide-Anatomical", "Square", "Pointed"],  # no penalty either way
}

WIDTH_ORDER = ["Narrow", "Standard", "Wide", "Extra Wide"]


def _width_score(user_width: str, shoe_width: str) -> float:
    if user_width == "Not sure":
        return 0.7
    if user_width == shoe_width:
        return 1.0
    ui = WIDTH_ORDER.index(user_width)
    si = WIDTH_ORDER.index(shoe_width)
    diff = abs(ui - si)
    return max(0.0, 1.0 - diff * 0.35)


def _arch_score(user_arch: str, shoe_arch: str) -> float:
    if user_arch == "Not sure":
        return 0.7
    return 1.0 if user_arch == shoe_arch else 0.15


def _toe_score(user_toe_shape: str, shoe_toe_box: str) -> float:
    ranked = TOE_SHAPE_TO_BOX.get(user_toe_shape, TOE_SHAPE_TO_BOX["Not sure"])
    if shoe_toe_box not in ranked:
        return 0.2
    # earlier in the list = better match
    position = ranked.index(shoe_toe_box)
    return max(0.4, 1.0 - position * 0.25)


def rank_shoes(shoes: list, category: str, toe_shape: str, arch: str, width: str, top_n: int = 8):
    """
    category is a hard filter (user explicitly wants Everyday vs Sports vs Medical).
    toe_shape / arch / width are soft-scored so we always return good options,
    ranked by fit quality, instead of an empty page.
    """
    candidates = [s for s in shoes if s["category"] == category]
    scored = []
    for s in candidates:
        arch_w, toe_w, width_w = 0.4, 0.35, 0.25
        score = (
            _arch_score(arch, s["arch_support"]) * arch_w
            + _toe_score(toe_shape, s["toe_box_shape"]) * toe_w
            + _width_score(width, s["width"]) * width_w
        )
        scored.append((round(score * 100), s))
    scored.sort(key=lambda t: t[0], reverse=True)
    return scored[:top_n]
