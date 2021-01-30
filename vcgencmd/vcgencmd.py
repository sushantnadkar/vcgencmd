import subprocess
import shlex
import re

class Vcgencmd:
	__sources = {
		"clock": ["arm", "core","h264", "isp", "v3d", "uart", "pwm", "emmc", "pixel", "vec", "hdmi", "dpi"],
		"volts": ["core", "sdram_c", "sdram_i", "sdram_p"],
		"mem": ["arm", "gpu"],
		"codec": ["agif", "flac", "h263", "h264", "mjpa", "mjpb", "mjpg", "mpg2", "mpg4", "mvc0", "pcm", "thra", "vorb", "vp6", "vp8", "wmv9", "wvc1"],
		"display_id": [0, 1, 2, 3, 7]
	}

	def __run_command(self, cmd):

		args = shlex.split(cmd)
		args.insert(0, "vcgencmd")
		out = subprocess.check_output(args, stderr=subprocess.PIPE).decode("utf-8")

		return out

	def __verify_command(self, cmd, source, source_list):
		cmd = cmd.lower()
		source = source.lower()
		if source not in source_list:
			raise Exception("{0} must be one of {1}".format(source, source_list))
		return self.__run_command(cmd + source)

	def get_sources(self, typ):
		if typ not in self.__sources.keys():
			raise Exception("Invalid source type.\n{0} must be one of {1}".format(typ, self.__sources.keys))
		return self.__sources.get(typ)

	def vcos_version(self):
		out = self.__verify_command("vcos version", "", [""])
		return str(out)

	def vcos_log_status(self):
		out = self.__verify_command("vcos log status", "", [""])
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split(" - ")
			response[j[0].strip()] = j[1].strip()
		return response


	def version(self):
		out = self.__verify_command("version", "", [""])
		return str(out)

	def get_camera(self):
		out = self.__verify_command("get_camera", "", [""])
		out = out.split(" ")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split("=")
			response[j[0].strip()] = j[1].strip()
		return response

	def get_throttled(self):
		out = self.__verify_command("get_throttled", "", [""])
		hex_val = out.split("=")[1].strip()
		binary_val = format(int(hex_val[2:], 16), "020b")
		state = lambda s: True if s == "1" else False
		response = {}
		response["raw_data"] = hex_val
		response["binary"] = binary_val
		response["breakdown"] = {}
		response["breakdown"]["0"] = state(binary_val[16:][3])
		response["breakdown"]["1"] = state(binary_val[16:][2])
		response["breakdown"]["2"] = state(binary_val[16:][1])
		response["breakdown"]["3"] = state(binary_val[16:][0])
		response["breakdown"]["16"] = state(binary_val[0:4][3])
		response["breakdown"]["17"] = state(binary_val[0:4][2])
		response["breakdown"]["18"] = state(binary_val[0:4][1])
		response["breakdown"]["19"] = state(binary_val[0:4][0])
		return response

	def get_throttled_flags(self):
		bits = self.get_throttled()['breakdown']

		mapping = {
			"0": "Under-voltage detected",
			"1": "Arm frequency capped",
			"2": "Currently throttled",
			"3": "Soft temperature limit active",
			"16": "Under-voltage has occurred",
			"17": "Arm frequency capping has occurred",
			"18": "Throttling has occurred",
			"19": "Soft temperature limit has occurred"
		}

		desc = {}
		for bit, value in bits.items():
			desc[mapping[bit]] = value
		
		return desc

	def measure_temp(self):
		out = self.__verify_command("measure_temp", "", [""])
		return float(re.sub("[^\d\.]", "",out))

	def measure_clock(self, clock):
		out = self.__verify_command("measure_clock ", clock, self.__sources.get("clock"))
		out = out.split("=")[1]
		return int(out)

	def measure_volts(self, block):
		out = self.__verify_command("measure_volts ", block, self.__sources.get("volts"))
		return float(re.sub("[^\d\.]", "", out))

	def otp_dump(self):
		out = self.__verify_command("otp_dump", "", [""])
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split(":")
			response[j[0].strip()] = j[1].strip()
		return response

	def get_mem(self, typ):
		out = self.__verify_command("get_mem ", typ, self.__sources.get("mem"))
		return int(re.sub("[^\d]", "", out))

	def codec_enabled(self, typ):
		out = self.__verify_command("codec_enabled ", typ, self.__sources.get("codec"))
		out = out.split("=")[1]
		if out.strip() == "disabled":
			return False
		if out.strip() == "enabled":
			return True

	def get_config(self, type_or_name):
		out = self.__run_command("get_config " + type_or_name)
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split("=")
			response[j[0].strip()] = j[1].strip()
		return response

	def get_lcd_info(self):
		out = self.__verify_command("get_lcd_info ", "", [""])
		out = out.split()
		response = {"height": out[0], "width": out[1], "depth": out[2]}
		return response

	def mem_oom(self):
		out = self.__verify_command("mem_oom ", "", [""])
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split(":")
			response[j[0].strip()] = j[1].strip()
		return response

	def mem_reloc_stats(self):
		out = self.__verify_command("mem_reloc_stats ", "", [""])
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split(":")
			response[j[0].strip()] = j[1].strip()
		return response

	def read_ring_osc(self):
		out = self.__verify_command("read_ring_osc ", "", [""])
		response = {}
		out = out.split("=")[1]
		out = out.split(" ")
		response["freq_mhz"] = re.sub("[^\d\.]", "", out[0])
		response["volts_v"] = re.sub("[^\d\.]", "", out[1])
		response["temp_c"] = re.sub("[^\d\.]", "", out[2])
		return response

	def hdmi_timings(self):
		out = self.__verify_command("hdmi_timings ", "", [""])
		out_bits = out.split("=")[1].strip()
		out_bits = out_bits.split(" ")
		response = {
			"raw_data": out.split("=")[1].strip(),
			"breakdown": {
				"h_active_pixels": out_bits[0],
				"h_sync_polarity": out_bits[1],
				"h_front_porch": out_bits[2],
				"h_sync_pulse": out_bits[3],
				"h_back_porch": out_bits[4],
				"v_active_lines": out_bits[5],
				"v_sync_polarity": out_bits[6],
				"v_front_porch": out_bits[7],
				"v_sync_pulse": out_bits[8],
				"v_back_porch": out_bits[9],
				"v_sync_offset_a": out_bits[10],
				"v_sync_offset_b": out_bits[11],
				"pixel_rep": out_bits[12],
				"frame_rate": out_bits[13],
				"interlaced": out_bits[14],
				"pixel_freq": out_bits[15],
				"aspect_ratio": out_bits[16]
			}
		}
		return response

	def dispmanx_list(self):
		out = self.__verify_command("dispmanx_list ", "", [""])
		out = out.strip()
		out = re.sub("(?<=\d)\s(?=\d)", " resolution:", out)
		out = out.split(" ")
		response = {}
		for i in out:
			j = i.split(":")
			response[j[0].strip()] = j[1].strip()
		return response

	def display_power_on(self, display):
		if display not in self.__sources["display_id"]:
			raise Exception("{0} must be one of {1}".format(diaplay, self.__sources["display_id"]))
		out = self.__run_command("display_power 1 " + str(display))

	def display_power_off(self, display):
		if display not in self.__sources["display_id"]:
			raise Exception("{0} must be one of {1}".format(diaplay, self.__sources["display_id"]))
		out = self.__run_command("display_power 0 " + str(display))

	def display_power_state(self, display=0):
		if display not in self.__sources["display_id"]:
			raise Exception("{0} must be one of {1}".format(diaplay, self.__sources["display_id"]))
		out = self.__run_command("display_power -1 " + str(display))
		if out.split("=")[1].strip() == "0":
			return "off"
		elif out.split("=")[1].strip() == "1":
			return "on"

