# MedDecode master list (draft for instructor review).
# PARTS: id -> (form, type, meaning, pronunciation, body system, used as a Tiles pair?, conflict key)
# The conflict key keeps look-alike meanings ("below", "within", "disease") off the same Tiles board.
PARTS = {
 # prefixes
 'a':      ('a-, an-','prefix','without, absence of','ay, an','General',True,None),
 'brady':  ('brady-','prefix','slow','BRAD-ee','General',True,None),
 'tachy':  ('tachy-','prefix','fast, rapid','TAK-ee','General',True,None),
 'dys':    ('dys-','prefix','difficult, painful, abnormal','dis','General',True,None),
 'hyper':  ('hyper-','prefix','above normal, excessive','HY-per','General',True,'above'),
 'hypo':   ('hypo-','prefix','below normal, deficient','HY-poh','General',True,'below'),
 'peri':   ('peri-','prefix','around','PAIR-ee','General',True,None),
 'endo':   ('endo-','prefix','within, inner','EN-doh','General',True,'within'),
 'sub':    ('sub-','prefix','below, under','sub','General',True,'below'),
 'poly':   ('poly-','prefix','many, much','POL-ee','General',True,None),
 'hemi':   ('hemi-','prefix','half','HEM-ee','General',True,None),
 'dia':    ('dia-','prefix','through, complete','DY-uh','General',True,None),
 # roots shown as pictures in Tiles
 'cardi':  ('cardi/o','root','heart','KAR-dee-oh','Cardiovascular',True,'heart'),
 'hepat':  ('hepat/o','root','liver','HEP-uh-toh','Digestive',True,None),
 'nephr':  ('nephr/o','root','kidney','NEF-roh','Urinary',True,None),
 'oste':   ('oste/o','root','bone','OS-tee-oh','Skeletal',True,None),
 # roots as text
 'gastr':  ('gastr/o','root','stomach','GAS-troh','Digestive',True,None),
 'enter':  ('enter/o','root','small intestine','EN-ter-oh','Digestive',True,None),
 'col':    ('col/o','root','colon (large intestine)','KOH-loh','Digestive',True,None),
 'append': ('append/o','root','appendix','uh-PEN-doh','Digestive',True,None),
 'cholecyst':('cholecyst/o','root','gallbladder','koh-lee-SIS-toh','Digestive',True,None),
 'phag':   ('phag/o','root','eat, swallow','FAY-goh','Digestive',True,None),
 'neur':   ('neur/o','root','nerve','NOO-roh','Nervous',True,None),
 'encephal':('encephal/o','root','brain','en-SEF-uh-loh','Nervous',True,None),
 'cephal': ('cephal/o','root','head','SEF-uh-loh','Nervous',True,None),
 'crani':  ('crani/o','root','skull','KRAY-nee-oh','Skeletal',True,None),
 'my':     ('my/o','root','muscle','MY-oh','Muscular',True,None),
 'arthr':  ('arthr/o','root','joint','AR-throh','Skeletal',True,None),
 'chondr': ('chondr/o','root','cartilage','KON-droh','Skeletal',True,None),
 'dermat': ('dermat/o','root','skin','DER-muh-toh','Integumentary',True,'skin'),
 'lip':    ('lip/o','root','fat','LIP-oh','Integumentary',True,None),
 'rhin':   ('rhin/o','root','nose','RY-noh','Respiratory',True,None),
 'laryng': ('laryng/o','root','larynx (voice box)','luh-RING-goh','Respiratory',True,None),
 'trache': ('trache/o','root','trachea (windpipe)','TRAY-kee-oh','Respiratory',True,None),
 'bronch': ('bronch/o','root','bronchus (airway)','BRONG-koh','Respiratory',True,None),
 'pulmon': ('pulmon/o','root','lung','PUL-muh-noh','Respiratory',True,None),
 'cyst':   ('cyst/o','root','urinary bladder','SIS-toh','Urinary',True,None),
 'hemat':  ('hemat/o','root','blood','HEE-muh-toh','Blood',True,None),
 'angi':   ('angi/o','root','blood vessel','AN-jee-oh','Cardiovascular',True,None),
 'phleb':  ('phleb/o','root','vein','FLEB-oh','Cardiovascular',True,None),
 'thromb': ('thromb/o','root','clot','THROM-boh','Blood',True,None),
 'glyc':   ('glyc/o','root','sugar, glucose','GLY-koh','Endocrine',True,None),
 'cyan':   ('cyan/o','root','blue','SY-uh-noh','General',True,None),
 'erythr': ('erythr/o','root','red','eh-RITH-roh','General',True,None),
 'leuk':   ('leuk/o','root','white','LOO-koh','General',True,None),
 'path':   ('path/o','root','disease','PATH-oh','General',True,'disease'),
 'ot':     ('ot/o','root','ear','OH-toh','Sensory',True,None),
 'ophthalm':('ophthalm/o','root','eye','off-THAL-moh','Sensory',True,None),
 'gloss':  ('gloss/o','root','tongue','GLOS-oh','Oral',True,None),
 'odont':  ('odont/o','root','tooth','oh-DON-toh','Oral',True,'tooth'),
 'gingiv': ('gingiv/o','root','gums','JIN-jih-voh','Oral',True,None),
 # roots used in terms but not as Tiles pairs
 'tension':('tension','root','pressure','TEN-shun','General',False,None),
 'tonsill':('tonsill/o','root','tonsils','TON-sih-loh','Lymphatic',False,None),
 'cutane': ('cutane/o','root','skin','kyoo-TAY-nee-oh','Integumentary',False,'skin'),
 'por':    ('por/o','root','pore, small opening','POR-oh','General',False,None),
 'electr': ('electr/o','root','electricity','ee-LEK-troh','General',False,None),
 'colon':  ('colon/o','root','colon','koh-LON-oh','Digestive',False,None),
 # suffixes
 'itis':   ('-itis','suffix','inflammation','EYE-tis','General',True,None),
 'ectomy': ('-ectomy','suffix','surgical removal','EK-tuh-mee','General',True,None),
 'otomy':  ('-otomy','suffix','incision, cutting into','OT-uh-mee','General',True,None),
 'ostomy': ('-ostomy','suffix','new surgical opening','OS-tuh-mee','General',True,None),
 'algia':  ('-algia','suffix','pain','AL-jee-uh','General',True,None),
 'megaly': ('-megaly','suffix','enlargement','MEG-uh-lee','General',True,None),
 'logy':   ('-logy','suffix','study of','LOH-jee','General',True,None),
 'scopy':  ('-scopy','suffix','visual examination','SKOH-pee','General',True,None),
 'plasty': ('-plasty','suffix','surgical repair','PLAS-tee','General',True,None),
 'gram':   ('-gram','suffix','record, picture','gram','General',True,None),
 'emia':   ('-emia','suffix','blood condition','EE-mee-uh','General',True,None),
 'osis':   ('-osis','suffix','abnormal condition','OH-sis','General',True,None),
 'oma':    ('-oma','suffix','tumor, mass','OH-muh','General',True,None),
 'pathy':  ('-pathy','suffix','disease','PATH-ee','General',True,'disease'),
 'cyte':   ('-cyte','suffix','cell','site','General',True,None),
 'pnea':   ('-pnea','suffix','breathing','NEE-uh','General',True,None),
 'uria':   ('-uria','suffix','urine condition','YOO-ree-uh','General',True,None),
 'rrhea':  ('-rrhea','suffix','flow, discharge','REE-uh','General',True,None),
 'plegia': ('-plegia','suffix','paralysis','PLEE-juh','General',True,None),
 'penia':  ('-penia','suffix','deficiency, too few','PEE-nee-uh','General',True,None),
 # suffixes used in terms but not as Tiles pairs
 'ia':     ('-ia','suffix','condition','EE-uh','General',False,None),
 'ous':    ('-ous','suffix','pertaining to','us','General',False,None),
}

