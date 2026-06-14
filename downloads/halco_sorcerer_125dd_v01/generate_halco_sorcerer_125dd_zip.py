#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-contained generator for a printable Sorcerer-125-DD-style trolling lure ZIP.
This is NOT an official Halco model and does not contain logos/trademarks.
Run: python3 generate_halco_sorcerer_125dd_zip.py
Output: Halco_Sorcerer_125DD_Bambu_v01.zip
"""
import math, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

OUT=Path('build_halco_sorcerer_125dd')
ZIP_NAME='Halco_Sorcerer_125DD_Bambu_v01.zip'
L=125.0; MAX_W=15.0; MAX_H=19.0; NX=86; NA=22; NZ=10

def radii(x):
    t=max(0,min(1,x/L))
    base=(math.sin(math.pi*t)**0.48) if 0<t<1 else 0
    front=0.86+0.22*math.exp(-((t-0.36)/0.18)**2)
    tail=1.0-0.34*max(0,(t-0.72)/0.28)
    return max(.25,(MAX_W/2)*base*front*tail), max(.28,(MAX_H/2)*base*(.94+.12*math.exp(-((t-.42)/.22)**2)))

def stl(path,name,tris):
    with open(path,'w',encoding='utf-8',newline='\n') as f:
        f.write(f'solid {name}\n')
        for tri in tris:
            f.write('  facet normal 0 0 0\n    outer loop\n')
            for p in tri: f.write(f'      vertex {p[0]:.5f} {p[1]:.5f} {p[2]:.5f}\n')
            f.write('    endloop\n  endfacet\n')
        f.write(f'endsolid {name}\n')

def half(sign):
    v=[]
    for i in range(NX+1):
        x=L*i/NX; ry,rz=radii(x); row=[]
        for j in range(NA+1):
            ph=math.pi*j/NA; row.append((x,sign*ry*math.sin(ph),rz*math.cos(ph)))
        v.append(row)
    tris=[]
    for i in range(NX):
        for j in range(NA):
            a,b,c,d=v[i][j],v[i+1][j],v[i][j+1],v[i+1][j+1]
            tris += [(a,b,d),(a,d,c)] if sign>0 else [(a,d,b),(a,c,d)]
    p=[]
    for i in range(NX+1):
        x=L*i/NX; ry,rz=radii(x); p.append([(x,0,-rz+2*rz*k/NZ) for k in range(NZ+1)])
    for i in range(NX):
        for k in range(NZ):
            a,b,c,d=p[i][k],p[i+1][k],p[i][k+1],p[i+1][k+1]
            tris += [(a,d,b),(a,c,d)] if sign>0 else [(a,b,d),(a,d,c)]
    # small glue-face guide ribs; cut/drill the real through-wire slot manually
    for gz in (0,-3.2,3.2):
        x0,x1,h,w,y=12,119,.18,.52,sign*.08
        pts=[(x0,y,gz-w),(x1,y,gz-w),(x1,y,gz+w),(x0,y,gz+w),(x0,sign*h,gz-w),(x1,sign*h,gz-w),(x1,sign*h,gz+w),(x0,sign*h,gz+w)]
        for A,B,C in [(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(3,2,6),(3,6,7)]: tris.append((pts[A],pts[B],pts[C]))
    return tris

def lip():
    th=2.0; poly=[(0,-12.5),(7,-13),(28,-10.5),(49,-7),(54,0),(49,7),(28,10.5),(7,13),(0,12.5)]
    top=[(x,y,th/2) for x,y in poly]; bot=[(x,y,-th/2) for x,y in poly]; tris=[]
    for i in range(1,len(poly)-1): tris += [(top[0],top[i],top[i+1]),(bot[0],bot[i+1],bot[i])]
    for i in range(len(poly)):
        j=(i+1)%len(poly); tris += [(bot[i],bot[j],top[j]),(bot[i],top[j],top[i])]
    return tris

def move(tris,dx=0,dy=0,dz=0): return [tuple((p[0]+dx,p[1]+dy,p[2]+dz) for p in t) for t in tris]

def svg(path):
    poly=[(0,-12.5),(7,-13),(28,-10.5),(49,-7),(54,0),(49,7),(28,10.5),(7,13),(0,12.5)]
    pts=' '.join(f'{x+5:.2f},{y+18:.2f}' for x,y in poly)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="64mm" height="36mm" viewBox="0 0 64 36">\n<polygon points="{pts}" fill="none" stroke="black" stroke-width="0.35"/>\n<circle cx="41" cy="18" r="1.25" fill="none" stroke="black" stroke-width="0.25"/>\n<text x="3" y="34" font-size="2.5">Sorcerer 125 DD style lip, 2mm PC</text>\n</svg>\n',encoding='utf-8')

def readme(path):
    path.write_text('''# Sorcerer 125 DD style v0.1 — печать и доводка

Это не официальный Halco и не точная копия с логотипом. Это рабочий прототип “125 DD style” для личных испытаний.

Файлы: две половинки корпуса STL, шаблон DD-лопатки STL/SVG, 3MF для Bambu Studio, инструкция.

Печать Bambu Lab A1: PETG/ASA, слой 0.16–0.20 мм, стенки 5–6, заполнение 15–25% gyroid. Лопатку для реальной рыбалки лучше вырезать из поликарбоната 2 мм по SVG-шаблону.

Сборка: сквозная нержавеющая проволока 1.0–1.2 мм; петля лески в лопатке; нижние петли примерно 40–45 мм и 82–88 мм от носа; балласт 3–6 г снизу ближе к передней трети; склейка эпоксидкой; герметизация эпоксидкой/UV-смолой/яхтным лаком.

Правильная плавучесть: воблер плавает, не ложится на бок, нос чуть ниже хвоста, после погружения медленно всплывает.
''',encoding='utf-8')

def write3mf(path,tris):
    verts=[]; idx={}; faces=[]
    for tri in tris:
        face=[]
        for p in tri:
            k=(round(p[0],5),round(p[1],5),round(p[2],5))
            if k not in idx: idx[k]=len(verts); verts.append(k)
            face.append(idx[k])
        faces.append(tuple(face))
    vx='\n'.join(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x,y,z in verts)
    tr='\n'.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in faces)
    model=f'''<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><metadata name="Title">{escape('Sorcerer 125 DD style')}</metadata><resources><object id="1" type="model"><mesh><vertices>{vx}</vertices><triangles>{tr}</triangles></mesh></object></resources><build><item objectid="1"/></build></model>'''
    rels='<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
    types='<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',types); z.writestr('_rels/.rels',rels); z.writestr('3D/3dmodel.model',model)

def main():
    OUT.mkdir(exist_ok=True)
    left,right,lp=half(1),half(-1),lip()
    files=[OUT/'sorcerer125dd_style_Bambu_parts_v01.3mf',OUT/'sorcerer125dd_style_LEFT_half_v01.stl',OUT/'sorcerer125dd_style_RIGHT_half_v01.stl',OUT/'sorcerer125dd_style_DD_lip_2mm_template_v01.stl',OUT/'sorcerer125dd_style_DD_lip_cut_template_v01.svg',OUT/'README_RU_PRINT_AND_TUNE_v01.txt']
    write3mf(files[0], move(left,0,14,0)+move(right,0,-14,0)+move(lp,22,0,-18))
    stl(files[1],'sorcerer125dd_left_half',left); stl(files[2],'sorcerer125dd_right_half',right); stl(files[3],'sorcerer125dd_dd_lip_template',lp)
    svg(files[4]); readme(files[5])
    with zipfile.ZipFile(ZIP_NAME,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files: z.write(p,p.name)
    print('OK:',Path(ZIP_NAME).resolve())

if __name__=='__main__': main()
