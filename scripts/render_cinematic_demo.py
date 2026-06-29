#!/usr/bin/env python3
import json, math, subprocess, wave, struct, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / 'submission'
DATA = ROOT / 'data'
W, H, FPS = 1080, 1920, 24
BG_PATH = SUB / 'cinematic_background.jpg'
DASH_PATH = SUB / 'mobile-live-dashboard.png'
VOICE = SUB / 'cinematic_voiceover.ogg'
SILENT = SUB / 'otto-procurement-cinematic-silent.mp4'
SFX = SUB / 'cinematic_sfx.wav'
FINAL = SUB / 'otto-procurement-cinematic-x-demo.mp4'

def probe_duration(path):
    out = subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)], text=True).strip()
    return float(out)

def pick_font(size, bold=False, mono=False):
    candidates=[]
    if mono:
        candidates=['/System/Library/Fonts/Menlo.ttc','/System/Library/Fonts/SFNSMono.ttf','/System/Library/Fonts/Supplemental/Courier New.ttf']
    elif bold:
        candidates=['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/System/Library/Fonts/Supplemental/Helvetica Bold.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']
    else:
        candidates=['/System/Library/Fonts/Supplemental/Arial.ttf','/System/Library/Fonts/Supplemental/Helvetica.ttf']
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

F_MICRO=pick_font(22, mono=True); F_CAP=pick_font(28); F_BODY=pick_font(36); F_BODY_B=pick_font(38, True)
F_H=pick_font(58, True); F_H2=pick_font(72, True); F_NUM=pick_font(112, True, True); F_BIG=pick_font(155, True, True); F_MONO=pick_font(30, mono=True); F_MONO_B=pick_font(34, True, True)

COL = {
    'bg': (8,9,10), 'panel': (15,16,18), 'panel2': (25,26,28), 'text': (247,248,248),
    'muted': (180,188,200), 'dim': (98,102,109), 'green': (118,185,0), 'green2': (0,255,65),
    'stripe': (99,91,255), 'red': (255,23,68), 'amber': (255,179,0), 'gold': (255,209,102), 'white': (255,255,255)
}

def clamp(x,a=0,b=1): return max(a,min(b,x))
def ease(t):
    t=clamp(t); return 1-(1-t)*(1-t)*(1-t)
def lerp(a,b,t): return a+(b-a)*t

def text_size(draw, text, font):
    bb=draw.textbbox((0,0), text, font=font); return bb[2]-bb[0], bb[3]-bb[1]
def centered(draw, y, text, font, fill, x0=0, x1=W):
    tw,th=text_size(draw,text,font); draw.text((x0+(x1-x0-tw)/2,y), text, font=font, fill=fill); return th

def wrap_lines(draw, text, font, width):
    words=text.split(); lines=[]; line=''
    for w in words:
        test=(line+' '+w).strip()
        if text_size(draw,test,font)[0] <= width or not line: line=test
        else: lines.append(line); line=w
    if line: lines.append(line)
    return lines

def draw_wrapped(draw, xy, text, font, fill, width, spacing=8):
    x,y=xy
    for line in wrap_lines(draw,text,font,width):
        draw.text((x,y), line, font=font, fill=fill); y += font.size + spacing
    return y

def fmt_money(n, cents=False):
    if cents: return '$' + f'{n:,.2f}'
    return '$' + f'{int(round(n)):,.0f}'