# TERMS: (word, parts, definition, pronunciation, what it names, body system, level)
# parts: list of (letters, part id); a combining vowel is ('o','cv').
T = lambda *a: a
TERMS = [
 T('gastritis',[('gastr','gastr'),('itis','itis')],'inflammation of the stomach','gas-TRY-tis','condition','Digestive','easy'),
 T('hepatitis',[('hepat','hepat'),('itis','itis')],'inflammation of the liver','hep-uh-TY-tis','condition','Digestive','easy'),
 T('nephritis',[('nephr','nephr'),('itis','itis')],'inflammation of the kidney','neh-FRY-tis','condition','Urinary','easy'),
 T('dermatitis',[('dermat','dermat'),('itis','itis')],'inflammation of the skin','der-muh-TY-tis','condition','Integumentary','easy'),
 T('cystitis',[('cyst','cyst'),('itis','itis')],'inflammation of the urinary bladder','sis-TY-tis','condition','Urinary','easy'),
 T('laryngitis',[('laryng','laryng'),('itis','itis')],'inflammation of the larynx (voice box)','lair-in-JY-tis','condition','Respiratory','easy'),
 T('phlebitis',[('phleb','phleb'),('itis','itis')],'inflammation of a vein','fleh-BY-tis','condition','Cardiovascular','easy'),
 T('encephalitis',[('encephal','encephal'),('itis','itis')],'inflammation of the brain','en-sef-uh-LY-tis','condition','Nervous','easy'),
 T('glossitis',[('gloss','gloss'),('itis','itis')],'inflammation of the tongue','glos-SY-tis','condition','Oral','easy'),
 T('gingivitis',[('gingiv','gingiv'),('itis','itis')],'inflammation of the gums','jin-jih-VY-tis','condition','Oral','easy'),
 T('colitis',[('col','col'),('itis','itis')],'inflammation of the colon','koh-LY-tis','condition','Digestive','easy'),
 T('appendectomy',[('append','append'),('ectomy','ectomy')],'surgical removal of the appendix','ap-en-DEK-tuh-mee','procedure','Digestive','easy'),
 T('tonsillectomy',[('tonsill','tonsill'),('ectomy','ectomy')],'surgical removal of the tonsils','ton-sih-LEK-tuh-mee','procedure','Lymphatic','easy'),
 T('cholecystectomy',[('cholecyst','cholecyst'),('ectomy','ectomy')],'surgical removal of the gallbladder','koh-lee-sis-TEK-tuh-mee','procedure','Digestive','easy'),
 T('craniotomy',[('crani','crani'),('otomy','otomy')],'an incision into the skull','kray-nee-OT-uh-mee','procedure','Nervous','easy'),
 T('tracheostomy',[('trache','trache'),('ostomy','ostomy')],'a new surgical opening into the trachea (windpipe)','tray-kee-OS-tuh-mee','procedure','Respiratory','easy'),
 T('rhinoplasty',[('rhin','rhin'),('o','cv'),('plasty','plasty')],'surgical repair of the nose','RY-noh-plas-tee','procedure','Respiratory','easy'),
 T('angioplasty',[('angi','angi'),('o','cv'),('plasty','plasty')],'surgical repair of a blood vessel','AN-jee-oh-plas-tee','procedure','Cardiovascular','easy'),
 T('cardiomegaly',[('cardi','cardi'),('o','cv'),('megaly','megaly')],'enlargement of the heart','kar-dee-oh-MEG-uh-lee','sign','Cardiovascular','easy'),
 T('hepatomegaly',[('hepat','hepat'),('o','cv'),('megaly','megaly')],'enlargement of the liver','hep-uh-toh-MEG-uh-lee','sign','Digestive','easy'),
 T('neuralgia',[('neur','neur'),('algia','algia')],'nerve pain','noo-RAL-juh','symptom','Nervous','easy'),
 T('myalgia',[('my','my'),('algia','algia')],'muscle pain','my-AL-juh','symptom','Muscular','easy'),
 T('cephalalgia',[('cephal','cephal'),('algia','algia')],'headache','sef-uh-LAL-juh','symptom','Nervous','easy'),
 T('otalgia',[('ot','ot'),('algia','algia')],'earache','oh-TAL-juh','symptom','Sensory','easy'),
 T('odontalgia',[('odont','odont'),('algia','algia')],'toothache','oh-don-TAL-jee-uh','symptom','Oral','easy'),
 T('arthralgia',[('arthr','arthr'),('algia','algia')],'joint pain','ar-THRAL-jee-uh','symptom','Skeletal','easy'),
 T('dermatology',[('dermat','dermat'),('o','cv'),('logy','logy')],'the study of the skin','der-muh-TOL-uh-jee','specialty','Integumentary','easy'),
 T('neurology',[('neur','neur'),('o','cv'),('logy','logy')],'the study of the nervous system','noo-ROL-uh-jee','specialty','Nervous','easy'),
 T('pathology',[('path','path'),('o','cv'),('logy','logy')],'the study of disease','puh-THOL-uh-jee','specialty','General','easy'),
 T('ophthalmology',[('ophthalm','ophthalm'),('o','cv'),('logy','logy')],'the study of the eye','off-thal-MOL-uh-jee','specialty','Sensory','easy'),
 T('bronchoscopy',[('bronch','bronch'),('o','cv'),('scopy','scopy')],'visual examination of the airways with a scope','brong-KOS-kuh-pee','test','Respiratory','easy'),
 T('lipoma',[('lip','lip'),('oma','oma')],'a benign (non-cancerous) tumor made of fat','lih-POH-muh','condition','Integumentary','easy'),
 T('thrombosis',[('thromb','thromb'),('osis','osis')],'an abnormal condition of a blood clot forming in a vessel','throm-BOH-sis','condition','Cardiovascular','easy'),
 T('cyanosis',[('cyan','cyan'),('osis','osis')],'bluish discoloration of the skin','sy-uh-NOH-sis','sign','General','easy'),
 T('neuropathy',[('neur','neur'),('o','cv'),('pathy','pathy')],'disease or damage of the nerves','noo-ROP-uh-thee','condition','Nervous','easy'),
 T('leukocyte',[('leuk','leuk'),('o','cv'),('cyte','cyte')],'white blood cell','LOO-koh-site','body part','Blood','easy'),
 T('erythrocyte',[('erythr','erythr'),('o','cv'),('cyte','cyte')],'red blood cell','eh-RITH-roh-site','body part','Blood','easy'),
 T('thrombocyte',[('thromb','thromb'),('o','cv'),('cyte','cyte')],'platelet; a cell that helps blood clot','THROM-boh-site','body part','Blood','easy'),
 T('leukopenia',[('leuk','leuk'),('o','cv'),('penia','penia')],'too few white blood cells','loo-koh-PEE-nee-uh','condition','Blood','easy'),
 T('hematuria',[('hemat','hemat'),('uria','uria')],'blood in the urine','hee-muh-TOO-ree-uh','sign','Urinary','easy'),
 T('rhinorrhea',[('rhin','rhin'),('o','cv'),('rrhea','rrhea')],'runny nose; discharge from the nose','ry-noh-REE-uh','symptom','Respiratory','easy'),
 T('anemia',[('an','a'),('emia','emia')],'a lack of red blood cells or hemoglobin','uh-NEE-mee-uh','condition','Blood','medium'),
 T('polyuria',[('poly','poly'),('uria','uria')],'excessive urination','pol-ee-YOOR-ee-uh','symptom','Urinary','medium'),
 T('apnea',[('a','a'),('pnea','pnea')],'absence of breathing','AP-nee-uh','sign','Respiratory','medium'),
 T('tachypnea',[('tachy','tachy'),('pnea','pnea')],'fast breathing','tak-ip-NEE-uh','sign','Respiratory','medium'),
 T('dyspnea',[('dys','dys'),('pnea','pnea')],'difficulty breathing','DISP-nee-uh','symptom','Respiratory','medium'),
 T('bradycardia',[('brady','brady'),('card','cardi'),('ia','ia')],'slow heart rate','brad-ee-KAR-dee-uh','sign','Cardiovascular','medium'),
 T('tachycardia',[('tachy','tachy'),('card','cardi'),('ia','ia')],'fast heart rate','tak-ih-KAR-dee-uh','sign','Cardiovascular','medium'),
 T('hypoglycemia',[('hypo','hypo'),('glyc','glyc'),('emia','emia')],'below-normal blood sugar','hy-poh-gly-SEE-mee-uh','condition','Endocrine','medium'),
 T('hyperglycemia',[('hyper','hyper'),('glyc','glyc'),('emia','emia')],'above-normal blood sugar','hy-per-gly-SEE-mee-uh','condition','Endocrine','medium'),
 T('hypertension',[('hyper','hyper'),('tension','tension')],'abnormally high blood pressure','hy-per-TEN-shun','condition','Cardiovascular','medium'),
 T('pericarditis',[('peri','peri'),('card','cardi'),('itis','itis')],'inflammation of the sac around the heart','pair-ih-kar-DY-tis','condition','Cardiovascular','medium'),
 T('dysphagia',[('dys','dys'),('phag','phag'),('ia','ia')],'difficulty swallowing','dis-FAY-jee-uh','symptom','Digestive','medium'),
 T('hemiplegia',[('hemi','hemi'),('plegia','plegia')],'paralysis of one side of the body','hem-ee-PLEE-juh','sign','Nervous','medium'),
 T('diarrhea',[('dia','dia'),('rrhea','rrhea')],'frequent, loose, watery stools','dy-uh-REE-uh','symptom','Digestive','medium'),
 T('endoscopy',[('endo','endo'),('scopy','scopy')],'visual examination inside the body with a scope','en-DOS-kuh-pee','test','General','medium'),
 T('subcutaneous',[('sub','sub'),('cutane','cutane'),('ous','ous')],'pertaining to below the skin','sub-kyoo-TAY-nee-us','descriptive word','Integumentary','medium'),
 T('gastroenteritis',[('gastr','gastr'),('o','cv'),('enter','enter'),('itis','itis')],'inflammation of the stomach and small intestine','gas-troh-en-ter-EYE-tis','condition','Digestive','hard'),
 T('osteoarthritis',[('oste','oste'),('o','cv'),('arthr','arthr'),('itis','itis')],'inflammation of bone and joint; degenerative joint disease','os-tee-oh-ar-THRY-tis','condition','Skeletal','hard'),
 T('osteoporosis',[('oste','oste'),('o','cv'),('por','por'),('osis','osis')],'a condition of thin, porous bones that break easily','os-tee-oh-puh-ROH-sis','condition','Skeletal','hard'),
 T('electrocardiogram',[('electr','electr'),('o','cv'),('cardi','cardi'),('o','cv'),('gram','gram')],"a record of the heart's electrical activity (ECG or EKG)",'ee-lek-troh-KAR-dee-oh-gram','test','Cardiovascular','hard'),
]

