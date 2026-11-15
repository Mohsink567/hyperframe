# Upbeat catchy hook beat (120 BPM, A minor). usage: hookbeat.py out.wav
import numpy as np, soundfile as sf, sys
from scipy import signal
SR=48000; DUR=21.8; N=int(SR*DUR); rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N); SC=np.ones(N)   # SC = sidechain gain
DROP=2.0; KEND=14.0; CTA=17.0; B=0.5          # beat length
HITS=[]                              # stop-downs
def add(x,st,g=1.,pan=0.,duck=True):
    i=int(round(st*SR)); j=min(N,i+len(x))
    if i<0 or i>=N or j<=i: return
    y=x[:j-i]*g; L[i:j]+=y*np.sqrt(.5*(1-pan))*(1 if not duck else 1); R[i:j]+=y*np.sqrt(.5*(1+pan))
def T(d): return np.arange(int(d*SR))/SR
def lp(x,fc): b,a=signal.butter(2,min(fc/(SR/2),.99),'low'); return signal.lfilter(b,a,x)
def hp(x,fc): b,a=signal.butter(2,fc/(SR/2),'high'); return signal.lfilter(b,a,x)
def bp(x,lo,hi): b,a=signal.butter(2,[lo/(SR/2),min(hi/(SR/2),.99)],'band'); return signal.lfilter(b,a,x)
def f(m): return 440*2**((m-69)/12)
def stopped(t,w=0.9): return any(h-0.05<=t<h+w for h in HITS)
# ---------- instruments
def kick():
    tt=T(.35); fr=48+120*np.exp(-tt*35); x=np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-tt*9)
    return np.tanh(x*2.2)*.9 + bp(rng.standard_normal(len(tt)),2000,6000)*np.exp(-tt*400)*.25
def clap():
    tt=T(.3); n=rng.standard_normal(len(tt)); e=np.zeros(len(tt))
    for o in (0,.009,.018): e+=np.exp(-np.clip(tt-o,0,None)*60)*(tt>=o)
    return bp(n,900,5000)*(e*.5+np.exp(-tt*14)*.5)*.8
def hat(op=False):
    tt=T(.25 if op else .05); return hp(rng.standard_normal(len(tt)),7000)*np.exp(-tt*(12 if op else 90))*.5
def bass(m,d):
    tt=T(d); x=np.sin(2*np.pi*f(m)*tt)+.25*np.sin(2*np.pi*f(m)*2*tt)
    return np.tanh(x*1.3)*np.minimum(1,tt/.01)*np.clip((d-tt)/.05,0,1)*.55
def pluck(m,d=.45,bright=2600):
    tt=T(d); x=signal.sawtooth(2*np.pi*f(m)*tt)+signal.sawtooth(2*np.pi*f(m)*1.006*tt)
    env=np.exp(-tt*7); y=np.zeros(len(tt))
    for i in range(0,len(tt),1200):
        fc=400+bright*np.exp(-i/SR*9); seg=x[i:i+1200]; y[i:i+len(seg)]=lp(seg,fc)
    return y*env*np.minimum(1,tt/.003)*.32
def padc(ms,d,fc=1800):
    tt=T(d); x=0
    for m in ms:
        for dt in (-.006,0,.006): x=x+signal.sawtooth(2*np.pi*f(m)*(1+dt)*tt+rng.random()*6)
    e=np.clip(np.minimum(tt/.4,(d-tt)/.4),0,1); return lp(x/len(ms)/3,fc)*e
def riser(d):
    n=int(d*SR); tt=np.arange(n)/SR; x=rng.standard_normal(n); out=np.zeros(n)
    for i in range(0,n,2400):
        fc=400+7000*(i/n)**2; seg=x[i:i+2400]; out[i:i+len(seg)]=bp(seg,fc*.7,fc*1.3)
    return out*(tt/d)**2*.6
def impact(g=1.):
    tt=T(2.2); s=np.sin(2*np.pi*np.cumsum(40+90*np.exp(-tt*8))/SR)*np.exp(-tt*2.2)
    n=lp(rng.standard_normal(len(tt)),1500)*np.exp(-tt*6)*.5
    return np.tanh((s+n)*1.8)*g
# ---------- arrangement
prog=[(53,[53,57,60]),(55,[55,59,62]),(57,[57,60,64]),(52,[52,56,59])]  # Am F C G (bass root, chord)
hook=[72,76,79,76, 74,72,71,72]        # catchy 8-step motif (8th notes)
hook2=[79,76,74,76, 79,81,79,76]
# intro: riser + filtered pad
add(riser(1.95),0.05,.55); add(padc([57,60,64],2.1,900),0,.2)
for k in range(4): add(clap(),0.0+k*B,.18+.06*k)
add(impact(.9),DROP)
bar=0; t=DROP
while t<CTA-0.01:
    root,ch=prog[bar%4]; outro=t>=KEND
    for bt in range(4):
        tb=t+bt*B
        if tb>=CTA: break
        if not stopped(tb):
            add(kick(),tb,.75 if not outro else .85)
            i=int(tb*SR); j=min(N,i+int(.22*SR)); SC[i:j]=np.minimum(SC[i:j],np.linspace(.45,1,j-i))
            if bt in (1,3): add(clap(),tb,.42,pan=.05)
            for k in range(2):
                th=tb+k*B/2
                if bt==3 and k==1 and bar%2==1: add(hat(True),th,.22,pan=.3)
                else: add(hat(),th,.28 if k else .18,pan=.3)
            if bar%4==3 and bt==3:                      # hat roll fill
                for r in range(4): add(hat(),tb+B/2+r*B/8,.18,pan=-.3)
            add(bass(root-24,B*.9),tb,.9)
        # melody: 8th-note pluck motif, sparser under the voice
        mel=hook2 if (outro and bar%2) else hook
        for k in range(2):
            th=tb+k*B/2; idx=(bt*2+k)%8
            if stopped(th): continue
            m=mel[idx]+(0 if not outro else 12)
            add(pluck(m,.45,2600 if outro else 1700),th,.55 if outro else .42,pan=-.2 if k else .2)
    add(padc(ch,4*B+.3,1400 if not t>=KEND else 2600),t,.14 if t<KEND else .2)
    bar+=1; t+=4*B
for h in HITS: add(impact(.8),h); add(riser(.8),h-.8,.35)
add(riser(1.0),KEND-1.0,.4); add(impact(.6),KEND)
# CTA resolve
add(impact(.5),CTA)
for m in [45,57,64,69,72,76]: add(padc([m],DUR-CTA,2200),CTA,.12)
for i,m in enumerate([81,84,88,93]): add(pluck(m,.9,3500),CTA+.3+i*.15,.45,pan=.2)
# ---------- mix
L*=SC; R*=SC
def rev(x,seed):
    r=np.random.default_rng(seed); n=int(1.6*SR); ir=lp(r.standard_normal(n),7000)*np.exp(-np.arange(n)/SR*3.2); ir/=np.sqrt(np.sum(ir**2))
    return signal.fftconvolve(x,ir)[:len(x)]
mix=np.stack([L+.22*rev(L,1),R+.22*rev(R,2)],1)
mix=hp(mix.T,35).T
mix=np.tanh(mix*1.1); mix/=np.max(np.abs(mix)); mix*=.9
fo=int(.9*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]
sf.write(sys.argv[1],mix,SR); print("ok")
