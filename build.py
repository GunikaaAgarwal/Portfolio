from pathlib import Path
import html,re,json

r=Path(__file__).parent;d=r/'dist'
site_source=(r/'content/site-content.md').read_text()
site=json.loads(re.search(r'```json\s*(\{.*?\})\s*```',site_source,re.S).group(1))
old=json.loads((r/'content/existing-projects.json').read_text())
new=json.loads((r/'content/new-projects.json').read_text())
galleries=json.loads((r/'content/galleries.json').read_text())
profile=site.get('profile') or json.loads((r/'content/profile.json').read_text())

def esc(s):return html.escape(str(s),quote=True)
def join_lines(lines): return '<br>'.join(esc(line) for line in lines)
def render_about(about):
 photos=''.join(f'<button type="button" class="about-photo {esc(p["class"])}" aria-pressed="false" aria-label="Bring forward: {esc(p["label"])}"><img src="{esc(p["src"])}" alt="{esc(p["alt"])}" width="{p["width"]}" height="{p["height"]}" loading="lazy"><span>{esc(p["label"])}</span></button>' for p in about['photos'])
 paragraphs=''.join(f'<p>{p}</p>' for p in about['paragraphs'])
 return f'<section class="about-section about-refreshed" id="about"><div class="about-visual"><p class="eyebrow">{esc(about["eyebrow"])}</p><h2 class="about-title">{esc(about["heading_lines"][0])}<br><span>{esc(about["heading_lines"][1])}</span></h2><div class="about-photo-stack" role="group" aria-label="A little more about Gunikaa">{photos}</div><p class="about-photo-hint">{esc(about["photo_hint"])}</p></div><div class="about-copy">{paragraphs}<p class="about-availability">{about["availability"]}</p></div></section>'
project_meta=site['project_meta']
projects=[]
for slug,x in old.items():
 meta=project_meta[slug]
 projects.append(dict(slug=slug,name=meta['name'],category=meta['category'],label=meta['label'],description=meta['description'],cover=slug,headline=x['heading'],body=x['body'],facts=x['facts']))
projects+=new
projects.sort(key=lambda x:site['project_order'].index(x['slug']))
def figure(asset,caption):
 return f'<figure class="project-figure reveal"><button class="zoom-image" data-image="assets/{asset}.webp" data-caption="{esc(caption)}" aria-label="Enlarge image: {esc(caption)}"><img src="assets/{asset}.webp" alt="{esc(caption)}" loading="lazy"><span class="zoom-label">View detail <span aria-hidden="true">＋</span></span></button><figcaption>{esc(caption)}</figcaption></figure>'
nav_cfg=site['navigation']
def render_nav():
 links=''.join(f'<a href="{esc(link["href"])}">{esc(link["label"])}</a>' for link in nav_cfg['links'])
 return (
  '<a class="skip-link" href="#main">Skip to content</a><header class="site-header">'
  f'<a class="wordmark" href="index.html" aria-label="{esc(site["site"]["name"])} home">{esc(site["site"]["name"].lower())}<span class="brand-dot">.</span><small>DESIGNER</small></a>'
  '<nav aria-label="Main navigation">'
  f'{links}'
    f'<a class="resume-nav" href="{esc(nav_cfg["resume_href"])}" target="_blank" rel="noopener">{esc(nav_cfg["resume_label"])}</a>'
  f'<a class="nav-contact" href="{esc(nav_cfg["contact_href"])}">{esc(nav_cfg["contact_label"])} <span aria-hidden="true">↗</span></a>'
  '</nav></header>'
 )
footer_cfg=site['footer']
footer='<footer><a href="index.html" class="footer-name">'+esc(footer_cfg['name'])+'</a><span>'+esc(footer_cfg['descriptor'])+'</span><button class="back-top">'+esc(footer_cfg['back_top'])+'</button></footer>'
dialog='<dialog class="lightbox" aria-label="Project image detail"><button class="close-lightbox" aria-label="Close image">Close ×</button><img alt=""><p></p></dialog>'
def shell(title,body,description='',case=False):
 description=description or site['site']['description']
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="'+esc(site['site']['theme_color'])+'"><title>'+esc(title)+' | '+esc(site['site']['name'])+'</title><meta name="description" content="'+esc(description)+'"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 40 40%27%3E%3Crect width=%2740%27 height=%2740%27 rx=%2710%27 fill=%27%23431c27%27/%3E%3Ctext x=%279%27 y=%2729%27 font-size=%2728%27 font-family=%27Arial%27 fill=%27%23ffad66%27%3Eg%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="style.css"><script src="interactions.js" defer></script></head><body'+(' class="case-page"' if case else '')+'><div class="reading-progress" aria-hidden="true"></div>'+render_nav()+'<main id="main">'+body+'</main>'+footer+dialog+'</body></html>'
def card(p,i):
 hidden=' hidden' if i>=site["work"]["featured_count"] else ''
 thumbnail=p.get("thumbnail", p["cover"]+".webp")
 return f'<article class="project-card reveal" data-category="{esc(p["category"])}"{hidden}><a href="{esc(p["slug"])}.html" class="project-link"><div class="project-visual visual-{esc(p["slug"])}"><img src="assets/{esc(thumbnail)}" alt="{esc(p["name"])} project presentation" loading="lazy"><span class="project-number">{i+1:02}</span><span class="view-project">Explore project <span aria-hidden="true">↗</span></span></div><div class="project-info"><p class="project-label">{esc(p["label"])}</p><h3>{esc(p["name"])}<span class="project-arrow" aria-hidden="true">↗</span></h3><p class="project-description">{esc(p["description"])}</p></div></a></article>'