# =====================================================================
# Expansion, Oct 2026: parts and terms so every chapter of
# "Acquiring Medical Language" (Jones & Cavanagh, McGraw Hill, 3rd ed.) has content.
# Drafts for instructor review.
# =====================================================================
PARTS['pulmon'] = PARTS['pulmon'][:6] + ('lung',)
PARTS.update({
 # prefixes
 'intra':  ('intra-','prefix','within, inside','IN-truh','General',True,'within'),
 'inter':  ('inter-','prefix','between','IN-ter','General',True,None),
 'para':   ('para-','prefix','beside, near; abnormal','PAIR-uh','General',True,None),
 'quadri': ('quadri-','prefix','four','KWAD-rih','General',True,None),
 'pre':    ('pre-','prefix','before','pree','General',True,'before'),
 'pro':    ('pro-','prefix','before, forward','proh','General',False,'before'),
 'post':   ('post-','prefix','after','pohst','General',True,None),
 'neo':    ('neo-','prefix','new','NEE-oh','General',True,None),
 'epi':    ('epi-','prefix','upon, above','EP-ee','General',True,'above'),
 'olig':   ('olig/o','prefix','scanty, few','OL-ih-goh','General',True,None),
 # roots
 'derm':   ('derm/o','root','skin','DER-moh','Integumentary',False,'skin'),
 'melan':  ('melan/o','root','black, dark','MEL-uh-noh','General',True,None),
 'onych':  ('onych/o','root','nail','ON-ih-koh','Integumentary',True,None),
 'myc':    ('myc/o','root','fungus','MY-koh','General',True,None),
 'cost':   ('cost/o','root','rib','KOS-toh','Skeletal',True,None),
 'vertebr':('vertebr/o','root','vertebra (backbone)','VER-tuh-broh','Skeletal',True,'vertebra'),
 'myel':   ('myel/o','root','bone marrow; spinal cord','MY-eh-loh','Skeletal',True,None),
 'mening': ('mening/o','root','meninges (membranes around the brain and spinal cord)','meh-NING-goh','Nervous',True,None),
 'phas':   ('phas/o','root','speech','FAY-zoh','Nervous',True,None),
 'hydr':   ('hydr/o','root','water, fluid','HY-droh','General',True,None),
 'psych':  ('psych/o','root','mind','SY-koh','Nervous',True,None),
 'blephar':('blephar/o','root','eyelid','BLEF-uh-roh','Sensory',True,None),
 'conjunctiv':('conjunctiv/o','root','conjunctiva (lining of the eyelid and eye)','kon-junk-TY-voh','Sensory',True,None),
 'retin':  ('retin/o','root','retina','RET-ih-noh','Sensory',True,None),
 'myring': ('myring/o','root','eardrum','mih-RING-goh','Sensory',True,'eardrum'),
 'tympan': ('tympan/o','root','eardrum, middle ear','TIM-puh-noh','Sensory',True,'eardrum'),
 'thyroid':('thyroid/o','root','thyroid gland','THY-roy-doh','Endocrine',True,None),
 'crin':   ('crin/o','root','to secrete','KRIN-oh','Endocrine',True,None),
 'acr':    ('acr/o','root','extremities (hands and feet)','AK-roh','General',True,None),
 'calc':   ('calc/o','root','calcium','KAL-koh','General',True,None),
 'cyt':    ('cyt/o','root','cell','SY-toh','General',False,None),
 'splen':  ('splen/o','root','spleen','SPLEE-noh','Lymphatic',True,None),
 'lymph':  ('lymph/o','root','lymph','LIMF-oh','Lymphatic',True,None),
 'immun':  ('immun/o','root','immune, protection','IM-yoo-noh','Lymphatic',True,None),
 'hem':    ('hem/o','root','blood','HEE-moh','Blood',False,None),
 'arteri': ('arteri/o','root','artery','ar-TEER-ee-oh','Cardiovascular',True,None),
 'scler':  ('scler/o','root','hard, hardening','SKLAIR-oh','General',True,None),
 'rrhythm':('rrhythm/o','root','rhythm','RITH-moh','Cardiovascular',False,None),
 'pneumon':('pneumon/o','root','lung, air','noo-MOH-noh','Respiratory',True,'lung'),
 'pleur':  ('pleur/o','root','pleura (lining around the lungs)','PLOOR-oh','Respiratory',False,None),
 'orth':   ('orth/o','root','straight, upright','OR-thoh','General',True,None),
 'ox':     ('ox/o','root','oxygen','OK-soh','Respiratory',True,None),
 'esophag':('esophag/o','root','esophagus','eh-SOF-uh-goh','Digestive',True,None),
 'stomat': ('stomat/o','root','mouth','STOH-muh-toh','Oral',True,'mouth'),
 'cheil':  ('cheil/o','root','lip','KY-loh','Oral',True,None),
 'dent':   ('dent/o','root','tooth','DEN-toh','Oral',False,'tooth'),
 'pancreat':('pancreat/o','root','pancreas','PAN-kree-uh-toh','Digestive',True,None),
 'lith':   ('lith/o','root','stone','LITH-oh','General',True,None),
 'ur':     ('ur/o','root','urine, urinary tract','YOO-roh','Urinary',True,None),
 'pyel':   ('pyel/o','root','renal pelvis (center of the kidney)','PY-eh-loh','Urinary',True,None),
 'prostat':('prostat/o','root','prostate gland','PROS-tuh-toh','Male reproductive',True,None),
 'orch':   ('orch/o','root','testis, testicle','OR-koh','Male reproductive',True,None),
 'vas':    ('vas/o','root','vessel, duct; vas deferens','VAS-oh','Male reproductive',True,None),
 'hyster': ('hyster/o','root','uterus','HIS-ter-oh','Female reproductive',True,None),
 'mamm':   ('mamm/o','root','breast','MAM-oh','Female reproductive',True,'breast'),
 'mast':   ('mast/o','root','breast','MAS-toh','Female reproductive',True,'breast'),
 'gynec':  ('gynec/o','root','woman, female','GY-neh-koh','Female reproductive',True,None),
 'men':    ('men/o','root','menstruation','MEN-oh','Female reproductive',True,None),
 'oophor': ('oophor/o','root','ovary','oh-OF-or-oh','Female reproductive',True,None),
 'salping':('salping/o','root','fallopian tube','sal-PING-goh','Female reproductive',True,None),
 'colp':   ('colp/o','root','vagina','KOL-poh','Female reproductive',True,None),
 'nat':    ('nat/o','root','birth','NAY-toh','Female reproductive',True,None),
 'part':   ('part/o','root','labor, childbirth','PAR-toh','Female reproductive',False,None),
 'gnos':   ('gnos/o','root','knowledge','NOH-soh','General',True,None),
 'eti':    ('eti/o','root','cause','EE-tee-oh','General',True,None),
 'brachi': ('brachi/o','root','arm','BRAY-kee-oh','Skeletal',True,None),
 'femor':  ('femor/o','root','femur (thigh bone)','FEM-or-oh','Skeletal',True,None),
 'carp':   ('carp/o','root','wrist bones','KAR-poh','Skeletal',True,None),
 'tendin': ('tendin/o','root','tendon','TEN-dih-noh','Muscular',True,None),
 'burs':   ('burs/o','root','bursa (fluid sac near a joint)','BUR-soh','Skeletal',True,None),
 'spondyl':('spondyl/o','root','vertebra (backbone)','SPON-dih-loh','Skeletal',True,'vertebra'),
 'lamin':  ('lamin/o','root','lamina (part of a vertebra)','LAM-ih-noh','Skeletal',False,None),
 'thorac': ('thorac/o','root','chest','thoh-RAK-oh','Respiratory',True,None),
 'cervic': ('cervic/o','root','neck; cervix','SER-vih-koh','Skeletal',True,None),
 'sacr':   ('sacr/o','root','sacrum','SAY-kroh','Skeletal',True,None),
 'centesis':('-centesis','suffix','surgical puncture to remove fluid','sen-TEE-sis','General',True,None),
 # suffixes
 'ic':     ('-ic','suffix','pertaining to','ik','General',False,None),
 'al':     ('-al','suffix','pertaining to','ul','General',False,None),
 'tic':    ('-tic','suffix','pertaining to','tik','General',False,None),
 'malacia':('-malacia','suffix','softening','muh-LAY-shuh','General',True,None),
 'paresis':('-paresis','suffix','slight paralysis, weakness','puh-REE-sis','General',True,None),
 'scope':  ('-scope','suffix','instrument for viewing','skohp','General',True,None),
 'ism':    ('-ism','suffix','condition, state','IZ-um','General',True,None),
 'dipsia': ('-dipsia','suffix','thirst','DIP-see-uh','General',True,None),
 'lysis':  ('-lysis','suffix','breakdown, destruction','LY-sis','General',True,None),
 'iasis':  ('-iasis','suffix','abnormal condition','EYE-uh-sis','General',False,None),
 'iatry':  ('-iatry','suffix','medical treatment','EYE-uh-tree','General',True,None),
 'ics':    ('-ics','suffix','practice, field of study','iks','General',False,None),
 'graphy': ('-graphy','suffix','process of recording','gruh-fee','General',False,None),
 'graph':  ('-graph','suffix','instrument for recording','graf','General',False,None),
 'us':     ('-us','suffix','noun ending','us','General',False,None),
 'um':     ('-um','suffix','noun ending','um','General',False,None),
 'is':     ('-is','suffix','noun ending','is','General',False,None),
})

