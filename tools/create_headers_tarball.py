#!/usr/bin/env python3

import argparse
import lzma
import os
import shutil
import sys
import subprocess
import tarfile
import tempfile

def strip_tarball_suffix(filename):
  suffixs = ['-headers.tar.gz', '-headers.tar.xz']
  for suffix in suffixs:
    if filename.endswith(suffix):
      return filename[:-len(suffix)]
  raise ValueError('The tarball name must ends with -headers.tar.gz/xz.')

def run_install_py(flags, temp_dir):
  install_py = os.path.join(os.path.dirname(__file__), 'install.py')
  subprocess.check_call([
      sys.executable,
      install_py,
      'install',
      '--silent',
      '--headers-only',
      '--dest-dir', temp_dir,
      '--prefix', '/',
  ] + flags)

def create_tarball(temp_dir, tarball, compression_level):
  if tarball.endswith('.gz'):
    tar = tarfile.open(tarball, 'w:gz', compresslevel=int(compression_level))
  elif tarball.endswith('.xz'):
    if compression_level.endswith('e'):
      preset = int(compression_level[:-1]) | lzma.PRESET_EXTREME
    else:
      preset = int(compression_level)
    tar = tarfile.open(tarball, 'w:xz', preset=preset)
  else:
    raise ValueError('Invalid tarball extension. Only .tar.gz and .tar.xz are supported.')
  with tar:
    tar.add(temp_dir, arcname=os.path.basename(temp_dir))

def main():
  parser = argparse.ArgumentParser(
      description='Install headers and create tarball')
  parser.add_argument('--target',
                      required=True,
                      help='Target path of the generated tarball')
  parser.add_argument('--compression-level',
                      default='9',
                      help='Compression level for gzip or xz (default: 9)')
  args, unknown_args = parser.parse_known_args()

  temp_dir = tempfile.mkdtemp()
  try:
    workspace = os.path.join(temp_dir, strip_tarball_suffix(args.target))
    run_install_py(unknown_args, workspace)
    create_tarball(workspace, args.target, args.compression_level)
  finally:
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
  main()
