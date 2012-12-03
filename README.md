A collection of vapoursynth modules ported from various avisynth scripts.

Here comes a list with the dependencies for every module and an example on how to load them:

# supersampledantialiasing.py
import vapoursynth as vs
import sys
import supersampledantialiasing
core = vs.Core()
core.std.LoadPlugin(path=r'fmtconv.dll')
core.avs.LoadPlugin(path=r'mt_masktools-25.dll')
core.avs.LoadPlugin(path=r'SangNom.dll')
core.avs.LoadPlugin(path=r'RepairSSE2.dll')
core.avs.LoadPlugin(path=r'RemoveGrainSSE2.dll')
aa = supersampledantialiasing.SupersampledAntialiasing(core)
# stuff happens
clip = aa.ssaa(src)


# fastlinedarken.py
import vapoursynth as vs
import sys
import fastlinedarken
core = vs.Core()
core.avs.LoadPlugin(path=r'mt_masktools-25.dll')
core.avs.LoadPlugin(path=r'RemoveGrainSSE2.dll')
ld = fastlinedarken.FastLineDarken(core)
# stuff happens
clip = ld.fastlinedarken(src)


# edgecleaner.py
import vapoursynth as vs
import sys
import edgecleaner
core = vs.Core()
core.avs.LoadPlugin(path=r'avisynthfilters.dll')
core.avs.LoadPlugin(path=r'mt_masktools-25.dll')
core.avs.LoadPlugin(path=r'RepairSSE2.dll')
core.avs.LoadPlugin(path=r'RemoveGrainSSE2.dll')
core.avs.LoadPlugin(path=r'Deen.dll')
core.avs.LoadPlugin(path=r'aWarpSharp.dll')
ec = edgecleaner.EdgeCleaner(core)
# stuff happens
clip = ec.edgecleaner(src)


# dehalo_alpha.py
import vapoursynth as vs
import sys
import dehalo_alpha
core = vs.Core()
core.std.LoadPlugin(path=r'fmtconv.dll')
core.avs.LoadPlugin(path=r'mt_masktools-25.dll')
core.avs.LoadPlugin(path=r'RepairSSE2.dll')
core.avs.LoadPlugin(path=r'RemoveGrainSSE2.dll')
core.avs.LoadPlugin(path=r'RemoveGrainHD.dll')
dh = dehalo_alpha.DeHalo_alpha(core)
# stuff happens
clip = dh.dehalo_alpha(src)


# contrasharpening.py
import vapoursynth as vs
import sys
import contrasharpening
core = vs.Core()
core.avs.LoadPlugin(path=r'RepairSSE2.dll')
core.avs.LoadPlugin(path=r'RemoveGrainSSE2.dll')
cs = contrasharpening.ContraSharpening(core)
# stuff happens
clip = cs.contrasharpening(filtered_clip, unfiltered_clip)
