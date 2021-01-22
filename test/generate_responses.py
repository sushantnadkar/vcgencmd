#!/usr/bin/env python3
""" Capture responses from real vcgencmd for unit testing

Run this script as root to create a new `captured_responses.json` file that can
be added to the unit test suite.
"""

import subprocess
import json

commands = [
    "vcos version",
    "vcos log status",
    "version",
    "get_camera",
    "get_throttled",
    "measure_temp",
    "measure_clock arm",
    "measure_clock core",
    "measure_clock h264",
    "measure_clock H264",
    "measure_clock isp",
    "measure_clock v3d",
    "measure_clock uart",
    "measure_clock pwm",
    "measure_clock emmc",
    "measure_clock pixel",
    "measure_clock vec",
    "measure_clock hdmi",
    "measure_clock dpi",
    "measure_volts core",
    "measure_volts sdram_c",
    "measure_volts sdram_i",
    "measure_volts sdram_p",
    "otp_dump",
    "get_mem arm",
    "get_mem gpu",
    "codec_enabled agif",
    "codec_enabled flac",
    "codec_enabled h263",
    "codec_enabled h264",
    "codec_enabled mjpa",
    "codec_enabled mjpb",
    "codec_enabled mjpg",
    "codec_enabled mpg2",
    "codec_enabled mpg4",
    "codec_enabled mvc0",
    "codec_enabled pcm",
    "codec_enabled thra",
    "codec_enabled vorb",
    "codec_enabled vp6",
    "codec_enabled vp8",
    "codec_enabled wmv9",
    "codec_enabled wvc1",
    "get_config int",
    "get_config str",
    "get_config arm_freq",
    "get_lcd_info",
    "mem_oom",
    "mem_reloc_stats",
    "read_ring_osc",
    "hdmi_timings",
    "dispmanx_list",
    "display_power -1 0",
    "display_power -1 1",
    "display_power -1 2",
    "display_power -1 3",
    "display_power -1 7",
    "display_power 0 0",
    "display_power 1 0",
]

responses = {}

for command in commands:
    p = subprocess.Popen("vcgencmd " + command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()

    responses[command] = {"stdout": stdout.decode(), "stderr": stderr.decode()}

with open("captured_responses.json", "w") as response_file:
    json.dump(responses, response_file, indent=2)