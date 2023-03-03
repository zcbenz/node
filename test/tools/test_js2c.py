import unittest
import sys, os

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(rootdir, 'tools'))

from js2c import NormalizeFileName

class Js2ctest(unittest.TestCase):
    def testNormalizeFileName(self):
        self.assertEqual(NormalizeFileName(None, 'dir/mod.js'), 'mod')
        self.assertEqual(NormalizeFileName(None, 'deps/mod.js'), 'internal/deps/mod')
        self.assertEqual(NormalizeFileName(None, 'mod.js'), 'mod')

    def testNormalizeFileNameWithRoot(self):
        self.assertEqual(
            NormalizeFileName(rootdir, os.path.join(rootdir, 'dir/mod.js')),
            'mod')
        self.assertEqual(
            NormalizeFileName(rootdir, os.path.join(rootdir, 'deps/mod.js')),
            'internal/deps/mod')
        self.assertEqual(
            NormalizeFileName(rootdir, os.path.join(rootdir, 'mod.js')),
            'mod')

if __name__ == '__main__':
    unittest.main()