def rounded(draw, box, r=24, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def glow_rect(draw, box, color, width=2):
    x0,y0,x1,y1=box
    for i,alpha in enumerate([60,35,18]):
        pad=8+i*8
        overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
        od.rounded_rectangle((x0-pad,y0-pad,x1+pad,y1+pad), radius=28+pad, outline=color+(alpha,), width=width+i*2)
        return overlay

def make_base(bg_img, vignette=True):
    img = bg_img.copy().convert('RGB')
    d = ImageDraw.Draw(img, 'RGBA')
    # Linear / NVIDIA grid
    for x in range(0,W,90): d.line((x,0,x,H), fill=(255,255,255,10), width=1)
    for y in range(0,H,90): d.line((0,y,W,y), fill=(255,255,255,8), width=1)
    if vignette:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
        od.rectangle((0,0,W,H), fill=(0,0,0,90))
        # dark top/bottom safe zones
        od.rectangle((0,0,W,220), fill=(0,0,0,90)); od.rectangle((0,H-300,W,H), fill=(0,0,0,115))
        img=Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    return img

def top_label(draw, text):
    rounded(draw,(52,46,52+len(text)*15+50,96),22,fill=(0,0,0,120),outline=COL['green'],width=2)
    draw.text((78,60), text, font=F_MICRO, fill=COL['green'])

def bottom_caption(draw, text):
    y=H-210
    rounded(draw,(60,y-20,W-60,H-64),24,fill=(0,0,0,185),outline=(255,255,255,30),width=1)
    lines=wrap_lines(draw,text,F_BODY_B,W-160)
    cy=y
    for line in lines[:3]:
        centered(draw, cy, line, F_BODY_B, COL['text'], 80, W-80); cy += F_BODY_B.size+6

def add_scanlines(img, opacity=18):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(0,H,4): od.line((0,y,W,y), fill=(0,0,0,opacity), width=1)
    return Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')

def prepare_bg():
    if BG_PATH.exists(): bg=Image.open(BG_PATH).convert('RGB')
    else: bg=Image.new('RGB',(W,H),COL['bg'])
    # cover-crop portrait
    ratio=max(W/bg.width,H/bg.height); bg=bg.resize((int(bg.width*ratio), int(bg.height*ratio)), Image.Resampling.LANCZOS)
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width+W)//2,(bg.height+H)//2))
    bg=bg.filter(ImageFilter.GaussianBlur(4))
    bg=ImageEnhance.Brightness(bg).enhance(0.38)
    bg=ImageEnhance.Contrast(bg).enhance(1.22)
    return bg

# Load facts
audit=json.loads((DATA/'audit.json').read_text()); evidence=json.loads((DATA/'evidence_pack.json').read_text()); ledger=json.loads((DATA/'ledger.json').read_text())
FACTS={'stack':audit['before_annual_spend'],'savings':audit['annual_savings'],'fee':audit['success_fee_amount'],'cost':evidence['agent_pnl']['agent_operating_cost'],'net':evidence['agent_pnl']['customer_net_first_year_value'],'treasury':ledger['balance_cents']/100}

def draw_money(draw, label, value, y, progress, color):
    # Keep the exact final number onscreen; animate surrounding panels instead of showing misleading intermediate dollar values.
    s = fmt_money(value, cents=(value<100))
    centered(draw,y,s,F_BIG if value>=1000 else F_NUM,color)
    centered(draw,y+140,label,F_CAP,COL['muted'])

def scene_hook(img, t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'SAFETY FIRST')
    # proposal card
    p=clamp(t/1.5); y=int(260-40*(1-p)); alpha=int(255*p)
    rounded(d,(72,y,1008,y+360),28,fill=(17,18,20,220),outline=(255,255,255,45),width=1)
    d.text((110,y+42),'PROPOSED SAVINGS',font=F_MICRO,fill=COL['amber'])
    d.text((110,y+100),'Cut Slack Enterprise add-ons',font=F_H,fill=COL['text'])
    d.text((110,y+200),'Tempting savings',font=F_CAP,fill=COL['muted'])
    d.text((640,y+180),'$9,360',font=F_NUM,fill=COL['amber'])
    rounded(d,(110,y+285,430,y+336),16,fill=(255,179,0,25),outline=COL['amber'],width=1)
    d.text((136,y+300),'APPROVE CUT',font=F_MICRO,fill=COL['amber'])
    if t>1.8:
        q=ease((t-1.8)/0.55); scale=lerp(1.9,1.0,q); # stamp
        stamp='BLOCKED'
        fs=int(130*scale); f=pick_font(fs, True)
        tw,th=text_size(d,stamp,f); cx,cy=W/2,820
        box=(cx-tw/2-44,cy-th/2-28,cx+tw/2+44,cy+th/2+32)
        d.rounded_rectangle(box, radius=28, fill=(120,0,20,230), outline=COL['red'], width=5)
        d.text((cx-tw/2,cy-th/2-8),stamp,font=f,fill=(255,240,240,255))
        if t<2.55:
            # impact flash
            d.rectangle((0,0,W,H),fill=(255,23,68,int(90*(1-q))))
    if t>2.5:
        rounded(d,(86,1000,994,1268),24,fill=(0,0,0,170),outline=COL['red'],width=2)
        d.text((126,1038),'Reason',font=F_CAP,fill=COL['red'])
        draw_wrapped(d,(126,1094),'Legal hold + executive workspace dependencies. Risk greater than savings.',F_BODY,COL['text'],820)
    bottom_caption(d,"Otto doesn't just find savings. It knows which savings not to take.")