def o(): return ('o','cv')
TERMS += [
 # Ch 2 Health records
 T('diagnosis',[('dia','dia'),('gnos','gnos'),('is','is')],'identification of a disease or condition','dy-ug-NOH-sis','record term','General','medium'),
 T('prognosis',[('pro','pro'),('gnos','gnos'),('is','is')],'the expected outcome of a disease','prog-NOH-sis','record term','General','medium'),
 T('etiology',[('eti','eti'),o(),('logy','logy')],'the cause of a disease; the study of causes','ee-tee-OL-uh-jee','record term','General','medium'),
 # Ch 3 Integumentary
 T('melanoma',[('melan','melan'),('oma','oma')],'a cancerous tumor of the pigment cells of the skin','mel-uh-NOH-muh','condition','Integumentary','medium'),
 T('onychomycosis',[('onych','onych'),o(),('myc','myc'),('osis','osis')],'a fungal infection of a nail','on-ih-koh-my-KOH-sis','condition','Integumentary','hard'),
 T('hypodermic',[('hypo','hypo'),('derm','derm'),('ic','ic')],'pertaining to under the skin','hy-poh-DER-mik','descriptive word','Integumentary','medium'),
 T('intradermal',[('intra','intra'),('derm','derm'),('al','al')],'pertaining to within the skin','in-truh-DER-mul','descriptive word','Integumentary','medium'),
 T('dermatoplasty',[('dermat','dermat'),o(),('plasty','plasty')],'surgical repair of the skin; skin grafting','DER-muh-toh-plas-tee','procedure','Integumentary','easy'),
 T('lipectomy',[('lip','lip'),('ectomy','ectomy')],'surgical removal of fat','lih-PEK-tuh-mee','procedure','Integumentary','easy'),
 # Ch 4 Musculoskeletal
 T('arthritis',[('arthr','arthr'),('itis','itis')],'inflammation of a joint','ar-THRY-tis','condition','Skeletal','easy'),
 T('arthroscopy',[('arthr','arthr'),o(),('scopy','scopy')],'visual examination inside a joint with a scope','ar-THROS-kuh-pee','procedure','Skeletal','easy'),
 T('arthroplasty',[('arthr','arthr'),o(),('plasty','plasty')],'surgical repair or replacement of a joint','AR-throh-plas-tee','procedure','Skeletal','easy'),
 T('osteomyelitis',[('oste','oste'),o(),('myel','myel'),('itis','itis')],'inflammation (usually infection) of bone and bone marrow','os-tee-oh-my-eh-LY-tis','condition','Skeletal','hard'),
 T('osteomalacia',[('oste','oste'),o(),('malacia','malacia')],'softening of the bones','os-tee-oh-muh-LAY-shuh','condition','Skeletal','medium'),
 T('chondromalacia',[('chondr','chondr'),o(),('malacia','malacia')],'softening of cartilage','kon-droh-muh-LAY-shuh','condition','Skeletal','medium'),
 T('myopathy',[('my','my'),o(),('pathy','pathy')],'disease of the muscles','my-OP-uh-thee','condition','Muscular','easy'),
 T('costochondritis',[('cost','cost'),o(),('chondr','chondr'),('itis','itis')],'inflammation of the cartilage that joins a rib to the breastbone','kos-toh-kon-DRY-tis','condition','Skeletal','hard'),
 T('intercostal',[('inter','inter'),('cost','cost'),('al','al')],'pertaining to between the ribs','in-ter-KOS-tul','descriptive word','Skeletal','medium'),
 T('vertebral',[('vertebr','vertebr'),('al','al')],'pertaining to a vertebra','VER-tuh-brul','descriptive word','Skeletal','easy'),
 T('brachial',[('brachi','brachi'),('al','al')],'pertaining to the arm (as in the brachial pulse)','BRAY-kee-ul','descriptive word','Skeletal','easy'),
 T('femoral',[('femor','femor'),('al','al')],'pertaining to the femur or thigh (as in the femoral pulse)','FEM-or-ul','descriptive word','Skeletal','easy'),
 T('carpal',[('carp','carp'),('al','al')],'pertaining to the wrist bones','KAR-pul','descriptive word','Skeletal','easy'),
 T('cervical',[('cervic','cervic'),('al','al')],'pertaining to the neck (as in the cervical spine)','SER-vih-kul','descriptive word','Skeletal','easy'),
 T('sacral',[('sacr','sacr'),('al','al')],'pertaining to the sacrum, the base of the spine','SAY-krul','descriptive word','Skeletal','easy'),
 T('tendinitis',[('tendin','tendin'),('itis','itis')],'inflammation of a tendon','ten-dih-NY-tis','condition','Muscular','easy'),
 T('bursitis',[('burs','burs'),('itis','itis')],'inflammation of a bursa, a fluid sac near a joint','bur-SY-tis','condition','Skeletal','easy'),
 T('arthrocentesis',[('arthr','arthr'),o(),('centesis','centesis')],'surgical puncture of a joint to remove fluid','ar-throh-sen-TEE-sis','procedure','Skeletal','hard'),
 T('spondylosis',[('spondyl','spondyl'),('osis','osis')],'an abnormal condition of the vertebrae; wear-and-tear arthritis of the spine','spon-dih-LOH-sis','condition','Skeletal','medium'),
 T('laminectomy',[('lamin','lamin'),('ectomy','ectomy')],'surgical removal of part of a vertebra (the lamina)','lam-ih-NEK-tuh-mee','procedure','Skeletal','medium'),
 T('myelogram',[('myel','myel'),o(),('gram','gram')],'an x-ray picture of the spinal cord and the space around it','MY-eh-loh-gram','test','Nervous','medium'),
 T('thoracic',[('thorac','thorac'),('ic','ic')],'pertaining to the chest','thoh-RAS-ik','descriptive word','Respiratory','easy'),
 T('thoracotomy',[('thorac','thorac'),('otomy','otomy')],'an incision into the chest','thor-uh-KOT-uh-mee','procedure','Respiratory','medium'),
 # Ch 5 Nervous system and psychiatry
 T('quadriplegia',[('quadri','quadri'),('plegia','plegia')],'paralysis of all four limbs','kwad-rih-PLEE-juh','sign','Nervous','medium'),
 T('paraplegia',[('para','para'),('plegia','plegia')],'paralysis of both legs and the lower body','pair-uh-PLEE-juh','sign','Nervous','medium'),
 T('hemiparesis',[('hemi','hemi'),('paresis','paresis')],'weakness of one side of the body','hem-ee-puh-REE-sis','sign','Nervous','medium'),
 T('aphasia',[('a','a'),('phas','phas'),('ia','ia')],'loss of the ability to speak or understand language','uh-FAY-zhuh','sign','Nervous','medium'),
 T('dysphasia',[('dys','dys'),('phas','phas'),('ia','ia')],'difficulty speaking or understanding language','dis-FAY-zhuh','sign','Nervous','medium'),
 T('meningitis',[('mening','mening'),('itis','itis')],'inflammation of the meninges, the membranes around the brain and spinal cord','men-in-JY-tis','condition','Nervous','easy'),
 T('hydrocephalus',[('hydr','hydr'),o(),('cephal','cephal'),('us','us')],'a buildup of fluid in the spaces of the brain','hy-droh-SEF-uh-lus','condition','Nervous','hard'),
 T('encephalopathy',[('encephal','encephal'),o(),('pathy','pathy')],'disease of the brain','en-sef-uh-LOP-uh-thee','condition','Nervous','medium'),
 T('neuritis',[('neur','neur'),('itis','itis')],'inflammation of a nerve','noo-RY-tis','condition','Nervous','easy'),
 T('psychiatry',[('psych','psych'),('iatry','iatry')],'the medical treatment of mental disorders','sy-KY-uh-tree','specialty','Nervous','medium'),
 T('psychology',[('psych','psych'),o(),('logy','logy')],'the study of the mind and behavior','sy-KOL-uh-jee','specialty','Nervous','easy'),
 # Ch 6 Sensory: eye and ear
 T('otitis',[('ot','ot'),('itis','itis')],'inflammation of the ear','oh-TY-tis','condition','Sensory','easy'),
 T('otorrhea',[('ot','ot'),o(),('rrhea','rrhea')],'discharge from the ear','oh-toh-REE-uh','sign','Sensory','easy'),
 T('otoscope',[('ot','ot'),o(),('scope','scope')],'an instrument for looking into the ear','OH-toh-skohp','instrument','Sensory','easy'),
 T('ophthalmoscope',[('ophthalm','ophthalm'),o(),('scope','scope')],'an instrument for looking into the eye','off-THAL-muh-skohp','instrument','Sensory','medium'),
 T('blepharitis',[('blephar','blephar'),('itis','itis')],'inflammation of the eyelid','blef-uh-RY-tis','condition','Sensory','easy'),
 T('blepharoplasty',[('blephar','blephar'),o(),('plasty','plasty')],'surgical repair of the eyelid','BLEF-uh-roh-plas-tee','procedure','Sensory','medium'),
 T('conjunctivitis',[('conjunctiv','conjunctiv'),('itis','itis')],'inflammation of the conjunctiva; pinkeye','kun-junk-tih-VY-tis','condition','Sensory','easy'),
 T('retinopathy',[('retin','retin'),o(),('pathy','pathy')],'disease of the retina','ret-ih-NOP-uh-thee','condition','Sensory','medium'),
 T('myringotomy',[('myring','myring'),('otomy','otomy')],'an incision into the eardrum','mir-in-GOT-uh-mee','procedure','Sensory','medium'),
 T('tympanoplasty',[('tympan','tympan'),o(),('plasty','plasty')],'surgical repair of the eardrum','TIM-puh-noh-plas-tee','procedure','Sensory','medium'),
 T('otolaryngology',[('ot','ot'),o(),('laryng','laryng'),o(),('logy','logy')],'the study of the ear, nose and throat (ENT)','oh-toh-lair-in-GOL-uh-jee','specialty','Sensory','hard'),
 # Ch 7 Endocrine
 T('thyroidectomy',[('thyroid','thyroid'),('ectomy','ectomy')],'surgical removal of the thyroid gland','thy-roy-DEK-tuh-mee','procedure','Endocrine','easy'),
 T('thyroiditis',[('thyroid','thyroid'),('itis','itis')],'inflammation of the thyroid gland','thy-roy-DY-tis','condition','Endocrine','easy'),
 T('hyperthyroidism',[('hyper','hyper'),('thyroid','thyroid'),('ism','ism')],'a condition of an overactive thyroid gland','hy-per-THY-roy-diz-um','condition','Endocrine','medium'),
 T('hypothyroidism',[('hypo','hypo'),('thyroid','thyroid'),('ism','ism')],'a condition of an underactive thyroid gland','hy-poh-THY-roy-diz-um','condition','Endocrine','medium'),
 T('endocrinology',[('endo','endo'),('crin','crin'),o(),('logy','logy')],'the study of the endocrine glands and hormones','en-doh-krih-NOL-uh-jee','specialty','Endocrine','hard'),
 T('polydipsia',[('poly','poly'),('dipsia','dipsia')],'excessive thirst','pol-ee-DIP-see-uh','symptom','Endocrine','medium'),
 T('acromegaly',[('acr','acr'),o(),('megaly','megaly')],'enlargement of the hands, feet and face from too much growth hormone','ak-roh-MEG-uh-lee','condition','Endocrine','medium'),
 T('hypercalcemia',[('hyper','hyper'),('calc','calc'),('emia','emia')],'too much calcium in the blood','hy-per-kal-SEE-mee-uh','condition','Endocrine','medium'),
 # Ch 8 Blood, lymphatic and immune
 T('thrombocytopenia',[('thromb','thromb'),o(),('cyt','cyt'),o(),('penia','penia')],'too few platelets in the blood','throm-boh-sy-toh-PEE-nee-uh','condition','Blood','hard'),
 T('hematology',[('hemat','hemat'),o(),('logy','logy')],'the study of blood','hee-muh-TOL-uh-jee','specialty','Blood','easy'),
 T('hematoma',[('hemat','hemat'),('oma','oma')],'a collection of blood in tissue, often under the skin','hee-muh-TOH-muh','condition','Blood','easy'),
 T('leukemia',[('leuk','leuk'),('emia','emia')],'a cancer of the white blood cells','loo-KEE-mee-uh','condition','Blood','easy'),
 T('hemolysis',[('hem','hem'),o(),('lysis','lysis')],'the breakdown of red blood cells','hee-MOL-ih-sis','condition','Blood','medium'),
 T('splenomegaly',[('splen','splen'),o(),('megaly','megaly')],'enlargement of the spleen','splee-noh-MEG-uh-lee','sign','Lymphatic','easy'),
 T('splenectomy',[('splen','splen'),('ectomy','ectomy')],'surgical removal of the spleen','splee-NEK-tuh-mee','procedure','Lymphatic','easy'),
 T('lymphoma',[('lymph','lymph'),('oma','oma')],'a cancer of the lymph tissue','lim-FOH-muh','condition','Lymphatic','easy'),
 T('immunology',[('immun','immun'),o(),('logy','logy')],'the study of the immune system','im-yoo-NOL-uh-jee','specialty','Lymphatic','easy'),
 T('tonsillitis',[('tonsill','tonsill'),('itis','itis')],'inflammation of the tonsils','ton-sih-LY-tis','condition','Lymphatic','easy'),
 # Ch 9 Cardiovascular
 T('cardiology',[('cardi','cardi'),o(),('logy','logy')],'the study of the heart','kar-dee-OL-uh-jee','specialty','Cardiovascular','easy'),
 T('endocarditis',[('endo','endo'),('card','cardi'),('itis','itis')],'inflammation of the inner lining of the heart','en-doh-kar-DY-tis','condition','Cardiovascular','medium'),
 T('cardiomyopathy',[('cardi','cardi'),o(),('my','my'),o(),('pathy','pathy')],'disease of the heart muscle','kar-dee-oh-my-OP-uh-thee','condition','Cardiovascular','hard'),
 T('arteriosclerosis',[('arteri','arteri'),o(),('scler','scler'),('osis','osis')],'hardening of the arteries','ar-teer-ee-oh-skleh-ROH-sis','condition','Cardiovascular','hard'),
 T('thrombophlebitis',[('thromb','thromb'),o(),('phleb','phleb'),('itis','itis')],'inflammation of a vein with a blood clot','throm-boh-fleh-BY-tis','condition','Cardiovascular','hard'),
 T('hypotension',[('hypo','hypo'),('tension','tension')],'abnormally low blood pressure','hy-poh-TEN-shun','condition','Cardiovascular','medium'),
 T('angiogram',[('angi','angi'),o(),('gram','gram')],'an x-ray picture of blood vessels','AN-jee-oh-gram','test','Cardiovascular','easy'),
 T('arrhythmia',[('a','a'),('rrhythm','rrhythm'),('ia','ia')],'an abnormal heart rhythm','uh-RITH-mee-uh','condition','Cardiovascular','medium'),
 T('phlebotomy',[('phleb','phleb'),('otomy','otomy')],'an incision into a vein to draw blood','fleh-BOT-uh-mee','procedure','Cardiovascular','easy'),
 # Ch 10 Respiratory
 T('bronchitis',[('bronch','bronch'),('itis','itis')],'inflammation of the bronchi (airways)','brong-KY-tis','condition','Respiratory','easy'),
 T('pneumonia',[('pneumon','pneumon'),('ia','ia')],'infection and inflammation of the lungs','noo-MOH-nee-uh','condition','Respiratory','easy'),
 T('bradypnea',[('brady','brady'),('pnea','pnea')],'slow breathing','brad-ip-NEE-uh','sign','Respiratory','medium'),
 T('orthopnea',[('orth','orth'),o(),('pnea','pnea')],'difficulty breathing except when sitting or standing upright','or-THOP-nee-uh','symptom','Respiratory','medium'),
 T('hypoxia',[('hyp','hypo'),('ox','ox'),('ia','ia')],'too little oxygen reaching the body tissues','hy-POK-see-uh','condition','Respiratory','medium'),
 T('laryngoscopy',[('laryng','laryng'),o(),('scopy','scopy')],'visual examination of the larynx with a scope','lair-in-GOS-kuh-pee','test','Respiratory','easy'),
 T('rhinitis',[('rhin','rhin'),('itis','itis')],'inflammation of the lining of the nose','ry-NY-tis','condition','Respiratory','easy'),
 T('pulmonology',[('pulmon','pulmon'),o(),('logy','logy')],'the study of the lungs','pul-muh-NOL-uh-jee','specialty','Respiratory','easy'),
 T('tracheotomy',[('trache','trache'),('otomy','otomy')],'an incision into the trachea (windpipe)','tray-kee-OT-uh-mee','procedure','Respiratory','easy'),
 # Ch 11 Gastrointestinal, including the mouth and teeth
 T('colonoscopy',[('colon','colon'),o(),('scopy','scopy')],'visual examination of the colon with a scope','koh-luh-NOS-kuh-pee','test','Digestive','easy'),
 T('esophagitis',[('esophag','esophag'),('itis','itis')],'inflammation of the esophagus','eh-sof-uh-JY-tis','condition','Digestive','easy'),
 T('gastrostomy',[('gastr','gastr'),('ostomy','ostomy')],'a new surgical opening into the stomach, often for a feeding tube','gas-TROS-tuh-mee','procedure','Digestive','easy'),
 T('colostomy',[('col','col'),('ostomy','ostomy')],'a new surgical opening from the colon to the outside of the abdomen','koh-LOS-tuh-mee','procedure','Digestive','easy'),
 T('pancreatitis',[('pancreat','pancreat'),('itis','itis')],'inflammation of the pancreas','pan-kree-uh-TY-tis','condition','Digestive','easy'),
 T('cholecystitis',[('cholecyst','cholecyst'),('itis','itis')],'inflammation of the gallbladder','koh-lee-sis-TY-tis','condition','Digestive','easy'),
 T('gastroenterology',[('gastr','gastr'),o(),('enter','enter'),o(),('logy','logy')],'the study of the stomach and intestines','gas-troh-en-ter-OL-uh-jee','specialty','Digestive','hard'),
 T('stomatitis',[('stomat','stomat'),('itis','itis')],'inflammation of the mouth','stoh-muh-TY-tis','condition','Oral','easy'),
 T('cheilitis',[('cheil','cheil'),('itis','itis')],'inflammation of the lips','ky-LY-tis','condition','Oral','easy'),
 T('periodontitis',[('peri','peri'),('odont','odont'),('itis','itis')],'inflammation of the tissues around a tooth; advanced gum disease','pair-ee-oh-don-TY-tis','condition','Oral','medium'),
 T('periodontal',[('peri','peri'),('odont','odont'),('al','al')],'pertaining to the tissues around a tooth','pair-ee-oh-DON-tul','descriptive word','Oral','medium'),
 T('orthodontics',[('orth','orth'),('odont','odont'),('ics','ics')],'the dental specialty that straightens teeth','or-thoh-DON-tiks','specialty','Oral','medium'),
 T('gingivectomy',[('gingiv','gingiv'),('ectomy','ectomy')],'surgical removal of gum tissue','jin-jih-VEK-tuh-mee','procedure','Oral','easy'),
 # Ch 12 Urinary and male reproductive
 T('nephrology',[('nephr','nephr'),o(),('logy','logy')],'the study of the kidneys','neh-FROL-uh-jee','specialty','Urinary','easy'),
 T('nephrectomy',[('nephr','nephr'),('ectomy','ectomy')],'surgical removal of a kidney','neh-FREK-tuh-mee','procedure','Urinary','easy'),
 T('nephrolithiasis',[('nephr','nephr'),o(),('lith','lith'),('iasis','iasis')],'kidney stones','nef-roh-lih-THY-uh-sis','condition','Urinary','hard'),
 T('dysuria',[('dys','dys'),('uria','uria')],'painful or difficult urination','dis-YOO-ree-uh','symptom','Urinary','medium'),
 T('anuria',[('an','a'),('uria','uria')],'no urine production','an-YOO-ree-uh','sign','Urinary','medium'),
 T('oliguria',[('olig','olig'),('uria','uria')],'too little urine production','ol-ih-GYOO-ree-uh','sign','Urinary','medium'),
 T('cystoscopy',[('cyst','cyst'),o(),('scopy','scopy')],'visual examination of the urinary bladder with a scope','sis-TOS-kuh-pee','test','Urinary','easy'),
 T('urology',[('ur','ur'),o(),('logy','logy')],'the study of the urinary tract and the male reproductive system','yoo-ROL-uh-jee','specialty','Urinary','easy'),
 T('pyelonephritis',[('pyel','pyel'),o(),('nephr','nephr'),('itis','itis')],'inflammation (usually infection) of the kidney and renal pelvis','py-eh-loh-neh-FRY-tis','condition','Urinary','hard'),
 T('prostatitis',[('prostat','prostat'),('itis','itis')],'inflammation of the prostate gland','pros-tuh-TY-tis','condition','Male reproductive','easy'),
 T('prostatectomy',[('prostat','prostat'),('ectomy','ectomy')],'surgical removal of the prostate gland','pros-tuh-TEK-tuh-mee','procedure','Male reproductive','easy'),
 T('orchitis',[('orch','orch'),('itis','itis')],'inflammation of a testis','or-KY-tis','condition','Male reproductive','easy'),
 T('vasectomy',[('vas','vas'),('ectomy','ectomy')],'removal of part of the vas deferens to prevent pregnancy','vuh-SEK-tuh-mee','procedure','Male reproductive','easy'),
 # Ch 13 Female reproductive, obstetrics and newborns
 T('hysterectomy',[('hyster','hyster'),('ectomy','ectomy')],'surgical removal of the uterus','his-ter-EK-tuh-mee','procedure','Female reproductive','easy'),
 T('mammogram',[('mamm','mamm'),o(),('gram','gram')],'an x-ray picture of the breast','MAM-oh-gram','test','Female reproductive','easy'),
 T('mastectomy',[('mast','mast'),('ectomy','ectomy')],'surgical removal of a breast','mas-TEK-tuh-mee','procedure','Female reproductive','easy'),
 T('mastitis',[('mast','mast'),('itis','itis')],'inflammation of the breast','mas-TY-tis','condition','Female reproductive','easy'),
 T('gynecology',[('gynec','gynec'),o(),('logy','logy')],'the study of the female reproductive system','gy-neh-KOL-uh-jee','specialty','Female reproductive','easy'),
 T('amenorrhea',[('a','a'),('men','men'),o(),('rrhea','rrhea')],'absence of menstrual periods','ay-men-oh-REE-uh','symptom','Female reproductive','medium'),
 T('dysmenorrhea',[('dys','dys'),('men','men'),o(),('rrhea','rrhea')],'painful menstrual periods','dis-men-oh-REE-uh','symptom','Female reproductive','medium'),
 T('oophorectomy',[('oophor','oophor'),('ectomy','ectomy')],'surgical removal of an ovary','oh-of-oh-REK-tuh-mee','procedure','Female reproductive','medium'),
 T('salpingitis',[('salping','salping'),('itis','itis')],'inflammation of a fallopian tube','sal-pin-JY-tis','condition','Female reproductive','medium'),
 T('colposcopy',[('colp','colp'),o(),('scopy','scopy')],'visual examination of the vagina and cervix with a scope','kol-POS-kuh-pee','test','Female reproductive','medium'),
 T('prenatal',[('pre','pre'),('nat','nat'),('al','al')],'pertaining to before birth','pree-NAY-tul','descriptive word','Female reproductive','easy'),
 T('neonatal',[('neo','neo'),('nat','nat'),('al','al')],'pertaining to a newborn (the first 28 days of life)','nee-oh-NAY-tul','descriptive word','Female reproductive','easy'),
 T('neonatology',[('neo','neo'),('nat','nat'),o(),('logy','logy')],'the study and care of newborns','nee-oh-nay-TOL-uh-jee','specialty','Female reproductive','medium'),
 T('postpartum',[('post','post'),('part','part'),('um','um')],'after childbirth','pohst-PAR-tum','descriptive word','Female reproductive','medium'),
]

