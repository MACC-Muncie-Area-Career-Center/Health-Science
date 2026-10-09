# Body Map spots (v2): places on MedDecode's original male and female figures (bodyfig.py, viewBox 0 0 400 820),
# each with the master-list roots that name it. Layers keep overlapping organs apart.
# A spot's shape is a string (same on both figures) or {'m':..., 'f':...}; 'sex' limits a spot to one figure.
import bodyfig as F

def mirror(path_d):
    """Mirror a simple absolute path (M/L/Q/C/Z with x y pairs) across x=200."""
    import re
    out=[]; xturn=True
    for t in re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', path_d):
        if t.isalpha(): out.append(t); xturn=True; continue
        v=float(t)
        out.append(f'{(400-v) if xturn else v:g}')
        xturn = not xturn
    return ' '.join(out)

E = lambda cx,cy,rx,ry,extra='': f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {extra}/>'
P = lambda d,extra='': f'<path d="{d}" {extra}/>'
T = lambda d,w=5: f'<path class="tube" d="{d}" style="stroke-width:{w}px"/>'   # stroked tube
T2 = lambda d,w=5: T(d,w)+T(mirror(d),w)
R = lambda x,y,w,h,rx=3,extra='': f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {extra}/>'
both = lambda fn: {'m':fn('m'), 'f':fn('f')}

VIEW = '0 0 400 820'
ZOOM = {'repro':'135 336 130 266'}     # the reproductive layer zooms in on the pelvis

LAYERS = [
  ('outside', 'Outside'),
  ('organs', 'Organs'),
  ('urinary', 'Urinary'),
  ('bones', 'Bones'),
  ('repro', 'Reproductive'),
]

PC = F.PIECES
hw = {s:F.FIG[s]['hw'] for s in ('m','f')}
ao = {'m':0,'f':-12}