vendor_names=['Slack','Figma','Zoom','Asana','Datadog','Intercom','Dropbox','Loom','Miro','Airtable','Calendly','New Relic','Zendesk','GitHub','Notion','Canva','HubSpot','Google','Okta','Lucid']
def scene_stack(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'STACK UNDER MANAGEMENT')
    centered(d,145,'20 vendors normalized',F_H,COL['text'])
    draw_money(d,'annual spend under audit',FACTS['stack'],340,clamp(t/3.0),COL['text'])
    # Do not show a tiny logo wall; show a few large representative tiles + the count.
    names=['Slack','Figma','Zoom','Asana','Datadog','Intercom']
    coords=[(90,770),(610,770),(90,930),(610,930),(90,1090),(610,1090)]
    for i,(name,(x,y)) in enumerate(zip(names,coords)):
        appear=ease(clamp((t-1.3-i*.18)/.45))
        if appear<=0: continue
        yy=y+int((1-appear)*35)
        rounded(d,(x,yy,x+380,yy+118),22,fill=(18,20,24,230),outline=COL['green'] if i<3 else (90,95,106),width=2)
        d.text((x+30,yy+36),name,font=F_BODY_B,fill=COL['text'])
        d.text((x+300,yy+36),'✓',font=F_BODY_B,fill=COL['green'])
    # multiplier / scan result
    if t>3.8:
        q=ease((t-3.8)/1.0)
        rounded(d,(150,1320,930,1460),30,fill=(0,0,0,210),outline=COL['green'],width=3)
        centered(d,1355,'+14 more apps scanned',F_BODY_B,COL['green'])
        d.line((170,1515,int(170+740*q),1515),fill=COL['green2'],width=6)
    bottom_caption(d,'Every seat. Every tier. Every renewal window.')

def evidence_card(d, box, title, amount, evidence_lines, color=COL['green']):
    x0,y0,x1,y1=box
    rounded(d,box,24,fill=(18,20,24,230),outline=(255,255,255,45),width=1)
    d.text((x0+28,y0+24),'EVIDENCE',font=F_MICRO,fill=color)
    draw_wrapped(d,(x0+28,y0+66),title,F_BODY_B,COL['text'],x1-x0-56,spacing=2)
    d.text((x0+28,y1-94),amount,font=F_H,fill=color)
    yy=y0+168
    for line in evidence_lines[:3]:
        d.text((x0+28,yy),'• '+line,font=F_MICRO,fill=COL['muted']); yy+=34