# =====================================================================
# Filters: chapter, body region, CTE program
# =====================================================================
BOOK = 'Acquiring Medical Language, 3rd ed. (Jones & Cavanagh, McGraw Hill)'
CHAPTERS = {
 1:'Introduction to Medical Language', 2:'Introduction to Health Records',
 3:'Integumentary System (Dermatology)', 4:'Musculoskeletal System (Orthopedics)',
 5:'Nervous System (Neurology and Psychiatry)', 6:'Sensory System (Eye and Ear)',
 7:'Endocrine System', 8:'Blood and Lymphatic Systems (Hematology and Immunology)',
 9:'Cardiovascular System (Cardiology)', 10:'Respiratory System (Pulmonology)',
 11:'Gastrointestinal System (Gastroenterology)', 12:'Urinary and Male Reproductive Systems (Urology)',
 13:'Female Reproductive System (Gynecology, Obstetrics, Neonatology)'}
SYS_CH = {'General':1,'Integumentary':3,'Skeletal':4,'Muscular':4,'Nervous':5,'Sensory':6,'Endocrine':7,
          'Blood':8,'Lymphatic':8,'Cardiovascular':9,'Respiratory':10,'Digestive':11,'Oral':11,
          'Urinary':12,'Male reproductive':12,'Female reproductive':13}
