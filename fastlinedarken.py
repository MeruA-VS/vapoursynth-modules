# FastLineDarken.py v0.1 (2012-11-20)
# requirements: RemoveGrain.dll(avs), mt_masktools-25.dll(avs)

import vapoursynth as vs


class InvalidArgument(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def clamp(minimum, x, maximum):
    return int(max(minimum, min(round(x), maximum)))

class FastLineDarken(object):
	def __init__(self, core):
		self.rgrain    = core.avs.RemoveGrain
		self.expand    = core.avs.mt_expand
		self.inpand    = core.avs.mt_inpand
		self.std       = core.std
		self.lut_range = None
		self.max       = 0
		self.mid       = 0
	
	def mt_lut(self, c1, expr, planes=0):
		lut = [clamp(0, expr(x), self.max) for x in self.lut_range]
		return self.std.Lut(c1, lut, planes)
	
	def mt_lutxy(self, c1, c2, expr, planes=0):
		lut = []
		for y in self.lut_range:
			for x in self.lut_range:
				lut.append(clamp(0, expr(x, y), self.max))
		return self.std.Lut2([c1, c2], lut, planes)
	
	def mt_lutxy2(self, c1, c2, luma_cap, threshold, planes=0):
		lut = []
		for y in self.lut_range:
			for x in self.lut_range:
				if y < luma_cap:
					res = y
				else:
					res = luma_cap
				if res > (x + threshold):
					if y < luma_cap:
						res = x - y
					else:
						res = x - luma_cap
				else:
					res = 0
				lut.append(clamp(0, res + 127, self.max))
		return self.std.Lut2([c1, c2], lut, planes)
	
	def mt_lutxy3(self, c1, c2, luma_cap, threshold, strf, planes=0):
		lut = []
		for y in self.lut_range:
			for x in self.lut_range:
				if y < luma_cap:
					res = y
				else:
					res = luma_cap
				if res > (x + threshold):
					if y < luma_cap:
						res = x - y
					else:
						res = x - luma_cap
				else:
					res = 0
				lut.append(clamp(0, ((res * strf) + x), self.max))
		return self.std.Lut2([c1, c2], lut, planes)
	
	def fastLinedarken(self, src, strength=42, luma_cap=191, threshold=4, thinning=0):
		strf = float(strength)/128.0
		thn  = float(thinning)/16.0
		
		self.max       = 2 ** src.format.bits_per_sample - 1
		self.mid       = self.max // 2 + 1
		self.lut_range = range(self.max + 1)
		
		exin     = self.inpand(self.expand(src))
		diff     = self.mt_lutxy2(src, exin, luma_cap, threshold)
		linemask = self.rgrain(self.mt_lut(self.inpand(diff), lambda x: ((x - 127) * thn) + 255), 20, -1)
		thick    = self.mt_lutxy3(src, exin, luma_cap, threshold, strf)
		
		if thinning > 0:
			expr = lambda x, y: (x + ((y - (self.mid - 1)) * (strf + 1)))
			expa = self.expand(src, chroma='copy')
			return self.mt_lutxy(expa, diff, expr)
		else:
			return thick
	
	def usage(self):
		usage = '''
		Line darkening script for vapoursynth ported from avisynth.

		fastLinedarken(clip, strength=42, luma_cap=191, threshold=4, thinning=0)

		Parameters are:
		strength (integer)  - Line darkening amount, 0-256. Default 48. Represents the _maximum_ amount
				that the luma will be reduced by, weaker lines will be reduced by
				proportionately less.
		luma_cap (integer)  - value from 0 (black) to 255 (white), used to stop the darkening
				determination from being 'blinded' by bright pixels, and to stop grey
				lines on white backgrounds being darkened. Any pixels brighter than
				luma_cap are treated as only being as bright as luma_cap. Lowering
				luma_cap tends to reduce line darkening. 255 disables capping. Default 191.
		threshold (integer) - any pixels that were going to be darkened by an amount less than
				threshold will not be touched. setting this to 0 will disable it, setting
				it to 4 (default) is recommended, since often a lot of random pixels are
				marked for very slight darkening and a threshold of about 4 should fix
				them. Note if you set threshold too high, some lines will not be darkened
		thinning (integer)  - optional line thinning amount, 0-256. Setting this to 0 will disable it,
				which is gives a _big_ speed increase. Note that thinning the lines will
				inherently darken the remaining pixels in each line a little. Default 24.
		'''
		return usage
