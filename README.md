# Python binding for RaspberryPi vcgencmd command-line tool

## Summary

'vcgencmd' is a command line utility that can get various pieces of information from the VideoCore GPU on the Raspberry Pi. This Python package is a binding to that tool.

## Install

`vcgencmd` is compatible with both Python2.7+ and Python3.x. These instructions will be for Python 3.x. You can substitute the python and pip commands accordingly for other versions. The installer requires the `setuptools` package.

(Note: DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020.)

### Requirements
Pip (Python 3 version):
```bash
sudo apt-get install python3-pip
```
Setuptools (Python 3 version):
```bash
sudo pip3 install setuptools
```

### Python package manager (PIP)
Install globally:
```bash
sudo pip3 install vcgencmd
```
Install locally:
```bash
pip3 install --user vcgencmd
```

### Source installation
Install globally:
```bash
sudo pip3 install -e .
```
Install locally:
```bash
pip3 install -e . --user
```

## Uninstall
```bash
sudo pip3 uninstall vcgencmd
```

## Usage

```
from vcgencmd import Vcgencmd

vcgm = Vcgencmd()
output = vcgm.version()
print(output)

```

## Commands

#### get_sources(src)

Returns list of all possible sources/arguments,  required for some of the methods listed below.

Example: `get_sources("mem")` will return `["arm", "gpu"]` which are the sources/arguments for `get_mem(source)` that returns the memory of the source passed as argument to it.

#### vcos_version()

Returns a string with build date and version of the firmware on the VideoCore.

#### vcos_log_status()

Returns the error log status of the various VideoCore software areas in JSON format.

#### version()

Returns the string containing build date and version of the firmware on the VideoCore.

#### get_camera()

Returns the enabled and detected state of the official camera in JSON format. 1 means yes, 0 means no. Whilst all firmware (except cutdown versions) will support the camera, this support needs to be enabled by using [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md).

#### get_throttled()

Returns the throttled state of the system in dictionaries (similar to JSON format). This is a bit pattern - a bit being set indicates the following meanings:

| Bit | Meaning |
|:---:|---------|
| 0   | Under-voltage detected |
| 1   | Arm frequency capped |
| 2   | Currently throttled |
| 3   | Soft temperature limit active |
| 16  | Under-voltage has occurred |
| 17  | Arm frequency capping has occurred |
| 18  | Throttling has occurred |
| 19  | Soft temperature limit has occurred |

A value of zero indicates that none of the above conditions is true.

To find if one of these bits has been set, convert the value returned to binary, then number each bit along the top. You can then see which bits are set. For example:

``0x50000 = 0101 0000 0000 0000 0000``

Adding the bit numbers along the top we get:

```text
19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
 0  1  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
```

From this we can see that bits 18 and 16 are set, indicating that the Pi has previously been throttled due to under-voltage, but is not currently throttled for any reason.

#### get_throttled_flags()

Returns a dictionary of the same results as `get_throttled()` but with the descriptive names as the keys.

```python
>>> pprint.pp(out.get_throttled_flags())
{'Under-voltage detected': False,
 'Arm frequency capped': False,
 'Currently throttled': False,
 'Soft temperature limit active': False,
 'Under-voltage has occurred': False,
 'Arm frequency capping has occurred': True,
 'Throttling has occurred': False,
 'Soft temperature limit has occurred': False}
```

#### measure_temp()

Returns the temperature of the SoC as measured by the on-board temperature sensor.

#### measure_clock(clock)

This returns the current frequency of the specified clock in Hertz. List of clock options can be retrieved by `get_sources("clock")`. The options are:

| clock | Description |
|:-----:|-------------|
| arm   | ARM cores |
| core  | VC4 scaler cores |
| H264  | H264 block |
| isp   | Image Signal Processor |
| v3d   | 3D block |
| uart  | UART |
| pwm   | PWM block (analogue audio output) |
| emmc  | SD card interface |
| pixel | Pixel valve |
| vec | Analogue video encoder |
| hdmi | HDMI |
| dpi | Display Peripheral Interface |

#### measure_volts(block)

Returns the current voltage used by the specific block in volts. List of voltage sources can be retrieved by `get_sources("volts")`. The options are:

| block | Description |
|:-----:|-------------|
| core | VC4 core voltage |
| sdram_c | |
| sdram_i | |
| sdram_p | |

#### otp_dump()

Returns the content of the One Time Programmable (OTP) memory, which is part of the SoC. These are 32 bit values, indexed from 8 to 64, in JSON format. See the [OTP bits page](https://www.raspberrypi.org/documentation/hardware/raspberrypi/otpbits.md) for more details.

#### get_mem(type)

Returns the amount of memory allocated to the ARM cores and the VC4, in Megabytes. List of memory type options can be retrieved by `get_sources("mem")`. The options are:

| type | Description |
|:-----:|-------------|
| arm | ARM core |
| gpu | VC4 |

**Note:** On a Raspberry Pi 4 with greater than 1GB of RAM, the `arm` option is inaccurate. This is because the GPU firmware which implements this command is only aware of the first gigabyte of RAM on the system, so the `arm` setting will always return 1GB minus the `gpu` memory value. To get an accurate report of the amount of ARM memory, use one of the standard Linux commands, such as `free` or `cat /proc/meminfo`

#### codec_enabled(type)

Returns whether the specified CODEC type is enabled, in boolean type. Possible options for type are AGIF, FLAC, H263, H264, MJPA, MJPB, MJPG, **MPG2**, MPG4, MVC0, PCM, THRA, VORB, VP6, VP8, **WMV9**, **WVC1**. This list can be retrieved by `get_sources("codec")`. Those highlighted currently require a paid for licence (see the [FAQ](https://www.raspberrypi.org/documentation/faqs/README.md#pi-video) for more info), except on the Pi4, where these hardware codecs are disabled in preference to software decoding, which requires no licence. Note that because the H265 HW block on the Raspberry Pi4 is not part of the Videocore GPU, its status is not accessed via this command.

#### get_config(type | name)

This returns a JSON object of all the configuration items of the specified type that have been set in `/boot/config.txt`, or a single configuration item. Possible values for type parameter are **int, str**, or simply use the name of the configuration item.

#### get_lcd_info()

Returns the resolution and colour depth of any attached display, in JSON format.

#### mem_oom()

Return JSON object containing statistics on any Out Of Memory events occuring in the VC4 memory space.

#### mem_reloc_stats()

Return JSON object containing statistics from the relocatable memory allocator on the VC4.

#### read_ring_osc()

Return JSON object containing the curent speed, voltage and temperature of the ring oscillator.

#### hdmi_timings()

Returns the current HDMI settings timings, in JSON format. See [Video Config](https://www.raspberrypi.org/documentation/configuration/config-txt/video.md) for details of the values returned.

#### dispmanx_list()

Returns a JSON object of all dispmanx items currently being displayed.

#### display_power_on(display)

Sets the display power state to *on* of the display whose ID is passed as the parameter.

#### display_power_off(display)

Sets the display power state to *off* of the display whose ID is passed as the parameter.

#### display_power_state(display)

Returns the display power state as *on* or *off* of the display whose ID is passed as the parameter.

The display ID for the preceding three methods are determined by the following table.

| Display | ID |
| --- | --- |
|Main LCD       | 0 |
|Secondary LCD  | 1 |
|HDMI 0         | 2 |
|Composite      | 3 |
|HDMI 1         | 7 |