TERM_CH = {'diagnosis':[2],'prognosis':[2],'etiology':[2],'pathology':[1,2],'cyanosis':[3,10],'endoscopy':[1,11]}

REGIONS = ['Head and neck','Chest','Abdomen and pelvis','Back and spine','Arms and legs','Skin','Whole body']
H,CH,AB,SP,LI,SK,WB = REGIONS
ROOT_REG = {
 'encephal':[H],'cephal':[H],'crani':[H],'rhin':[H],'laryng':[H],'trache':[H],'ot':[H],'ophthalm':[H],
 'gloss':[H],'odont':[H],'dent':[H],'gingiv':[H],'tonsill':[H],'phag':[H],'blephar':[H],'conjunctiv':[H],
 'retin':[H],'myring':[H],'tympan':[H],'thyroid':[H],'stomat':[H],'cheil':[H],'phas':[H],'psych':[H],
 'mening':[H,SP],'esophag':[H,CH],
 'cardi':[CH],'bronch':[CH],'pulmon':[CH],'pneumon':[CH],'pleur':[CH],'cost':[CH],'mamm':[CH],'mast':[CH],
 'gastr':[AB],'enter':[AB],'col':[AB],'colon':[AB],'append':[AB],'cholecyst':[AB],'hepat':[AB],'nephr':[AB],
 'cyst':[AB],'splen':[AB],'pancreat':[AB],'pyel':[AB],'ur':[AB],'prostat':[AB],'orch':[AB],'vas':[AB],
 'hyster':[AB],'oophor':[AB],'salping':[AB],'colp':[AB],'men':[AB],'gynec':[AB],'part':[AB],'nat':[AB],
 'vertebr':[SP],'spondyl':[SP],'lamin':[SP],'sacr':[SP],'cervic':[H,SP],'thorac':[CH],'brachi':[LI],'femor':[LI],'carp':[LI],'tendin':[LI],'burs':[LI],'myel':[SP,WB],
 'arthr':[LI],'acr':[LI],'onych':[LI,SK],
 'dermat':[SK],'derm':[SK],'cutane':[SK],'lip':[SK],'melan':[SK],'cyan':[SK],
 'oste':[WB],'my':[WB],'chondr':[WB],'neur':[WB],'hemat':[WB],'hem':[WB],'angi':[WB],'phleb':[WB],'arteri':[WB],
 'thromb':[WB],'glyc':[WB],'leuk':[WB],'erythr':[WB],'cyt':[WB],'lymph':[WB],'immun':[WB],'crin':[WB],'calc':[WB],
 'ox':[WB],'rrhythm':[CH],
}
TERM_REG = {
 'hydrocephalus':[H],'orthopnea':[CH],'hypoxia':[WB],'arteriosclerosis':[WB],'acromegaly':[LI,H],
 'hypertension':[WB],'hypotension':[WB],'apnea':[CH],'tachypnea':[CH],'dyspnea':[CH],'bradypnea':[CH],
 'hemiplegia':[WB],'hemiparesis':[WB],'quadriplegia':[SP,LI],'paraplegia':[SP,LI],
 'diarrhea':[AB],'polyuria':[AB],'dysuria':[AB],'anuria':[AB],'oliguria':[AB],
 'prenatal':[AB],'postpartum':[AB],'neonatal':[WB],'neonatology':[WB],'polydipsia':[WB],'anemia':[WB],
 'endoscopy':[WB],'electrocardiogram':[CH],'osteoarthritis':[LI],'osteoporosis':[WB,SP],'myalgia':[WB],
 'meningitis':[H,SP],'craniotomy':[H],'cyanosis':[SK],'subcutaneous':[SK],'lipoma':[SK],'hypercalcemia':[WB],
 'thrombosis':[WB],'leukemia':[WB],'lymphoma':[WB],'hematoma':[SK,WB],'otolaryngology':[H],'myelogram':[SP],'cervical':[H,SP],
}
PROGRAMS = ['EMT','CNA','CCMA','Dental']
EMT_SKIP_SYS = {'Oral','Male reproductive','Female reproductive','Lymphatic'}
EMT_ADD = {'prenatal','postpartum','neonatal','tonsillitis','hematoma'}
CNA_PROC_OK = {'laminectomy','tracheostomy','gastrostomy','colostomy','appendectomy','cholecystectomy','mastectomy','hysterectomy',
               'prostatectomy','arthroplasty','tonsillectomy','splenectomy','nephrectomy','phlebotomy','thyroidectomy','craniotomy'}
