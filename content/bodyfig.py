# MedDecode Body Map figures: original front-view (anatomical position) human outlines, male and female.
# Drawn by MedDecode from cubic curves; the right half is defined and mirrored across x=200. viewBox 0 0 400 820.

def mx(p): return None if p is None else (400 - p[0], p[1])

def seg(p0, c1, c2, p1): return (p0, c1, c2, p1)

def chain(start, rel):
    """rel: list of (c1, c2, p1); returns list of segments starting at start."""
    out = []; p = start
    for c1, c2, p1 in rel:
        out.append(seg(p, c1, c2, p1)); p = p1
    return out

def rev(segs):
    return [(s[3], s[2], s[1], s[0]) for s in reversed(segs)]

def mirror_segs(segs):
    return [tuple(mx(p) for p in s) for s in segs]

def f(p): return f'{p[0]:g} {p[1]:g}'

def path(segs, close=True, lines_to=None):
    d = f'M{f(segs[0][0])}'
    for s in segs:
        if s[1] is None: d += f' L{f(s[3])}'
        else: d += f' C{f(s[1])} {f(s[2])} {f(s[3])}'
    return d + (' Z' if close else '')

def L(p0, p1): return (p0, None, None, p1)

# ---------------------------------------------------------------- key curves (right half)
def curves(sex):
    m = sex == 'm'
    hw = 38 if m else 36            # head half-width
    nk = 18 if m else 15            # neck half-width
    sh = 306 if m else 292          # shoulder outer x
    ap = 274 if m else 266          # armpit x
    wa = 264 if m else 256          # waist x
    hp = 268 if m else 280          # hip x
    ao = 0 if m else -12            # arm x offset
    C = {}
    C['head'] = chain((200, 14), [((200+hw*.58, 14), (200+hw, 32), (200+hw, 60)),
                                  ((200+hw, 82), (200+hw-6, 100), (200+nk-2, 114))])
    C['neck'] = chain((200+nk-2, 114), [((200+nk-1, 124), (200+nk-1, 132), (200+nk, 140))])
    C['shoulder'] = chain((200+nk, 140), [((236, 150), (sh-44, 152), (sh-26, 160)),
                                         ((sh-8, 168), (sh, 186), (sh, 208))])
    C['arm_out'] = chain((sh, 208), [((sh+4+ao*0, 240), (316+ao, 272), (320+ao, 300)),
                                     ((326+ao, 335), (332+ao, 370), (336+ao, 400))])
    C['hand'] = chain((336+ao, 400), [((344+ao, 408), (352+ao, 424), (351+ao, 436)),      # thumb (points out in anatomical position)
                                      ((350+ao, 444), (343+ao, 443), (341+ao, 436)),
                                      ((345+ao, 452), (343+ao, 468), (337+ao, 478)),      # fingers
                                      ((331+ao, 487), (320+ao, 484), (318+ao, 472)),
                                      ((314+ao, 452), (313+ao, 426), (316+ao, 402))])
    C['arm_in'] = chain((316+ao, 402), [((310+ao, 370), (300+ao, 335), (296+ao, 302)),
                                        ((292+ao, 270), (ap+10, 244), (ap, 226))])
    if m:
        C['torso'] = chain((ap, 226), [((ap-2, 262), (wa, 300), (wa-2, 330)),
                                       ((wa-4, 356), (hp-2, 380), (hp, 404))])
    else:
        C['torso'] = chain((ap, 226), [((ap+2, 262), (wa+2, 296), (wa, 328)),
                                       ((wa-2, 356), (hp-4, 384), (hp, 412))])
    hip = C['torso'][-1][3]
    C['leg_out'] = chain(hip, [((hip[0]+4, 450), (hip[0]-2, 500), (262 if m else 264, 540)),
                               ((258, 560), (256, 575), (256, 590)),
                               ((264, 620), (264, 660), (254, 700)),
                               ((250, 720), (246, 735), (246, 750))])
    C['foot'] = chain((246, 750), [((256, 766), (262, 784), (254, 796)),
                                   ((244, 802), (222, 802), (214, 796)),
                                   ((210, 784), (212, 766), (214, 750))])
    C['leg_in'] = chain((214, 750), [((212, 724), (210, 700), (210, 680)),
                                     ((206, 650), (208, 620), (212, 594)),
                                     ((212, 560), (206, 512), (202, 470)),
                                     ((201, 466), (200, 464), (200, 462))])
    C['chin'] = [seg((200+nk-2, 114), (210, 121), (190, 121), (200-nk+2, 114))]
    C['hw'] = hw; C['sex'] = sex
    return C

