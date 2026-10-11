import sys, numpy as np, subprocess
sys.path.insert(0, sys.argv[1]); from cfg import *
sr=44100; N=int(DUR*sr); t=np.arange(N)/sr
out_dir=sys.argv[1]
voice=np.frombuffer(subprocess.run(["ffmpeg","-v","quiet","-i",sys.argv[2],"-f","f32le","-ac","1","-ar",str(sr),"-"],capture_output=True).stdout,dtype=np.float32).astype(np.float64)
V=np.zeros(N); s=int(VO*sr); V[s:s+len(voice)]=voice[:N-s]
V*=10**(5/20)
rng=np.random.default_rng(1)
def hz(m): return 440*2**((m-69)/12)
def env_adsr(n,a,r):
    e=np.ones(n); na=int(a*sr); nr=int(r*sr)
    if na: e[:na]=np.linspace(0,1,na)
    if nr: e[-nr:]*=np.linspace(1,0,nr)
    return e
def add(buf,t0,sig,g=1.0):
    i=int(t0*sr)
    if i>=N: return
    j=min(N,i+len(sig)); buf[i:j]+=g*sig[:j-i]
def tone(f,d,harm=6,decay=1.6,det=0.0):
    tt=np.arange(int(d*sr))/sr; x=0
    for k in range(1,harm+1):
        for dd in ([0] if not det else [-det,det]):
            x=x+np.sin(2*np.pi*f*k*(1+dd)*tt+rng.uniform(0,6))/k**decay
    return x
def lowpass(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/sr)
    X/= np.sqrt(1+(f/fc)**4); return np.fft.irfft(X,len(x))
music=np.zeros(N); drums=np.zeros(N); sfx=np.zeros(N)
bar=2.0  # 120bpm
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
# PAD whole song
for b in range(int(DUR/bar)+1):
    c=chords[b%4]; t0=b*bar
    for m in c+[c[0]+12]:
        sig=tone(hz(m),bar+0.6,harm=5,decay=1.8,det=0.003)*env_adsr(int((bar+0.6)*sr),0.4,0.8)
        add(music,t0,sig,0.05)
# intro chimes
for i,tt in enumerate(np.arange(0.4,6.4,0.25)):
    m=[76,79,81,84,88,84,81,79][i%8]
    sig=tone(hz(m),1.2,harm=3,decay=2.5)*np.exp(-np.arange(int(1.2*sr))/sr*4)
    add(music,tt,sig,0.035*(0.5+tt/6.4))
# bass + arps from 14.8
for b in range(int(DUR/bar)+1):
    t0=b*bar; c=chords[b%4]
    for k in range(8):
        tt=t0+k*0.25
        if not (14.8<=tt<25.4 or 30.4<=tt<44.5): continue
        d=0.22; sig=tone(hz(c[0]-12),d,harm=4,decay=1.2)*np.exp(-np.arange(int(d*sr))/sr*8)
        add(music,tt,sig,0.14)
    for k in range(16):
        tt=t0+k*0.125
        if not (31.0<=tt<44.5 or 20.0<=tt<25.4): continue
        m=(c+[c[0]+12])[ [0,1,2,3,2,1,2,3][k%8] ]+12
        d=0.14; sig=np.sign(np.sin(2*np.pi*hz(m)*np.arange(int(d*sr))/sr))*np.exp(-np.arange(int(d*sr))/sr*18)
        add(music,tt,lowpass(sig,3500),0.03)
def kick():
    d=0.45; tt=np.arange(int(d*sr))/sr; f=45+90*np.exp(-tt*28)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*7)
def snare(d=0.22):
    tt=np.arange(int(d*sr))/sr; n=rng.standard_normal(len(tt))
    return (lowpass(n,6000)*0.7+np.sin(2*np.pi*190*tt)*0.5)*np.exp(-tt*16)
def hat():
    d=0.06; n=rng.standard_normal(int(d*sr)); n=np.diff(n,prepend=0)
    return n*np.exp(-np.arange(len(n))/sr*60)
K=kick(); SN=snare(); HT=hat()
for k in range(int(DUR/0.5)):
    tt=k*0.5
    if 14.8<=tt<25.4 or 30.4<=tt<44.5:
        add(drums,tt,K,0.55)
        add(drums,tt+0.25,HT,0.08)
        if k%2==1: add(drums,tt,SN,0.28)
# build-up roll 25.4..30.4
tt=25.4; step=0.25
while tt<30.3:
    add(drums,tt,snare(0.12),0.10+0.25*(tt-25.4)/5); tt+=step; step=max(0.055,step*0.93)
# riser noise
def riser(t0,d,g):
    n=rng.standard_normal(int(d*sr)); x=np.linspace(0,1,len(n))
    sig=lowpass(n,4000)*x**2; add(sfx,t0,sig,g)