def scene_evidence(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'EVIDENCE WALL')
    centered(d,140,'Every dollar has receipts',F_H,COL['text'])
    cards=[('Retire New Relic','+$18,000',['invoice NR-2026-05','4 active / 20 seats','Datadog migration ready']),('Right-size Figma','+$5,760',['24 inactive editors','viewer role allowed','90-day usage proof']),('Route Zendesk queues','+$9,600',['3 active agents','Intercom mapped','migration plan ready']),('Unused seats bundle','+$12,600',['owner records','low utilization','renewal leverage'])]
    idx=min(len(cards)-1,int(t/2.15)); local=(t-idx*2.15)/2.15
    title,amt,lines=cards[idx]
    y=int(340 + (1-ease(clamp(local/.35)))*60)
    rounded(d,(70,y,1010,y+760),36,fill=(18,20,24,242),outline=COL['green'],width=3)
    d.text((115,y+55),'CASE FILE 0'+str(idx+1),font=F_CAP,fill=COL['green'])
    draw_wrapped(d,(115,y+125),title,F_H,COL['text'],820,spacing=6)
    centered(d,y+330,amt,F_BIG,COL['green'])
    yy=y+520
    for line in lines:
        rounded(d,(125,yy,955,yy+70),16,fill=(255,255,255,18),outline=(255,255,255,40),width=1)
        d.text((155,yy+19),line,font=F_CAP,fill=COL['muted'])
        yy+=90
    # progress dots
    for i in range(4):
        fill=COL['green'] if i==idx else (80,84,90)
        d.ellipse((440+i*55,1260,464+i*55,1284),fill=fill)
    if t>7.2:
        rounded(d,(110,1370,970,1505),24,fill=(0,0,0,210),outline=COL['gold'],width=2)
        centered(d,1405,'7 APPROVED ACTIONS',F_H,COL['gold'])
    bottom_caption(d,'Usage evidence. Invoice evidence. Contract evidence. Renewal evidence.')

def scene_council(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'ADVERSARIAL MoA COUNCIL')
    centered(d,150,'The council argues before money moves',F_H,COL['text'])
    roles=[('Finance','P&L valid',COL['green']),('Procurement','Path credible',COL['green']),('Risk','Slack blocked',COL['red']),('Engineering','Run verified',COL['green']),('Aggregator','7 actions approved',COL['gold'])]
    y=330
    for i,(role,line,color) in enumerate(roles):
        appear=ease(clamp((t-i*.55)/.5));
        if appear<=0: continue
        x=int(70+(1-appear)*-80); yy=y+i*210
        rounded(d,(x,yy,1010,yy+156),22,fill=(18,20,24,230),outline=color,width=2)
        d.text((x+34,yy+28),role,font=F_BODY_B,fill=color)
        # type-on line
        n=int(len(line)*clamp((t-i*.55-.25)/.8)); shown=line[:max(0,n)]
        d.text((x+34,yy+84),shown,font=F_H if role=='Risk' else F_BODY,fill=COL['text'])
    # consensus ring
    if t>3.2:
        q=(math.sin((t-3.2)*math.pi*2)*0.5+0.5)
        d.ellipse((430,1420,650,1640),outline=COL['green']+(int(120+80*q),),width=5)
        centered(d,1485,'CONSENSUS',F_CAP,COL['green'])
    bottom_caption(d,'Finance validates. Risk kills the bad cut. Engineering verifies the run.')

def scene_manifest(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'SIGNED DRY-RUN MANIFEST')
    centered(d,145,'Proof before execution',F_H,COL['text'])
    items=[('mode','DRY RUN',COL['green']),('approved savings','$62,880',COL['green']),('vendor actions executed','0',COL['red']),('human approval','REQUIRED',COL['amber']),('signature','dryrun_10ec26e1',COL['gold'])]
    y=300
    for i,(label,value,color) in enumerate(items):
        p=ease(clamp((t-i*.75)/.45))
        if p<=0: continue
        yy=y+i*220+int((1-p)*40)
        rounded(d,(70,yy,1010,yy+150),26,fill=(18,20,24,235),outline=color,width=2)
        d.text((112,yy+26),label.upper(),font=F_MICRO,fill=COL['muted'])
        f=F_H if len(value)<12 else F_BODY_B
        d.text((112,yy+72),value,font=f,fill=color)
    if t>4.6:
        rounded(d,(105,1450,975,1580),24,fill=(0,0,0,230),outline=COL['gold'],width=4)
        centered(d,1485,'NO VENDOR ACTION TAKEN',F_BODY_B,COL['gold'])
    bottom_caption(d,'No hidden click. Human approval still required.')

