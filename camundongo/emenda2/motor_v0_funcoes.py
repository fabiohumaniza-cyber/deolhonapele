"""motor_v0_funcoes.py — extraido VERBATIM de v0_congelado_2026-09-22/rodar.py
SHA-256 do arquivo de origem: 78b193014577a45109771a2b15f3b7ff55663b0bb4312a23980c766fe7161732
Extracao mecanica por ast.get_source_segment; nenhuma linha reescrita.
Contem: L, clareia, verm, lstar, mapa_t, anel, dice, canais, grade.
"""
import numpy as np, itertools
from scipy import ndimage as ndi

L=700

def clareia(im,g):
    if g==1.0: return im
    return (255*np.power(im.astype(np.float64)/255.,g)).astype(np.uint8)

def verm(im): return im[:,:,0].astype(float)-(im[:,:,1].astype(float)+im[:,:,2].astype(float))/2

def lstar(im):
    q=im.astype(np.float64)/255.
    def lin(c): return np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    R,G,B=[lin(q[:,:,i]) for i in range(3)]
    Y=R*.2126+G*.7152+B*.0722
    f=np.where(Y>0.008856,np.cbrt(Y),7.787*Y+16/116)
    return (116*f-16)*2.55

def mapa_t(A,g,ds,al,sv=4,ar=None):
    if sv>0: A=ndi.uniform_filter(A,size=2*sv+1)
    h,w=A.shape; kk=int(min(w,h)*0.08)
    m=np.zeros(A.shape,bool); m[:kk,:]=m[-kk:,:]=True; m[:,:kk]=m[:,-kk:]=True
    if ar is not None: m&=~ar
    pele=np.median(A[m])
    liv=~ar if ar is not None else np.ones(A.shape,bool)
    e=np.percentile(np.abs(A-pele)[liv],98) or 1
    return np.clip((np.abs(A-pele)/e*(g/100)+(ds/100))/max(0.01,al/100),0,1)

def anel(t,lo,hi,fecha=3,ar=None,diam=20.0):
    am=(t>=lo)&(t<=hi)
    if ar is not None: am&=~ar
    if am.sum()<80: return None
    fe=ndi.binary_closing(am,np.ones((2*fecha+1,)*2,bool))
    lbl,_=ndi.label(~fe)
    bb=set(lbl[0,:])|set(lbl[-1,:])|set(lbl[:,0])|set(lbl[:,-1]); bb.discard(0)
    fora=np.zeros(fe.shape,bool)
    for b in bb: fora|=(lbl==b)
    dentro=(~fe)&(~fora)
    if dentro.sum()<80: return None
    lb,nc=ndi.label(fe,structure=np.ones((3,3)))
    if nc==0: return None
    tam=ndi.sum(fe,lb,range(1,nc+1)); e=0
    for c in (np.argsort(-tam)+1)[:8]:
        mm=(lb==c)
        viz=ndi.binary_dilation(mm,np.ones((3,3),bool))&~mm
        if (viz&dentro).any() and (viz&fora).any(): e=c; break
    if not e: return None
    an=(lb==e)
    l2,_=ndi.label(~an)
    b2=set(l2[0,:])|set(l2[-1,:])|set(l2[:,0])|set(l2[:,-1]); b2.discard(0)
    f2=np.zeros(an.shape,bool)
    for b in b2: f2|=(l2==b)
    m=~f2; n=m.sum()
    if n<200 or n>0.6*t.size: return None
    per=(m&~ndi.binary_erosion(m,np.ones((3,3),bool))).sum()
    uni=min(1,an.sum()/max(1,am.sum()))
    fino=min(1,per/max(1,an.sum()))
    comp=min(1,4*np.pi*n/max(1,per*per))
    resp=np.pi*(diam/2*30*L/1380)**2
    tam_ok=1-min(1,abs(n-resp)/resp)
    prim=(0.25*uni+0.15*fino+0.25*comp+0.20*tam_ok)/0.85
    sec =(0.25*uni+0.15*fino+0.25*comp)/0.65
    return m,prim,sec

def dice(x,y): return 2*(x&y).sum()/max(1,x.sum()+y.sum())

canais={'verm':verm,'lstar':lstar}

grade=list(itertools.product([1.0,0.70,0.55],['verm','lstar'],[80,130],[-35,0],[50,80],
        [(0.35,0.75),(0.45,0.85),(0.62,0.86)]))