hero_cfg=site['hero']
hero='''<section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="short-rule"></span> '''+esc(hero_cfg['eyebrow'])+'''</p><h1>'''+join_lines(hero_cfg['heading_lines'])+'''</h1><p class="hero-intro">'''+esc(hero_cfg['intro'])+'''</p><div class="hero-actions"><a class="button primary" href="#work">'''+esc(hero_cfg['primary_cta'])+''' <span aria-hidden="true">↘</span></a><a class="text-link" href="#about">'''+esc(hero_cfg['secondary_cta'])+''' <span aria-hidden="true">↗</span></a></div><p class="hero-note">'''+esc(hero_cfg['note'])+'''</p></div><div class="portrait-composition"><div class="portrait-frame"><img class="portrait-source" src="'''+esc(site['site']['hero_image'])+'''" alt="'''+esc(hero_cfg['portrait_alt'])+'''" width="2047" height="1022" fetchpriority="high"></div><div class="portrait-caption"><span>'''+join_lines(hero_cfg['portrait_caption'].splitlines())+'''</span><span class="portrait-sign">'''+esc(hero_cfg['portrait_sign'])+'''</span></div></div></section><div class="discipline-line">'''+''.join(f'<span>{esc(text)}</span>' for text in hero_cfg['discipline_line'])+'''<a href="#work">'''+esc(hero_cfg['scroll_prompt'])+'''</a></div>'''
work_cfg=site['work']
filters=''.join(f'<button type="button" data-filter="{esc(v)}" aria-pressed="{str(v=="all").lower()}">{esc(t)}</button>' for v,t in work_cfg['filters'])
work='<section id="work" class="work-section"><div class="section-heading"><div><p class="eyebrow">'+esc(work_cfg['eyebrow'])+'</p><h2>'+join_lines(work_cfg['heading_lines'])+'</h2></div><p>'+esc(work_cfg['intro'])+'</p></div><div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects by discipline">'+filters+'</div><span id="project-count" role="status" aria-live="polite">Showing '+str(work_cfg['featured_count'])+' of '+str(len(projects))+' projects</span></div><div class="project-grid" id="project-grid">'+''.join(card(p,i) for i,p in enumerate(projects))+'</div><div class="more-projects-wrap"><button type="button" class="button primary more-projects" aria-controls="project-grid" aria-expanded="false">View more projects <span aria-hidden="true">↓</span></button></div><noscript><style>.project-card[hidden]{display:block!important}.more-projects-wrap,#project-count{display:none!important}</style></noscript></section>'
about=render_about(site['about'])
def entries(items):
 return '<ol class="timeline">'+''.join('<li><h4>'+esc(title)+'</h4><p>'+esc(organization)+'</p><p class="entry-date">'+esc(date)+'</p>'+('<p class="entry-detail">'+esc(detail)+'</p>' if detail else '')+'</li>' for title,organization,date,detail in items)+'</ol>'