# id, name, layer, color key, roots, shape, sex (None = both figures)
SPOTS = [
  # ----- Outside -----
  ('head','Head','outside','skin',['cephal'], both(lambda s: P(PC[s]['head'])), None),
  ('ear','Ear (ear, eardrum, middle ear)','outside','sense',['ot','myring','tympan'], both(lambda s: E(200-hw[s]-1,64,5,12)+E(200+hw[s]+1,64,5,12)), None),
  ('eye','Eye (eyeball, eyelid, conjunctiva, retina)','outside','sense',['ophthalm','blephar','conjunctiv','retin'], E(186,58,8,4.5)+E(214,58,8,4.5), None),
  ('nose','Nose','outside','resp',['rhin'], P('M200 62 L193 82 Q200 87 207 82 Z'), None),
  ('mouth','Mouth (lips, teeth, gums, tongue)','outside','oral',['stomat','cheil','gloss','odont','dent','gingiv'], E(200,96,11,4.5), None),
  ('neck','Neck','outside','skin',['cervic'], both(lambda s: P(PC[s]['neck'])), None),
  ('chest','Chest and breast','outside','skin',['thorac','mamm','mast'], both(lambda s: P(PC[s]['torso'], f'clip-path="url(#cp-chest)"')), None),
  ('abdomen','Abdomen','outside','skin',['lapar'], both(lambda s: P(PC[s]['torso'], f'clip-path="url(#cp-abd)"')), None),
  ('arm','Arm','outside','skin',['brachi'], both(lambda s: P(PC[s]['upperarm'])), None),
  ('extrem','Hands and feet (extremities)','outside','skin',['acr'], both(lambda s: P(PC[s]['hands'])+P(PC[s]['feet'])), None),
  # ----- Organs -----
  ('brain','Brain and meninges','organs','nerv',['encephal','mening'], E(200,52,29,27), None),
  ('tonsil','Tonsils','organs','lymph',['tonsill'], E(191,99,4.5,5)+E(209,99,4.5,5), None),
  ('thyroid','Thyroid gland','organs','endo',['thyroid'], E(191,134,7,6)+E(209,134,7,6)+R(191,131,18,5,1), None),
  ('larynx','Larynx (voice box)','organs','resp',['laryng'], R(194,111,12,12,4), None),
  ('trachea','Trachea (windpipe)','organs','resp',['trache'], R(196,123,8,52,3), None),
  ('lung','Lungs and pleura','organs','resp',['pulmon','pneumon','pleur'], P('M192 176 Q156 166 142 204 Q132 248 138 288 Q168 296 192 280 Z')+P(mirror('M192 176 Q156 166 142 204 Q132 248 138 288 Q168 296 192 280 Z')), None),
  ('bronchus','Bronchi (airways)','organs','resp',['bronch'], T('M200 174 L200 182 L180 198 L168 218 M180 198 L174 234 M200 182 L220 198 L232 218 M220 198 L226 234',5), None),
  ('esoph','Esophagus','organs','dig',['esophag'], T('M205 178 L207 278 Q212 296 230 304',6), None),
  ('heart','Heart','organs','card',['cardi'], E(208,240,22,18,'transform="rotate(-28 208 240)"'), None),
  ('liver','Liver','organs','dig',['hepat'], P('M150 298 Q178 288 226 296 Q218 320 184 330 Q160 334 152 322 Z'), None),
  ('gallbl','Gallbladder','organs','dig',['cholecyst'], E(174,334,6,9), None),
  ('stomach','Stomach','organs','dig',['gastr'], P('M222 300 Q244 292 250 310 Q254 338 238 348 Q222 352 216 338 Q228 324 222 306 Z'), None),
  ('spleen','Spleen','organs','lymph',['splen'], E(249,296,5.5,11), None),
  ('pancreas','Pancreas','organs','dig',['pancreat'], E(214,350,24,4.5,'transform="rotate(-10 214 350)"'), None),
  ('colon','Colon (large intestine)','organs','dig',['col','colon'], T('M158 414 L156 364 L244 364 L248 416 L222 430',12), None),
  ('smint','Small intestine (including the ileum)','organs','dig',['enter','ile'], E(201,396,32,23), None),
  ('append','Appendix','organs','dig',['append'], T('M158 420 L163 434',5), None),
  # ----- Urinary -----
  ('kidney','Kidneys (renal pelvis, glomeruli)','urinary','uri',['nephr','ren','pyel','glomerul'], E(168,332,14,24,'transform="rotate(10 168 332)"')+E(232,332,14,24,'transform="rotate(-10 232 332)"'), None),
  ('ureter','Ureters','urinary','uri',['ureter'], T2('M174 352 Q180 392 192 420',4), None),
  ('bladder','Urinary bladder','urinary','uri',['cyst','vesic'], E(200,428,17,13), None),
  ('urethra','Urethra and meatus','urinary','uri',['urethr','meat'], {'f':R(196,440,8,13,3), 'm':R(196,440,8,26,3)}, None),
  # ----- Bones -----
  ('skull','Skull','bones','bone',['crani'], both(lambda s: P(f'M{200-hw[s]+2} 60 Q{200-hw[s]+2} 14 200 14 Q{200+hw[s]-2} 14 {200+hw[s]-2} 60 Q{200+hw[s]-2} 86 {226 if s=="m" else 224} 100 L{174 if s=="m" else 176} 100 Q{200-hw[s]+2} 86 {200-hw[s]+2} 60 Z')), None),
  ('spine','Spine (vertebrae, lamina)','bones','bone',['vertebr','spondyl','lamin'], ''.join(R(194,y,12,9,2) for y in range(112,392,12)), None),
  ('ribs','Ribs','bones','bone',['cost'], ''.join(T2(f'M193 {y} Q150 {y-8} 142 {y+22}',4.5) for y in range(172,266,18)), None),
  ('sacrum','Sacrum','bones','bone',['sacr'], P('M186 392 L214 392 L206 426 L194 426 Z'), None),
  ('femur','Femur (thigh bone)','bones','bone',['femor'], {'m':T2('M248 430 L232 588',10), 'f':T2('M258 432 L232 588',10)}, None),
  ('wrist','Wrist bones','bones','bone',['carp'], both(lambda s: R(316+ao[s],398,21,10,4)+R(400-337-ao[s],398,21,10,4)), None),
  # ----- Reproductive (pelvis, zoomed) -----
  ('uterus','Uterus','repro','repro',['hyster'], P('M186 386 Q200 375 214 386 L210 415 Q200 421 190 415 Z'), 'f'),
  ('ftube','Fallopian tubes','repro','repro',['salping'], T2('M188 389 Q174 376 163 386',3), 'f'),
  ('ovary','Ovaries','repro','repro',['oophor'], E(159,393,7,4.5)+E(241,393,7,4.5), 'f'),
  ('cervix','Cervix','repro','repro',['cervic'], R(194,417,12,10,4), 'f'),
  ('vagina','Vagina','repro','repro',['colp'], R(195,429,10,27,4), 'f'),
  ('semves','Seminal vesicles','repro','repro',['vesicul'], E(186,431,6,3.5,'transform="rotate(-25 186 431)"')+E(214,431,6,3.5,'transform="rotate(25 214 431)"'), 'm'),
  ('prostate','Prostate gland','repro','repro',['prostat'], E(200,444,9,7), 'm'),
  ('vas','Vas deferens','repro','repro',['vas'], T2('M187 478 Q176 452 176 424 Q178 408 190 412 Q195 420 189 428',2.5), 'm'),
  ('epid','Epididymis','repro','repro',['epididym'], T2('M188 479 Q183 488 189 498',3), 'm'),
  ('testis','Testes','repro','repro',['orch','orchi','orchid','test'], E(194,489,5.5,8)+E(206,489,5.5,8), 'm'),
]