DENTAL_ADD = {'hypertension','hypotension','tachycardia','bradycardia','arrhythmia','endocarditis','anemia','leukemia',
              'thrombocytopenia','hematoma','hypoglycemia','hyperglycemia','polydipsia','hyperthyroidism','hypothyroidism',
              'apnea','dyspnea','tachypnea','hypoxia','cyanosis','dysphagia','tonsillitis','tonsillectomy','otolaryngology',
              'aphasia','hemiplegia','subcutaneous','lipoma','osteoporosis','rhinorrhea','thrombosis','electrocardiogram',
              'diagnosis','prognosis','etiology','pathology','hepatitis','sinusitis'}

def term_chapters(t):
    w = t[0]
    return TERM_CH.get(w, [SYS_CH[t[5]]])
def term_regions(t):
    w = t[0]
    if w in TERM_REG: return TERM_REG[w]
    regs = []
    for _,pid in t[1]:
        for r in ROOT_REG.get(pid, []):
            if r not in regs: regs.append(r)
    return regs or [WB]
def term_programs(t):
    w,parts,d,say,kind,sysname,lvl = t
    out = ['CCMA']
    if (sysname not in EMT_SKIP_SYS and kind not in ('specialty','instrument','specialist','process','substance')) or w in EMT_ADD: out.append('EMT')
    if kind not in ('specialty','instrument','specialist','process','substance') and (kind!='procedure' or w in CNA_PROC_OK): out.append('CNA')
    if sysname in ('Oral',) or w in DENTAL_ADD: out.append('Dental')
    return [p for p in PROGRAMS if p in out]
