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
        if args[0] != "vcgencmd":
            raise Exception("Arguments need to start with vcgencmd")
        args = args[1:]

        cmd = " ".join(args)
        if not cmd in self.cmd_responses:
            raise Exception('Missing `' + cmd + '` from prepared responses')

        return self.cmd_responses[cmd]["stdout"].encode()

    def call_arguments(self, args):
        args = ["vcgencmd"] + args
        self.mock_co.assert_called_once_with(args, stderr=-1)

    def test_vcos_version(self):
        expected = "Nov 30 2020 22:13:46\n"
        expected += "Copyright (c) 2011 Broadcom\n"
        expected += "version ab1181cc0cb6df52bfae3b1d3fef0ce7c325166c (clean)\n"
        expected += "host buildbot\n"
        self.assertEqual(expected, self.obj.vcos_version())
        self.call_arguments(['vcos', 'version'])

    def test_vcos_log_status(self):
        expected = {
            "mmal": "error",
            "gencmd_file": "info",
            "wdog": "warn",
            "mmal-opaque": "error",
            "mmalsrv": "error",
            "gpus": "warn",
            "vchiq_test": "info",
            "audioserv": "warn",
            "smct": "error",
            "smservice": "error",
            "vchiq_vc": "error",
            "vchiq_sync": "warn",
            "vchiq_srvtrace": "trace",
            "vchiq_core_msg": "warn",
            "vchiq_core": "warn",
            "pixelvalve": "warn",
            "vec": "trace",
            "arm_loader": "info",
            "dispmanx": "warn",
            "hdmi": "warn",
            "hvs": "warn",
            "scalerlib": "warn",
            "cam_alloc": "warn",
            "plat_conf": "warn",
            "confzilla_fe_fdt": "warn",
            "confzilla_be": "warn",
            "gpioman": "warn",
            "board": "warn",
            "brfs": "info",
            "vcos_cmd": "info",
            "default": "error",
            "vc_suspend": "warn",
            "clock": "warn",
            "camsubs": "warn",
            "arasan": "info"
        }
        self.assertDictEqual(expected, self.obj.vcos_log_status())
        self.call_arguments(['vcos', 'log', 'status'])

    def test_version(self):
        expected = "Nov 30 2020 22:13:46 \n"
        expected += "Copyright (c) 2012 Broadcom\n"
        expected += "version ab1181cc0cb6df52bfae3b1d3fef0ce7c325166c "
        expected += "(clean) (release) (start)\n"
        self.assertEqual(expected, self.obj.version())
        self.call_arguments(['version'])

    def test_get_camera(self):
        expected = {
            "supported": "0",
            "detected": "0"
        }
        self.assertDictEqual(expected, self.obj.get_camera())
        self.call_arguments(['get_camera'])

    def test_get_throttled(self):
        expected = {
            'raw_data': '0x50000',
            'binary': '01010000000000000000',
            'breakdown':{
                '0': False,
                '1': False,
                '2': False,
                '3': False,
                '16': True,
                '17': False,
                '18': True,
                '19': False
            }
        }
        self.assertDictEqual(expected, self.obj.get_throttled())
        self.call_arguments(['get_throttled'])

    def test_get_throttled_flags(self):
        expected = {
            "Under-voltage detected": False,
            "Arm frequency capped": False,
            "Currently throttled": False,
            "Soft temperature limit active": False,
            "Under-voltage has occurred": True,
            "Arm frequency capping has occurred": False,
            "Throttling has occurred": True,
            "Soft temperature limit has occurred": False
        }
        self.assertDictEqual(expected, self.obj.get_throttled_flags())
        self.call_arguments(['get_throttled'])

    def test_measure_temp(self):
        expected = 47.2
        self.assertAlmostEqual(expected, self.obj.measure_temp())
        self.call_arguments(['measure_temp'])

    def test_measure_clock(self):
        expected_values = {
            "arm": 1200000000,
            "core": 400000000,
            "h264": 0,
            "isp": 0,
            "v3d": 300000000,
            "uart": 48000000,
            "pwm": 0,
            "emmc": 200000000,
            "pixel": 0,
            "vec": 108000000,
            "hdmi": 0,
            "dpi": 0
        }
        for clock, expected in expected_values.items():
            self.assertEqual(expected, self.obj.measure_clock(clock))
            self.call_arguments(['measure_clock', clock])
            self.mock_co.reset_mock()

    def test_measure_volts(self):
        expected_values = {
            "core": 1.3125,
            "sdram_c": 1.2000,
            "sdram_i": 1.2000,
            "sdram_p": 1.2250
        }
        for volts, expected in expected_values.items():
            self.assertAlmostEqual(expected, self.obj.measure_volts(volts))
            self.call_arguments(['measure_volts', volts])
            self.mock_co.reset_mock()

    def test_otp_dump(self):
        expected = {
            "08": "00000000",
            "09": "00000000",
            "10": "00000000",
            "11": "00000000",
            "12": "00000000",
            "13": "00000000",
            "14": "00000000",
            "15": "00000000",
            "16": "00280000",
            "17": "1020000a",
            "18": "1020000a",
            "19": "ffffffff",
            "20": "ffffffff",
            "21": "ffffffff",
            "22": "ffffffff",
            "23": "ffffffff",
            "24": "ffffffff",
            "25": "ffffffff",
            "26": "ffffffff",
            "27": "00002727",
            "28": "53bfb541",
            "29": "ac404abe",
            "30": "00a02082",
            "31": "00000000",
            "32": "00000000",
            "33": "00000000",
            "34": "00000000",
            "35": "00000000",
            "36": "00000000",
            "37": "00000000",
            "38": "00000000",
            "39": "00000000",
            "40": "00000000",
            "41": "00000000",
            "42": "00000000",
            "43": "00000000",
            "44": "00000000",
            "45": "00000000",
            "46": "00000000",
            "47": "00000000",
            "48": "00000000",
            "49": "00000000",
            "50": "00000000",
            "51": "00000000",
            "52": "00000000",
            "53": "00000000",
            "54": "00000000",
            "55": "00000000",
            "56": "00000000",
            "57": "00000000",
            "58": "00000000",
            "59": "00000000",
            "60": "00000000",
            "61": "00000000",
            "62": "00000000",
            "63": "00000000",
            "64": "00000000",
            "65": "00000000",
            "66": "00000000"
        }
        self.assertDictEqual(expected, self.obj.otp_dump())
        self.call_arguments(['otp_dump'])

    def test_get_mem(self):
        expected_values = {
            "arm": 948,
            "gpu": 76
        }
        for loc, expected in expected_values.items():
            self.assertEqual(expected, self.obj.get_mem(loc))
            self.call_arguments(['get_mem', loc])
            self.mock_co.reset_mock()

    def test_codec_enabled(self):
        expected_values = {
            "agif": False,
            "flac": False,
            "h263": False,
            "h264": False,
            "mjpa": False,
            "mjpb": False,
            "mjpg": False,
            "mpg2": False,
            "mpg4": False,
            "mvc0": False,
            "pcm": False,
            "thra": False,
            "vorb": False,
            "vp6": False,
            "vp8": False,
            "wmv9": False,
            "wvc1": False
        }
        for codec, expected in expected_values.items():
            self.assertEqual(expected, self.obj.codec_enabled(codec))
            self.call_arguments(['codec_enabled', codec])
            self.mock_co.reset_mock()

    def test_get_config_int(self):
        expected = {
            "aphy_params_current": "819",
            "arm_freq": "1200",
            "arm_freq_min": "600",
            "audio_pwm_mode": "514",
            "config_hdmi_boost": "5",
            "core_freq": "400",
            "desired_osc_freq": "0x387520",
            "disable_commandline_tags": "2",
            "disable_l2cache": "1",
            "display_hdmi_rotate": "-1",
            "display_lcd_rotate": "-1",
            "dphy_params_current": "547",
            "enable_tvout": "1",
            "force_eeprom_read": "1",
            "force_pwm_open": "1",
            "framebuffer_ignore_alpha": "1",
            "framebuffer_swap": "1",
            "gpu_freq": "300",
            "init_uart_clock": "0x2dc6c00",
            "lcd_framerate": "60",
            "over_voltage_avs": "0x1b774",
            "pause_burst_frames": "1",
            "program_serial_random": "1",
            "sdram_freq": "450",
            "total_mem": "1024",
            "hdmi_force_cec_address:0": "65535",
            "hdmi_force_cec_address:1": "65535",
            "hdmi_pixel_freq_limit:0": "0x9a7ec80"
        }
        self.assertDictEqual(expected, self.obj.get_config("int"))
        self.call_arguments(['get_config', 'int'])

    def test_get_config_str(self):
        expected = {
            "device_tree": "-",
            "overlay_prefix": "overlays/",
            "hdmi_cvt:0": "",
            "hdmi_cvt:1": "",
            "hdmi_edid_filename:0": "",
            "hdmi_edid_filename:1": "",
            "hdmi_timings:0": "",
            "hdmi_timings:1": ""
        }
        self.assertDictEqual(expected, self.obj.get_config("str"))
        self.call_arguments(['get_config', 'str'])

    def test_get_config_value(self):
        expected = {"arm_freq": "1200"}
        self.assertEqual(expected, self.obj.get_config("arm_freq"))
        self.call_arguments(['get_config', 'arm_freq'])

    def test_get_lcd_info(self):
        # TODO: Fails with output from some instances of vcgencmd
        expected = {"height": "720", "width": "480", "depth": "24"}
        #self.assertEqual(expected, self.obj.get_lcd_info())

    @mock.patch("subprocess.check_output")
    def test_get_lcd_info_old(self, mock_co_replaced):
        mock_co_replaced.return_value = b"0 0 0 no display\n"
        expected = {"height": "0", "width": "0", "depth": "0"}
        self.assertDictEqual(expected, self.obj.get_lcd_info())
        mock_co_replaced.assert_called_once_with(
            ['vcgencmd', 'get_lcd_info'], stderr=-1)

    def test_mem_oom(self):
        expected = {
            "oom events": "0",
            "lifetime oom required": "0 Mbytes",
            "total time in oom handler": "0 ms",
            "max time spent in oom handler": "0 ms"
        }
        self.assertDictEqual(expected, self.obj.mem_oom())
        self.call_arguments(['mem_oom'])

    def test_mem_reloc_stats(self):
        expected = {
            "alloc failures": "0",
            "compactions": "0",
            "legacy block fails": "0"
        }
        self.assertDictEqual(expected, self.obj.mem_reloc_stats())
        self.call_arguments(['mem_reloc_stats'])

    def test_read_ring_osc(self):
        expected = {
            'freq_mhz': '3.510',
            'volts_v': '1.3125',
            'temp_c': '47.2'
        }
        self.assertDictEqual(expected, self.obj.read_ring_osc())
        self.call_arguments(['read_ring_osc'])

    def test_hdmi_timings(self):
        expected = {
            "raw_data": "0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0",
            "breakdown": {
                "h_active_pixels": "0",
                "h_sync_polarity": "1",
                "h_front_porch": "0",
                "h_sync_pulse": "0",
                "h_back_porch": "0",
                "v_active_lines": "0",
                "v_sync_polarity": "1",
                "v_front_porch": "0",
                "v_sync_pulse": "0",
                "v_back_porch": "0",
                "v_sync_offset_a": "0",
                "v_sync_offset_b": "0",
                "pixel_rep": "0",
                "frame_rate": "0",
                "interlaced": "0",
                "pixel_freq": "0",
                "aspect_ratio": "0"
            }
        }
        self.assertDictEqual(expected, self.obj.hdmi_timings())
        self.call_arguments(['hdmi_timings'])

    def test_dispmanx_list(self):
        #TODO: Doesn't correctly handle empty output, which is possible
        expected = {}
        #self.assertDictEqual(expected, self.obj.dispmanx_list())

    def test_dispmanx_list_values(self):
        #TODO: Need example data for this added
        pass

    def test_display_power_state(self):
        expected_values = {
            0: "off",
            1: "off",
            2: "off",
            3: "on",
            7: "off"
        }
        for disp, expected in expected_values.items():
            self.assertEqual(expected, self.obj.display_power_state(disp))
            self.call_arguments(["display_power", "-1", str(disp)])
            self.mock_co.reset_mock()

    
    def test_display_power_on(self):
        self.obj.display_power_on(0)
        self.call_arguments(["display_power", "1", "0"])

    def test_display_power_off(self):
        self.obj.display_power_off(0)
        self.call_arguments(["display_power", "0", "0"])