import zipfile, os
base = 'C:/Users/sxeyc/Downloads/수업'
out = 'C:/Users/sxeyc/KSTjiwoo/sugang-md.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith('.md'):
                zf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), base))
print('done', out)