riser(5.0,1.6,0.12); riser(13.6,1.2,0.08); riser(24.2,1.2,0.08); riser(27.0,3.4,0.16); riser(31.8,1.2,0.07)
def boom(d=2.5,f0=60):
    tt=np.arange(int(d*sr))/sr; n=lowpass(rng.standard_normal(len(tt)),900)
    return (np.sin(2*np.pi*np.cumsum(f0+80*np.exp(-tt*10))/sr)*0.9+n*0.6)*np.exp(-tt*2.2)
def thud():
    d=0.35; tt=np.arange(int(d*sr))/sr
    return (np.sin(2*np.pi*np.cumsum(70+120*np.exp(-tt*30))/sr)+lowpass(rng.standard_normal(len(tt)),1500)*0.4)*np.exp(-tt*12)
for lt in LETTER_T: add(sfx,lt+0.55,thud(),0.45)
add(sfx,6.6,boom(1.8,50),0.35)
# countdown ticks / tnt fuse
for ct in COUNT_T:
    add(sfx,ct,tone(hz(81),0.5,harm=3)*np.exp(-np.arange(int(0.5*sr))/sr*8),0.18)
fuse=lowpass(rng.standard_normal(int(4.2*sr)),7000)*0.5; fuse*= (0.6+0.4*np.sin(np.arange(len(fuse))/sr*2*np.pi*13))
add(sfx,26.2,fuse,0.05)
B=boom(3.5,40); add(sfx,BOOM_T,B,0.9)
crash=lowpass(rng.standard_normal(int(3*sr)),9000)*np.exp(-np.arange(int(3*sr))/sr*1.6); add(sfx,BOOM_T,crash,0.18)
# whooshes on cards
for ct in CARD_T:
    n=rng.standard_normal(int(0.5*sr)); e=np.sin(np.linspace(0,np.pi,len(n)))**2
    add(sfx,ct-0.1,lowpass(n,2500)*e,0.10)
# fireworks
for (t0,x,y,c,n) in FIREWORKS:
    d=1.4; tt=np.arange(int(d*sr))/sr
    pop=lowpass(rng.standard_normal(len(tt)),3000)*np.exp(-tt*9)
    cr=rng.standard_normal(len(tt))*(rng.random(len(tt))<0.004)*np.exp(-tt*2)*(tt>0.25)
    pan=x/1920
    add(sfx,t0,pop*0.5+cr*0.6,0.16)
    whistle=np.sin(2*np.pi*np.cumsum(np.linspace(900,1800,int(0.6*sr)))/sr)*np.linspace(0,1,int(0.6*sr))*0.15
    add(sfx,t0-0.6,whistle,0.05)
# sleigh bells + Jingle Bells (public domain) melody
def bell(f, d=1.2):
    tt=np.arange(int(d*sr))/sr; x=0
    for k,(m,g) in enumerate([(1,1),(2.76,0.5),(5.4,0.3),(8.93,0.15)]):
        x=x+g*np.sin(2*np.pi*f*m*tt)*np.exp(-tt*(3+3*k))
    return x
def sleigh():
    d=0.12; n=rng.standard_normal(int(d*sr)); n=np.diff(np.diff(n,prepend=0),prepend=0)
    tt=np.arange(len(n))/sr
    return (n*0.3+sum(np.sin(2*np.pi*f*tt) for f in (5200,6800,8100))*0.4)*np.exp(-tt*35)
SL=sleigh()
for k in range(int(DUR/0.25)):
    tt=k*0.25
    if 0.5<=tt<6.6 or 33.0<=tt<44.5: add(sfx,tt,SL,0.05 if k%2 else 0.08)
mel=[(76,0,.5),(76,.5,.5),(76,1,1),(76,2,.5),(76,2.5,.5),(76,3,1),(76,4,.5),(79,4.5,.5),(72,5,.75),(74,5.75,.25),(76,6,2)]
for (m,o,d) in mel:
    add(music,36.0+o,bell(hz(m),d+0.8),0.10)
    add(music,36.0+o,bell(hz(m+12),d+0.5),0.03)
# final chord ring
for m in [57,64,69,72,76]:
    add(music,44.5,tone(hz(m),2.5,harm=5,decay=1.6,det=0.003)*np.exp(-np.arange(int(2.5*sr))/sr*1.3),0.06)
# ducking
env=np.abs(V); k=int(0.15*sr); env=np.convolve(env,np.ones(k)/k,mode="same"); env=np.minimum(env/ (env.max()*0.35),1)
duck=1-0.55*env
mix=V + (music*0.9+drums*0.8)*duck + sfx*(1-0.3*env)
mix*=np.clip(np.minimum(t/0.3,(DUR-t)/1.2),0,1)
mix=np.tanh(mix*1.15)*0.93
np.save(out_dir+"/mix.npy",mix.astype(np.float32))
stereo=np.stack([mix,mix],1).astype(np.float32)
subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar",str(sr),"-ac","2","-i","-","-c:a","pcm_s16le",out_dir+"/mix.wav"],input=stereo.tobytes())
print("peak",np.abs(mix).max())