def _print_dict(input_dict):
	mm_fmt = "{:35s} : {}"
	for key, val in input_dict.items():
		print(mm_fmt.format(key, val))

def print_overview():
	mm_fmt = "{:35s} : {}"

	stats = Vcgencmd()
	print("Binary Version")
	print(stats.version())

	print("\nClock Frequencies (Hz)")
	for clock in stats.get_sources("clock"):
		val = stats.measure_clock(clock)
		print(mm_fmt.format(clock, val))
		
	print("\nVoltages (V)")
	for volt in stats.get_sources("volts"):
		val = stats.measure_volts(volt)
		print(mm_fmt.format(volt, val))
		
	print("\nMemory (MB) (Not accurate on rpi4)")
	for mem in stats.get_sources("mem"):
		val = stats.get_mem(mem)
		print(mm_fmt.format(mem, val))

	print("\nTemperatures (C)")
	val = stats.measure_temp()
	print(mm_fmt.format("core", val))

	print("\nVideo Core Log Status")
	_print_dict(stats.vcos_log_status())

	print("\nCamera")
	status = stats.get_camera()
	print(mm_fmt.format("supported", status["supported"]))
	print(mm_fmt.format("detected", status["detected"]))

	print("\nThrottling")
	_print_dict(stats.get_throttled_flags())

	print("\nOne Time Programmable Memory")
	_print_dict(stats.otp_dump())

	print("\nCodecs Enabled")
	for codec in stats.get_sources("codec"):
		val = stats.codec_enabled(codec)
		print(mm_fmt.format(codec, val))

	print("\nBoot Config Values (config.txt effective values)")
	_print_dict(stats.get_config("str"))
	_print_dict(stats.get_config("int"))

	print("\nLCD (px)")
	_print_dict(stats.get_lcd_info())

	print("\nstats Of Memory Events")
	_print_dict(stats.mem_oom())

	print("\nRelocatable Memory")
	_print_dict(stats.mem_reloc_stats())

	print("\nRing Oscillator")
	_print_dict(stats.read_ring_osc())

	print("\nHDMI Timings")
	_print_dict(stats.hdmi_timings()["breakdown"])

	print("\nDisplay Status")
	for disp in stats.get_sources("display_id"):
		val = stats.display_power_state(disp)
		print(mm_fmt.format("display " + str(disp), val))
