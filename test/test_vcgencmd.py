import sys
import subprocess
import os
import json
import unittest

try:
    import unittest.mock as mock
except ImportError:
    # Python 2 needs the 'mock' module installed
    import mock

with mock.patch('subprocess.check_output') as skip_checking_binary:
    import vcgencmd


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.patched_co = mock.patch('subprocess.check_output')
        self.mock_co = self.patched_co.start()
        self.mock_co.side_effect = self.fake_check_output

        self.cmd_responses = {}
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'captured_responses.json')
        with open(f, "r") as resps:
            self.cmd_responses = json.load(resps)

        self.obj = vcgencmd.Vcgencmd()

    def tearDown(self):
        self.patched_co.stop()

    def fake_check_output(self, args, stderr=None):
        if not args[0] is "vcgencmd":
            raise Exception("Arguments need to start with vcgencmd")
        args = args[1:]

        cmd = " ".join(args)
        if not cmd in self.cmd_responses:
            raise Exception(f'Missing `{cmd}` from prepared responses')

        return self.cmd_responses[cmd]["stdout"].encode()

    def test_version(self):
        expected = "Nov 30 2020 22:13:46 \nCopyright (c) 2012 Broadcom\nversion ab1181cc0cb6df52bfae3b1d3fef0ce7c325166c (clean) (release) (start)\n"
        self.assertEqual(expected, self.obj.version())