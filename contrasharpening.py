# contrasharpening.py (2012-12-01)
# Dependencies: RemoveGrain.dll (avs)
#		Repair.dll (avs)

import vapoursynth as vs

def clamp(minimum, x, maximum):
	return int(max(minimum, min(round(x), maximum)))

class ContraSharpening(object):
	def __init__(self, core):
		self.std       = core.std
		self.repair    = core.avs.Repair
		self.rgrain    = core.avs.RemoveGrain
		self.lut_range = None
		self.max       = 0
		self.mid       = 0
	
	def mt_lutxy(self, c1, c2, expr, planes=0):
		lut = []
		for y in self.lut_range:
			for x in self.lut_range:
				lut.append(clamp(0, expr(x, y), self.max))
		return self.std.Lut2([c1, c2], lut, planes)
	
	def mt_adddiff(self, c1, c2, planes=0):
		expr = lambda x, y: x + y - self.mid
		return self.mt_lutxy(c1, c2, expr, planes)
	
	def mt_makediff(self, c1, c2, planes=0):
		expr = lambda x, y: x - y + self.mid
		return self.mt_lutxy(c1, c2, expr, planes)
	
	def minblur(self, clip):
		self.max       = 2 ** clip.format.bits_per_sample - 1
		self.mid       = self.max // 2 + 1
		self.lut_range = range(self.max + 1)
		
		rg11D = self.mt_makediff(clip, self.rgrain(clip, 11, -1))
		rg4D  = self.mt_makediff(clip, self.rgrain(clip, 4, -1))
		expr  = lambda x, y: self.mid if ((x - self.mid) * (y - self.mid)) < 0 else (x if abs(x - self.mid) < abs(y - self.mid) else y)
		DD    = self.mt_lutxy(rg11D, rg4D, expr)
		
		return self.mt_makediff(clip, DD)
		
	def contrasharpening(self, filtered, original):
		self.max       = 2 ** filtered.format.bits_per_sample - 1
		self.mid       = self.max // 2 + 1
		self.lut_range = range(self.max + 1)
		
		s    = self.minblur(filtered)
		allD = self.mt_makediff(original, filtered)
		ssD  = self.mt_makediff(s, self.rgrain(s, 11, -1))
		ssDD = self.repair(ssD, allD, 1)
		ssDD = self.mt_lutxy(ssDD, ssD, lambda x, y: x if abs(x - self.mid) < abs(y - self.mid) else y)
		
		return self.mt_adddiff(filtered, ssDD)