def part_tags(pid):
    form,typ,m,say,sysname,tile,ck = PARTS[pid]
    ch = [SYS_CH.get(sysname,1)] if typ=='root' else [1]
    used = [t for t in TERMS if any(p==pid for _,p in t[1])]
    if typ=='root' and sysname=='General':
        ch = sorted({c for t in used for c in term_chapters(t)}) or [1]
    reg = ROOT_REG.get(pid, [])
    if typ=='root' and not reg:
        reg = sorted({r for t in used for r in term_regions(t)}, key=REGIONS.index)
    prog = sorted({p for t in used for p in term_programs(t)}, key=PROGRAMS.index) if typ=='root' else list(PROGRAMS)
    return {'ch':ch, 'reg':reg, 'prog':prog or list(PROGRAMS)}
def term_tags(t):
    return {'ch':term_chapters(t), 'reg':term_regions(t), 'prog':term_programs(t)}

# =====================================================================
# Chapter 12 glossary terms (Oct 2026). Word list from the AML Chapter 12 Quick Reference;
# definitions, splits and pronunciations written by MedDecode.
# =====================================================================
from glossary_ch12 import PARTS12, T12, PHRASES12
PARTS['nephr'] = PARTS['nephr'][:6] + ('kidney',)
PARTS['cyst'] = PARTS['cyst'][:6] + ('bladder',)
PARTS['orch'] = PARTS['orch'][:6] + ('testis',)
PARTS['algia'] = PARTS['algia'][:6] + ('pain',)
PARTS.update(PARTS12)
PARTS['dipsia'] = PARTS['dipsia'][:6] + ('thirst',)
_SYS12 = {}
for w,split,d,say,kind,lvl in T12:
    parts=[]
    for t in split.split('|'):
        if '=' in t: l,p=t.split('=')
        elif t in ('o','i'): l,p=t,'cv'
        else: l,p=t,t
        parts.append((l,p))
    sysn = 'Male reproductive' if any(p in ('balan','epididym','sperm','spermat','test','orchi','orchid','orch','prostat','vesicul','semin','gon','vas','varic','zo') for _,p in parts) else 'Urinary'
    TERMS.append(T(w,parts,d,say,kind,sysn,lvl))
    TERM_CH[w]=[12]
TERM_CH['polydipsia']=[7,12]
GLOSSARY_CH12 = {t[0] for t in T12} | {'cystitis','cystoscopy','dysuria','hematuria','nephrectomy','nephritis','nephrolithiasis','nephrology','oliguria','orchitis','polydipsia','polyuria','prostatectomy','prostatitis','pyelonephritis','urology','vasectomy'}
for r in ('balan','epididym','glomerul','meat','ren','sperm','spermat','test','orchi','orchid','ureter','urethr','vesic','vesicul','gon','semin','ile','lapar'):
    ROOT_REG[r]=[AB]
ROOT_REG['varic']=[AB,WB]
for w in ('nocturia','glucosuria','glycosuria','ketonuria','albuminuria','azoturia','pyuria','diuresis','enuresis','diuretic','uremia','uropoiesis','uroxanthin','urocyanosis','azotorrhea','aspermia','azoospermia','oligospermia','anorchidism','cryptorchidism','circumcision','gonorrhea','lithotripsy','lithectomy','ultrasonography'):
    TERM_REG[w]=[AB]
for w in ('azotemia','hyperkalemia','hyponatremia','ketolysis','dipsogenic','spermicide','spermolytic'):
    TERM_REG[w]=[WB] if w not in ('spermicide','spermolytic') else [AB]
PHRASES = [dict(t=t, d=d, say=say, c=c, ch=[12]) for t,d,say,c in PHRASES12]

# Synonyms: both answers are accepted in Build/Jeopardy, and they never share a Tiles board.
SYN_GROUPS = [['subcutaneous','hypodermic'],['orchitis','orchiditis','testitis'],['cystalgia','cystodynia'],
  ['cystostomy','vesicostomy'],['glucosuria','glycosuria'],['lithonephrotomy','nephrolithotomy'],['orchialgia','orchiodynia'],
  ['orchidectomy','orchiectomy'],['orchidopexy','orchiopexy'],['cystocele','vesicocele'],['nephrolithiasis','nephrolithosis'],
  ['pyelonephritis','nephropyelitis'],['pyelocystitis','cystopyelitis'],['urethrocystitis','cystourethritis'],['hydronephrosis','nephrohydrosis']]
SYN_OF = {w:g for g in SYN_GROUPS for w in g}
