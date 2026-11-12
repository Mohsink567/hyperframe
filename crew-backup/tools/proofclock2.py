# ticking-clock hook bed for 'proof' video. usage: proofclock2.py out.wav ring.wav
import numpy as np, soundfile as sf, sys
from scipy import signal
SR=48000; DUR=34.4; N=int(SR*DUR); rng=np.random.default_rng(4)
L=np.zeros(N); R=np.zeros(N)
KEND=22.5; CTA=29.6
def add(x,st,g=1.,pan=0.):
    i=int(round(st*SR)); j=min(N,i+len(x))
    if i<0 or i>=N or j<=i: return
    y=x[:j-i]*g; L[i:j]+=y*np.sqrt(.5*(1-pan)); R[i:j]+=y*np.sqrt(.5*(1+pan))
def lp(x,fc): b,a=signal.butter(2,min(fc/(SR/2),.99),'low'); return signal.lfilter(b,a,x)
def bp(x,lo,hi): b,a=signal.butter(2,[lo/(SR/2),min(hi/(SR/2),.99)],'band'); return signal.lfilter(b,a,x)
def f(m): return 440*2**((m-69)/12)
def T(d): return np.arange(int(d*SR))/SR
def tick(hi=True):
    tt=T(.05); x=bp(rng.standard_normal(len(tt)),2500 if hi else 1600,7000)*np.exp(-tt*140)
    return x+.3*np.sin(2*np.pi*(3200 if hi else 2400)*tt)*np.exp(-tt*200)
def boom(d=2.5,g=1.):
    tt=T(d); s=np.sin(2*np.pi*np.cumsum(36+80*np.exp(-tt*6))/SR)*np.exp(-tt*1.7)
    n=lp(rng.standard_normal(len(tt)),900)*np.exp(-tt*5)*.4
    return np.tanh((s+n)*1.6)*g
def heart():
    tt=T(.3); fr=55+40*np.exp(-tt*25); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-tt*12)
def riser(d):
    n=int(d*SR); tt=np.arange(n)/SR; x=rng.standard_normal(n); out=np.zeros(n)
    for i in range(0,n,2400):
        fc=300+6000*(i/n)**2; seg=x[i:i+2400]; out[i:i+len(seg)]=bp(seg,fc*.7,fc*1.3)
    sw=np.sin(2*np.pi*np.cumsum(f(45)*(1+3*(tt/d)**2))/SR)*.25
    return (out+sw)*(tt/d)**2
def pad(ms,d,fc=900):
    tt=T(d); x=0
    for m in ms:
        for dt in (-.004,0,.004): x=x+signal.sawtooth(2*np.pi*f(m)*(1+dt)*tt+rng.random()*6)
    e=np.clip(np.minimum(tt/1.2,(d-tt)/1.0),0,1); return lp(x/len(ms)/3,fc)*e
def piano(m,d=2.,v=1.):
    tt=T(d); x=0
    for h,a in [(1,1),(2,.4),(3,.15),(4,.06)]: x=x+a*np.sin(2*np.pi*f(m)*h*tt)*np.exp(-tt*(2+h*1.3))
    return x*np.minimum(1,tt/.004)*v*.5
tt=T(KEND); dr=np.sin(2*np.pi*f(38)*tt)*.5+np.sin(2*np.pi*f(45)*tt)*.18
add(dr*np.interp(tt,[0,1,9.5,16,19.7,KEND],[.35,.5,.6,.8,1.,.0]),0,.25)
for a,b,ch in [(0,9.5,[50,53,57]),(9.5,15.9,[46,50,53]),(15.9,KEND,[48,51,55])]: add(pad(ch,b-a+1),a,.09)
stops=[(1.3,2.0),(7.2,8.0),(15.0,15.7),(19.6,20.3)]
t=1.5; k=0
while t<22.2:
    if not any(a<=t<b for a,b in stops): add(tick(k%2==0),t,.05+.10*(t/22.2),pan=.25 if k%2 else -.25)
    t+=.5; k+=1
t=9.5; per=1.0
while t<22.2: add(heart(),t,.30); add(heart(),t+.22,.18); t+=per; per=max(.62,per*.97)
for t,g in [(0.0,.9),(1.5,.5),(7.44,.8),(9.5,.5),(15.2,.7),(15.9,.45),(17.44,.55),(19.84,.85),(KEND,.6)]: add(boom(2.4,g),t)
add(riser(1.4),7.44-1.4,.20); add(riser(1.6),19.84-1.6,.26); add(riser(1.2),KEND-1.2,.2)
st=KEND; i=0; chords=[[50,54,57],[47,50,54],[43,47,50],[45,49,52]]
while st<CTA-0.3:
    for m in chords[i%4]: add(piano(m+12,1.4,.7),st,.9)
    st+=.6 if i<4 else 1.2; i+=1
add(pad([50,54,57,62],DUR-KEND,2000),KEND,.10)
for m in [38,50,57,62,66,69,74]: add(piano(m,DUR-CTA,.9),CTA,.8)
for i,m in enumerate([74,78,81,86]): add(piano(m,1.4,.45),CTA+.5+i*.18,.8,pan=.2)
def rev(x,seed):
    r=np.random.default_rng(seed); n=int(2.4*SR); ir=lp(r.standard_normal(n),6000)*np.exp(-np.arange(n)/SR*2.4); ir/=np.sqrt(np.sum(ir**2))
    return signal.fftconvolve(x,ir)[:len(x)]
mix=np.stack([L+.3*rev(L,1),R+.3*rev(R,2)],1)
mix=np.tanh(mix*1.2); mix/=np.max(np.abs(mix)); mix*=.89
fo=int(.8*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]
sf.write(sys.argv[1],mix,SR)
# phone ring: two trill bursts
tt=T(.5); trill=(np.sin(2*np.pi*1300*tt)+np.sin(2*np.pi*1650*tt))*(0.5+0.5*np.sign(np.sin(2*np.pi*20*tt)))*np.minimum(1,np.minimum(tt,.5-tt)/.02)
ring=np.zeros(int(1.4*SR)); ring[:len(trill)]+=trill; ring[int(.7*SR):int(.7*SR)+len(trill)]+=trill
ring=bp(ring,600,6000)*.4; sf.write(sys.argv[2],np.stack([ring,ring],1),SR); print("ok")