contact_cfg=site['contact']
contact='''<section class="contact-section" id="contact"><p class="eyebrow">'''+esc(contact_cfg['eyebrow'])+'''</p><h2>'''+esc(contact_cfg['heading'])+'''<span>?</span></h2><div class="contact-bottom"><div><p>'''+esc(contact_cfg['intro'])+'''</p><a class="email-link" href="mailto:'''+esc(contact_cfg['email'])+'''">'''+esc(contact_cfg['email'])+'''</a></div><div class="contact-actions"><button class="copy-email" data-email="'''+esc(contact_cfg['email'])+'''">'''+esc(contact_cfg['copy_label'])+'''</button><a href="'''+esc(contact_cfg['linkedin'])+'''" target="_blank" rel="noopener noreferrer">'''+esc(contact_cfg['link_label'])+'''</a></div></div><p class="copy-status" role="status" aria-live="polite"></p></section>'''
resume_cfg=site['resume']
resume='<section id="experience" class="resume-section"><div class="section-heading"><div><p class="eyebrow">'+esc(resume_cfg['eyebrow'])+'</p><h2>'+join_lines(resume_cfg['heading_lines'])+'</h2></div><a class="text-link" href="'+esc(nav_cfg['resume_href'])+'" target="_blank" rel="noopener">'+esc(resume_cfg['link_label'])+'</a></div><div class="resume-columns"><div class="resume-column reveal"><h3 class="group-label">Experience</h3>'+entries(profile['experience'])+'</div><div class="resume-column reveal"><h3 class="group-label">Education</h3>'+entries(profile['education'])+'<h3 class="group-label certifications-label">Certifications</h3><ol class="timeline">'+''.join('<li><h4>'+esc(a)+'</h4><p>'+esc(b)+'</p></li>' for a,b in profile['certifications'])+'</ol></div></div></section>'
if not profile['certifications']:
 resume=re.sub(r'<h3 class="group-label certifications-label">Certifications</h3><ol class="timeline"></ol>', '', resume)