ORDER = ['head', 'neck', 'shoulder', 'arm_out', 'hand', 'arm_in', 'torso', 'leg_out', 'foot', 'leg_in']

def outline(C):
    right = [s for k in ORDER for s in C[k]]
    return path(right + rev(mirror_segs(right)))

def both(d_right_segs):
    return path(d_right_segs) + ' ' + path(mirror_segs(d_right_segs))

def pieces(C):
    """Closed regions used for fills and tappable areas."""
    P = {}
    head = C['head'] + C['chin'] + rev(mirror_segs(C['head']))
    P['head'] = path(head)
    nb = C['neck'][-1][3][0]
    P['neck'] = f'M{400-nb-1:g} 108 L{nb+1:g} 108 L{nb+1:g} 150 L{400-nb-1:g} 150 Z'
    sh_top = C['shoulder'][0][0]
    ap = C['arm_in'][-1][3]
    hip = C['torso'][-1][3]
    # torso: shoulder line, down the side to the hip, across the groin, and back up the other side
    tr = C['shoulder'] + [L(C['shoulder'][-1][3], ap)] + C['torso'] + [seg(hip, (hip[0]-6, 436), (232, 462), (200, 464))]
    P['torso'] = path(tr + rev(mirror_segs(tr)))
    arm = C['shoulder'][1:] + C['arm_out'] + C['hand'] + C['arm_in']
    arm = [L(C['shoulder'][1][0], C['shoulder'][1][0])] + arm + [L(ap, C['shoulder'][1][0])]
    P['arm_r'] = path(arm)
    P['arm'] = path(arm) + ' ' + path(mirror_segs(arm))
    upper = C['shoulder'][1:] + C['arm_out'] + [L(C['arm_out'][-1][3], C['arm_in'][0][0])] + C['arm_in'] + [L(ap, C['shoulder'][1][0])]
    P['upperarm'] = path(upper) + ' ' + path(mirror_segs(upper))
    hand = C['hand'] + [L(C['hand'][-1][3], C['hand'][0][0])]
    P['hands'] = path(hand) + ' ' + path(mirror_segs(hand))
    leg = C['leg_out'] + C['foot'] + C['leg_in'] + [L((200, 462), (200, 420)), L((200, 420), hip)]
    P['legs'] = path(leg) + ' ' + path(mirror_segs(leg))
    foot = C['foot'] + [L(C['foot'][-1][3], C['foot'][0][0])]
    P['feet'] = path(foot) + ' ' + path(mirror_segs(foot))
    return P

def details(C):
    """Decorative surface lines (collarbones, chest, navel, knees): not tappable."""
    m = C['sex'] == 'm'
    d = []
    clav = [seg((206, 160), (226, 164), (250, 160), (272 if m else 262, 168))]
    d.append(both(clav).replace(' Z', ''))
    if m:
        pec = [seg((206, 252), (226, 260), (252, 256), (264, 236))]
        d.append(both(pec).replace(' Z', ''))
    else:
        br = [seg((210, 228), (206, 258), (240, 274), (258, 246))]
        d.append(both(br).replace(' Z', ''))
    knee = [seg((222, 590), (230, 600), (244, 600), (250, 590))]
    d.append(both(knee).replace(' Z', ''))
    return ''.join(f'<path d="{x}"/>' for x in d) + '<circle cx="200" cy="356" r="2.5"/>'

def pelvis(sex):
    """Context outline of the hip bones (not tappable): the female pelvis is wider with a wider pubic arch."""
    if sex == 'm':
        r = [seg((212, 394), (222, 380), (236, 366), (250, 364)), seg((250, 364), (262, 366), (264, 380), (258, 398)),
             seg((258, 398), (254, 410), (248, 418), (244, 424)), seg((244, 424), (232, 432), (216, 438), (204, 440))]
    else:
        r = [seg((214, 396), (226, 382), (244, 368), (262, 368)), seg((262, 368), (276, 370), (278, 386), (270, 402)),
             seg((270, 402), (264, 412), (258, 420), (252, 426)), seg((252, 426), (238, 432), (224, 438), (210, 440))]
    return path(r, close=False) + ' ' + path(mirror_segs(r), close=False)

FIG = {s: curves(s) for s in ('m', 'f')}
OUTLINE = {s: outline(FIG[s]) for s in FIG}
PIECES = {s: pieces(FIG[s]) for s in FIG}
DETAILS = {s: details(FIG[s]) for s in FIG}
PELVIS = {s: pelvis(s) for s in FIG}
