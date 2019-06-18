import subprocess
import re
import os
import sys

# 檢查 Python 程式碼規範, 但容許 TODO 標記
print('Lint *.py files.')
cmd = 'pylint -f colorized -d fixme busm'
if os.system(cmd) != 0:
    exit(1)

# 檢查 reStructureText 語法, 避免上傳後被打槍
print('Check README.rst.')
cmd = ['rstcheck', 'README.rst']
complete = subprocess.run(cmd, stdout=subprocess.PIPE)
if complete.returncode != 0:
    exit(1)

exit(0)

# 打包
print('Build wheel.')
cmd = 'python setup.py bdist_wheel --plat-name win_amd64'
complete = subprocess.run(cmd, stdout=subprocess.PIPE)
if complete.returncode != 0:
    exit(1)

wheel = ''
out_lines = complete.stdout.decode('cp950').split('\r\n')
for line in out_lines:
    m = re.search(r'dist\\skcom-.+-win_amd64.whl', line)
    if m is not None:
        (off_beg, off_end) = m.span(0)
        wheel = line[off_beg:off_end]
        break

if wheel == '':
    exit(1)

# 上傳
if len(sys.argv) > 1 and sys.argv[1]:
    mode = 'production'
    cmd = 'twine upload --verbose ' + wheel
else:
    mode = 'testing'
    cmd = 'twine upload --repository testpypi --verbose ' + wheel

print('Upload wheel file: %s (%s mode).' % (wheel, mode))
if os.system(cmd) != 0:
    exit(1)