def chips(key):return '<ul class="skill-chips">'+''.join('<li>'+esc(x)+'</li>' for x in profile[key])+'</ul>'
skills_cfg=site['skills']
skills='<section class="skills-section reveal" id="skills" aria-labelledby="skills-heading"><div class="skills-title"><p class="eyebrow">'+esc(skills_cfg['eyebrow'])+'</p><h2 id="skills-heading">'+esc(skills_cfg['heading'])+'</h2></div><div class="skills-columns"><div><h3 class="group-label">'+esc(skills_cfg['group_labels']['skills'])+'</h3>'+chips('skills')+'</div><div><h3 class="group-label">'+esc(skills_cfg['group_labels']['tools'])+'</h3>'+chips('tools')+'<div class="ai-group"><h3 class="group-label">'+esc(skills_cfg['group_labels']['ai'])+'</h3>'+chips('ai')+'</div></div></div></section>'
(d/'index.html').write_text(shell('UX/UI & Communication Designer',hero+work+about+resume+skills+contact))
for i,p in enumerate(projects):
 title=esc(p['headline']);lead=esc(p['description'])
 b=f'<div class="case-back"><a href="index.html#work">← All projects</a><span>{i+1:02} / {len(projects):02}</span></div><section class="case-hero"><p class="eyebrow">{esc(p["label"])}</p><h1>{title}</h1><p>{lead}</p></section>'
 if 'facts' in p:b+=p['facts']
 else:b+='<div class="facts">'+''.join(f'<div><strong>{k}</strong>{esc(v)}</div>' for k,v in [('Role',p['role']),('Scope',p['scope']),('Context',p['type'])])+'</div>'
 if p['slug']=='abpal':b+='<div class="case-live"><a class="button primary" href="https://www.abpal.com/" target="_blank" rel="noopener noreferrer">Visit live website ↗</a></div>'
 if p['slug']=='abpal-catalog':b+='<div class="case-live"><a class="button primary" href="https://admin-portal.abpal.com/storage/about-sidebar/September2026/rVwM0GGBnYkzOMBwYDwd.pdf" target="_blank" rel="noopener noreferrer">Open full catalog PDF ↗</a></div>'
 b+=figure(p['cover'],p['name']+' — project overview')
 if 'body' in p:
  body=p['body']
  body=re.sub(r'<img src="assets/([^\"]+)\.webp" alt="([^\"]*)" loading="lazy">',lambda m:figure(m[1],html.unescape(m[2])),body)
  b+='<div class="case-body">'+body
  if p['slug']=='tac':
   b+='<section class="story"><p class="eyebrow">Extending the identity</p><h2>One brand, across physical and digital touchpoints.</h2><p>The graduation project also extends the identity into a catalog, business cards, supplement packaging, and bottle packaging. These applications connect the website’s visual language to the objects customers encounter beyond the screen.</p>'+figure('tac-catalog','The Anti-Aging Centre — catalog design')+figure('tac-packaging','The Anti-Aging Centre — packaging applications')+'</section>'
  b+='</div>'
 else:
  b+='<div class="case-body">'
  for label,heading,text,asset in p['sections']:
   b+=f'<section class="story"><p class="eyebrow">{esc(label)}</p><h2>{esc(heading)}</h2><p>{esc(text)}</p>'+(figure(asset,heading) if asset else '')+'</section>'
  b+=f'<section class="story outcome"><p class="eyebrow">Outcome</p><h2>{esc(p.get("outcome_heading", "What the work brings together."))}</h2><p>{esc(p["outcome"])}</p></section></div>'
 if p['slug'] in galleries:
  b+='<section class="outcome-gallery"><div class="section-heading"><div><p class="eyebrow">A CLOSER LOOK</p><h2>'+('Selected catalog pages' if p['slug']=='abpal-catalog' else 'Design outcomes & details')+'</h2></div></div><div class="outcome-grid">'+''.join(figure(asset,caption) for asset,caption in galleries[p['slug']] if asset!=p['cover'])+'</div></section>'
 if p['slug']=='abpal':b+='<p class="related-project"><a class="text-link" href="abpal-catalog.html">Explore my ABPAL catalog design ↗</a></p>'
 if p['slug']=='lissitzky':
  labels=['Cover','Introduction','Early work & geometric symbolism','Exhibition design','The Abstract Cabinet','Art & social change','Design principles','Legacy & communication','References']
  slides=''.join('<div class="editorial-slide"'+(' hidden' if j else '')+'>'+figure(f'lissitzky-reader-{j+1:02}',label)+'</div>' for j,label in enumerate(labels))
  thumbs=''.join(f'<button type="button" class="editorial-thumb" data-spread="{j}" aria-label="Show spread {j+1}: {esc(label)}" aria-pressed="{str(j==0).lower()}"><img src="assets/lissitzky-reader-{j+1:02}.webp" alt="" loading="lazy"><span>{j+1:02}</span></button>' for j,label in enumerate(labels))
  reader='<div class="editorial-reader" role="region" aria-label="Publication reader" tabindex="0"><div class="editorial-slides">'+slides+'</div><div class="editorial-reader-controls"><button type="button" data-reader-prev disabled aria-label="Previous spread">← Previous</button><p class="editorial-reader-status" aria-live="polite">01 / 09 · Cover</p><button type="button" data-reader-next aria-label="Next spread">Next →</button></div><div class="editorial-thumbs">'+thumbs+'</div></div><noscript><style>.editorial-slide[hidden]{display:block!important}.editorial-reader-controls,.editorial-thumbs{display:none!important}</style></noscript>'
  custom=(r/'content/lissitzky.html').read_text().replace('{{reader}}',reader)
  custom=re.sub(r'{{figure:([^|]+)\|([^}]+)}}',lambda m:figure(m[1],m[2]),custom)
  b=f'<div class="case-back"><a href="index.html#work">← All projects</a><span>{i+1:02} / {len(projects):02}</span></div>'+custom
 if p['slug']=='abpal-catalog':
  selections=galleries['abpal-catalog']
  slides=''.join('<div class="editorial-slide"'+(' hidden' if j else '')+'>'+figure(asset,label)+'</div>' for j,(asset,label) in enumerate(selections))
  thumbs=''.join(f'<button type="button" class="editorial-thumb" data-spread="{j}" aria-label="Show {esc(label)}" aria-pressed="{str(j==0).lower()}"><img src="assets/{asset}.webp" alt="" loading="lazy"><span>{j+1:02}</span></button>' for j,(asset,label) in enumerate(selections))
  reader='<div class="editorial-reader" role="region" aria-label="Selected catalog pages" tabindex="0"><div class="editorial-slides">'+slides+'</div><div class="editorial-reader-controls"><button type="button" data-reader-prev disabled aria-label="Previous page">← Previous</button><p class="editorial-reader-status" aria-live="polite">01 / 06 · Catalog cover — page 1</p><button type="button" data-reader-next aria-label="Next page">Next →</button></div><div class="editorial-thumbs">'+thumbs+'</div></div><noscript><style>.editorial-slide[hidden]{display:block!important}.editorial-reader-controls,.editorial-thumbs{display:none!important}</style></noscript>'
  custom=(r/'content/abpal-catalog.html').read_text().replace('{{reader}}',reader)
  custom=re.sub(r'{{figure:([^|]+)\|([^}]+)}}',lambda m:figure(m[1],m[2]),custom)
  b=f'<div class="case-back"><a href="index.html#work">← All projects</a><span>{i+1:02} / {len(projects):02}</span></div>'+custom
 nxt=projects[(i+1)%len(projects)]
 b+=f'<a class="next-project" href="{nxt["slug"]}.html"><span>CONTINUE EXPLORING</span><strong>{esc(nxt["name"])}</strong><span class="next-arrow" aria-hidden="true">↗</span></a>'
 (d/(p['slug']+'.html')).write_text(shell(p['name'],b,p['description'],True))
print('Built homepage and',len(projects),'case-study pages.')