CLIPS = '<defs><clipPath id="cp-chest"><rect x="0" y="0" width="400" height="274"/></clipPath><clipPath id="cp-abd"><rect x="0" y="274" width="400" height="136"/></clipPath></defs>'

# Context drawn behind the reproductive organs (not tappable).
REPRO_CONTEXT = {
  'f': ('<g class="ctx" aria-hidden="true"><ellipse class="organ-ctx" cx="200" cy="428" rx="17" ry="13"/>'
        '<text class="small" x="222" y="446">bladder</text></g>'),
  'm': ('<g class="ctx" aria-hidden="true"><ellipse class="organ-ctx" cx="200" cy="420" rx="17" ry="13"/>'
        '<text class="small" x="220" y="412">bladder</text>'
        '<path class="tube-ctx" d="M200 451 L200 470"/><text class="small" x="203.5" y="466" style="font-size:4px">urethra</text>'
        '<ellipse class="organ-ctx" cx="200" cy="488" rx="18" ry="15"/><text class="small" x="221" y="500">scrotum</text></g>'),
}

# Bigger invisible touch targets for small parts (cx, cy, r).
HITS = {
  'tonsil':[(200,99,12)], 'larynx':[(200,116,9)], 'thyroid':[(200,135,17)], 'gallbl':[(174,335,11)],
  'append':[(160,428,11)], 'urethra':[(200,450,11)], 'eye':[(186,58,11),(214,58,11)], 'nose':[(200,75,10)],
  'spleen':[(250,296,12)], 'wrist':{'m':[(326,403,14),(74,403,14)], 'f':[(314,403,14),(86,403,14)]},
  'cervix':[(200,422,7)], 'semves':[(186,431,7),(214,431,7)], 'prostate':[(200,444,9)],
}

# Whole-body items: not in one place, so they live in a tray beside the map.
TRAY = [
  ('skin','Skin',['dermat','derm','cutane']),
  ('nail','Nails',['onych']),
  ('fat','Fat',['lip']),
  ('muscle','Muscle',['my']),
  ('tendon','Tendons',['tendin']),
  ('bursa','Bursae',['burs']),
  ('bone','Bone',['oste']),
  ('joint','Joints',['arthr']),
  ('cart','Cartilage',['chondr']),
  ('marrow','Bone marrow and spinal cord',['myel']),
  ('nerve','Nerves',['neur']),
  ('blood','Blood',['hemat','hem']),
  ('vessel','Blood vessels',['angi']),
  ('artery','Arteries',['arteri']),
  ('vein','Veins',['phleb','varic']),
  ('lymph','Lymph',['lymph']),
]