def scene_numbers(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'TREASURY + P&L')
    centered(d,135,'The economics are the demo',F_H,COL['text'])
    stages=[('APPROVED SAVINGS',FACTS['savings'],COL['green'],'money found, risk-reviewed'),('SUCCESS FEE',FACTS['fee'],COL['gold'],'20% only when savings exist'),('AGENT RUN COST',FACTS['cost'],COL['red'],'measured operating cost'),('CUSTOMER NET VALUE',FACTS['net'],COL['green'],'value after success fee')]
    idx=min(3,int(t/2.65)); local=(t-idx*2.65)/2.65
    label,val,color,sub=stages[idx]
    rounded(d,(70,320,1010,1120),42,fill=(18,20,24,238),outline=color,width=4)
    centered(d,395,label,F_BODY_B,COL['muted'])
    centered(d,570,fmt_money(val,cents=(val<100)),F_BIG,color)
    centered(d,760,sub,F_BODY,COL['text'])
    # flow chips: previous / current / next
    y=1220
    for i,(lab,v,c,_) in enumerate(stages):
        x=110; yy=y+i*92
        active=i==idx; done=i<idx
        border=c if active or done else (70,74,82)
        fill=(18,20,24,230) if active else (12,13,15,180)
        rounded(d,(x,yy,970,yy+70),18,fill=fill,outline=border,width=2 if active else 1)
        d.text((140,yy+20),lab,font=F_MICRO,fill=COL['text'] if active or done else COL['dim'])
        if done:
            d.text((760,yy+20),fmt_money(v,cents=(v<100)),font=F_MICRO,fill=c)
        elif active:
            d.text((760,yy+20),'NOW',font=F_MICRO,fill=c)
    bottom_caption(d,'One run. Visible revenue. Visible cost. Visible customer value.')

def scene_autonomy(img,t):
    d=ImageDraw.Draw(img,'RGBA'); top_label(d,'NVIDIA PROOF LANE')
    centered(d,130,'Nemotron reviews before money moves',F_H,COL['text'])
    nodes=['schedule','fetch','MoA review','manifest','publish']
    x=110; y=330; node_h=110
    for i,n in enumerate(nodes):
        p=clamp((t-i*.65)/.45)
        col=COL['green'] if p>=1 else (95,98,105)
        rounded(d,(x,y+i*170,970,y+i*170+node_h),22,fill=(18,20,24,230),outline=col,width=2)
        d.text((x+36,y+i*170+36),n,font=F_BODY_B,fill=COL['text'])
        if p>=1: d.text((860,y+i*170+38),'✓',font=F_H,fill=COL['green'])
        if i<len(nodes)-1: d.line((540,y+i*170+node_h,540,y+(i+1)*170),fill=COL['green']+(90,),width=3)
    # inference lane
    rounded(d,(70,1250,1010,1580),28,fill=(0,0,0,220),outline=COL['green'],width=2)
    d.text((110,1290),'NEMOTRON + POLICY GATE',font=F_BODY_B,fill=COL['green'])
    # animated trace
    p=clamp((t-3.8)/2.2); xend=int(150+760*p)
    d.line((150,1410,xend,1410),fill=COL['green2'],width=5)
    d.ellipse((xend-10,1400,xend+10,1420),fill=COL['green2'])
    d.text((110,1480),'Nemotron 3 Ultra via Ollama Cloud',font=F_BODY_B,fill=COL['green'])
    d.text((110,1530),'NemoClaw-style policy scaffold',font=F_BODY,fill=COL['muted'])
    bottom_caption(d,'Nemotron reviews risk. Policy gates approve or block the next move.')

def scene_close(img,t,dash):
    d=ImageDraw.Draw(img,'RGBA')
    # phone/dashboard reveal
    p=clamp(t/3.0)
    rounded(d,(80,110,1000,1180),34,fill=(0,0,0,240),outline=(255,255,255,45),width=1)
    if dash:
        # crop top mobile screenshot and fit
        crop=dash.crop((0,0,dash.width,min(dash.height,1800)))
        ratio=min(860/crop.width,1000/crop.height); crop=crop.resize((int(crop.width*ratio),int(crop.height*ratio)),Image.Resampling.LANCZOS)
        crop=ImageEnhance.Brightness(crop).enhance(0.95)
        img.paste(crop,(110,145))
    d.rectangle((80,110,1000,1180),outline=COL['green']+(int(120*p),),width=4)
    # darken lower half and make the CTA readable in a feed
    d.rectangle((0,1180,W,H),fill=(0,0,0,175))
    y=1225
    centered(d,y,'Otto Procurement Profit Agent',F_BODY_B,COL['text']); y+=105
    centered(d,y,'Find savings.',F_H,COL['green']); y+=78
    centered(d,y,'Gate risk.',F_H,COL['red']); y+=78
    centered(d,y,'Prove the business.',F_H,COL['gold']); y+=98
    rounded(d,(110,y,970,y+118),28,fill=(99,91,255,245),outline=(255,255,255,110),width=3)
    centered(d,y+26,'LIVE DEMO',F_H,COL['white'])
    centered(d,y+152,'kcemate.github.io/otto-procurement-agent',F_CAP,COL['muted'])

