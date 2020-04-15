import subprocess
import shlex
import re

class Vcgencmd:
	sources = {
		"clock": ["arm", "core","H264", "isp", "v3d", "uart", "pwm", "emmc", "pixel", "vec", "hdmi", "dpi"],
		"volts": ["core", "sdram_c", "sdram_i", "sdram_p"],
		"mem": ["arm", "gpu"],
		"codec": ["agif", "flac", "h263", "h264", "mjpa", "mjpb", "mjpg", "mpg2", "mpg4", "mvc0", "pcm", "thra", "vorb", "vp6", "vp8", "wmv9", "wvc1"]

	}
	valid_args = {
		"state": [0, 1, -1],
		"display": [0, 1, 2, 3, 7]
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
		if typ not in self.sources.keys():
			raise Exception("Invalid source type.\n{0} must be one of {1}.format(typ, self.sources.keys)")
		return self.sources.get(typ)

	def vcos_version(self):
		out = self.self.__verify_command("vcos version", "", [""])
		return str(out)

	def vcos_log_status(self):
		out = self.__verify_command("vcos log status", "", [""])
		out = out.split("\n")
		out = list(filter(None, out))
		response = {}
		for i in out:
			j = i.split("-")
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

	def measure_temp(self):
		out = self.__verify_command("measure_temp", "", [""])
		return float(re.sub("[^\d\.]", "",out))

	def measure_clock(self, clock):
		out = self.__verify_command("measure_clock ", clock, self.sources.get("clock"))
		out = out.split("=")[1]
		return int(out)

	def measure_volts(self, block):
		out = self.__verify_command("measure_volts ", block, self.sources.get("volts"))
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
		out = self.__verify_command("get_mem ", typ, self.sources.get("mem"))
		return int(re.sub("[^\d]", "", out))

	def codec_enabled(self, typ):
		out = self.__verify_command("codec_enabled ", typ, self.sources.get("codec"))
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
		out = out.split(" ")
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
		if display not in [0, 1, 2, 3, 7]:
			raise Exception("{0} must be one of [0, 1, 2, 3, 7]")
		out = self.__run_command("display_power 1 " + str(display))

	def display_power_off(self, display):
		if display not in [0, 1, 2, 3, 7]:
			raise Exception("{0} must be one of [0, 1, 2, 3, 7]")
		out = self.__run_command("display_power 0 " + str(display))

	def display_power_state(self, display=0):
		if display not in [0, 1, 2, 3, 7]:
			raise Exception("{0} must be one of [0, 1, 2, 3, 7]")
		out = self.__run_command("display_power -1 " + str(display))
		if out.split("=")[1].strip() == "0":
			return "off"
		elif out.split("=")[1].strip() == "1":
			return "on"