def render_video():
    bg=prepare_bg()
    dash=None
    if DASH_PATH.exists(): dash=Image.open(DASH_PATH).convert('RGB')
    voice_dur=probe_duration(VOICE)
    total=voice_dur+1.0
    scenes=[('hook',5.0,scene_hook),('stack',6.0,scene_stack),('evidence',9.0,scene_evidence),('council',8.0,scene_council),('manifest',7.0,scene_manifest),('numbers',11.0,scene_numbers),('autonomy',8.0,scene_autonomy),('close',max(6.0,total-54.0),None)]
    total=sum(s[1] for s in scenes)
    frames=int(math.ceil(total*FPS))
    cmd=['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(SILENT)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    scene_start=0.0
    for name,dur,fn in scenes:
        nframes=int(round(dur*FPS))
        for f in range(nframes):
            t=f/FPS
            img=make_base(bg)
            if fn is None: scene_close(img,t,dash)
            else: fn(img,t)
            img=add_scanlines(img,10)
            proc.stdin.write(img.tobytes())
        scene_start+=dur
    proc.stdin.close(); proc.wait()
    if proc.returncode: raise SystemExit(proc.returncode)
    return total

def write_sfx(duration):
    sr=48000; n=int(duration*sr); data=[0.0]*n
    def add_sine(start,dur,freq,amp=0.2,decay=True):
        s=int(start*sr); m=int(dur*sr)
        for i in range(m):
            if s+i>=n: break
            env=(1-i/m) if decay else 1.0
            data[s+i]+=amp*env*math.sin(2*math.pi*freq*i/sr)
    def add_noise(start,dur,amp=0.03):
        s=int(start*sr); m=int(dur*sr)
        for i in range(m):
            if s+i>=n: break
            env=math.sin(math.pi*i/max(1,m))
            data[s+i]+=amp*env*(random.random()*2-1)
    # low drone
    for i in range(n): data[i]+=0.018*math.sin(2*math.pi*44*i/sr)+0.010*math.sin(2*math.pi*88*i/sr)
    for ts in [2.0,5.0,11.0,15.0,20.0,27.0,35.0,46.0,54.0]: add_sine(ts,0.35,72,0.18)
    for ts in [12.2,13.1,14.0,15.0,36.0,38.2,40.4,42.6]: add_noise(ts,0.08,0.08); add_sine(ts,0.08,880,0.06)
    for ts in [22.0,22.6,23.2,23.8,24.4,47.0,47.6,48.2,48.8,49.4]: add_sine(ts,0.12,660,0.06)
    # normalize soft
    mx=max(0.01,max(abs(x) for x in data)); scale=min(1.0,0.35/mx)
    with wave.open(str(SFX),'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        for x in data:
            v=int(max(-1,min(1,x*scale))*32767); w.writeframes(struct.pack('<h',v))

def mux_audio():
    cmd=['ffmpeg','-y','-i',str(SILENT),'-i',str(VOICE),'-i',str(SFX),'-filter_complex','[1:a]volume=1.0[a1];[2:a]volume=0.45[a2];[a1][a2]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(FINAL)]
    subprocess.check_call(cmd)

def main():
    total=render_video(); write_sfx(total); mux_audio()
    print(json.dumps({'ok':True,'silent':str(SILENT),'sfx':str(SFX),'final':str(FINAL),'duration_target':total},indent=2))
if __name__=='__main__': main()
