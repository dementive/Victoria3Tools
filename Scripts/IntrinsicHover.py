import sublime
import sublime_plugin

import webbrowser


IntrinsicList = {
	"abort": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/abort",
		"Terminates the current draw or dispatch call being executed."),
	"abs": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-abs",
		"Absolute value (per component)."),
	"acos": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-acos",
		"Returns the arccosine of each component of x."),
	"all": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-all",
		"Test if all components of x are nonzero."),
	"AllMemoryBarrier": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/allmemorybarrier",
		"Blocks execution of all threads in a group until all memory accesses have been completed."),
	"AllMemoryBarrierWithGroupSync": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/allmemorybarrierwithgroupsync",
		"Blocks execution of all threads in a group until all memory accesses have been completed and all threads in the group have reached this call."),
	"any": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-any",
		"Test if any component of x is nonzero."),
	"asdouble": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/asdouble",
		"Reinterprets a cast value into a double."),
	"asfloat": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-asfloat",
		"Convert the input type to a float."),
	"asin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-asin",
		"Returns the arcsine of each component of x."),
	"asint": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-asint",
		"Convert the input type to an integer."),
	"asuint": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-asuint",
		"Convert the input type to an unsigned integer."),
	"atan": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-atan",
		"Returns the arctangent of x."),
	"atan2": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-atan2",
		"Returns the arctangent of of two values (x,y)."),
	"ceil": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-ceil",
		"Returns the smallest integer which is greater than or equal to x."),
	"CheckAccessFullyMapped": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/checkaccessfullymapped",
		"Determines whether all values from a Sample or Load operation accessed mapped tiles in a tiled resource."),
	"clamp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-clamp",
		"Clamps x to the range [min, max]."),
	"clip": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-clip",
		"Discards the current pixel, if any component of x is less than zero."),
	"cos": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-cos",
		"Returns the cosine of x."),
	"cosh": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-cosh",
		"Returns the hyperbolic cosine of x."),
	"countbits": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/countbits",
		"Counts the number of bits (per component) in the input integer."),
	"cross": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-cross",
		"Returns the cross product of two 3D vectors."),
	"D3DCOLORtoUBYTE4": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-d3dcolortoubyte4",
		"Swizzles and scales components of the 4D vector x to compensate for the lack of UBYTE4 support in some hardware."),
	"ddx": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-ddx",
		"Returns the partial derivative of x with respect to the screen-space x-coordinate."),
	"ddx_coarse": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/ddx-coarse",
		"Computes a low precision partial derivative with respect to the screen-space x-coordinate."),
	"ddx_fine": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/ddx-fine",
		"Computes a high precision partial derivative with respect to the screen-space x-coordinate."),
	"ddy": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-ddy",
		"Returns the partial derivative of x with respect to the screen-space y-coordinate."),
	"ddy_coarse": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/ddy-coarse",
		"Computes a low precision partial derivative with respect to the screen-space y-coordinate."),
	"ddy_fine": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/ddy-fine",
		"Computes a high precision partial derivative with respect to the screen-space y-coordinate."),
	"degrees": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-degrees",
		"Converts x from radians to degrees."),
	"determinant": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-determinant",
		"Returns the determinant of the square matrix m."),
	"DeviceMemoryBarrier": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/devicememorybarrier",
		"Blocks execution of all threads in a group until all device memory accesses have been completed."),
	"DeviceMemoryBarrierWithGroupSync": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/devicememorybarrierwithgroupsync",
		"Blocks execution of all threads in a group until all device memory accesses have been completed and all threads in the group have reached this call."),
	"distance": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-distance",
		"Returns the distance between two points."),
	"dot": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-dot",
		"Returns the dot product of two vectors."),
	"dst": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dst",
		"Calculates a distance vector."),
	"errorf": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/errorf",
		"Submits an error message to the information queue."),
	"EvaluateAttributeAtCentroid": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/evaluateattributeatcentroid",
		"Evaluates at the pixel centroid."),
	"EvaluateAttributeAtSample": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/evaluateattributeatsample",
		"Evaluates at the indexed sample location."),
	"EvaluateAttributeSnapped": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/evaluateattributesnapped",
		"Evaluates at the pixel centroid with an offset."),
	"exp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-exp",
		"Returns the base-e exponent."),
	"exp2": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-exp2",
		"Base 2 exponent (per component)."),
	"f16tof32": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/f16tof32",
		"Converts the float16 stored in the low-half of the uint to a float."),
	"f32tof16": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/f32tof16",
		"Converts an input into a float16 type."),
	"faceforward": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-faceforward",
		"Returns -n * sign(dot(i, ng))."),
	"firstbithigh": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/firstbithigh",
		"Gets the location of the first set bit starting from the highest order bit and working downward, per component."),
	"firstbitlow": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/firstbitlow",
		"Returns the location of the first set bit starting from the lowest order bit and working upward, per component."),
	"floor": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-floor",
		"Returns the greatest integer which is less than or equal to x."),
	"fma": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-fma",
		"Returns the double-precision fused multiply-addition of a * b + c."),
	"fmod": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-fmod",
		"Returns the floating point remainder of x/y."),
	"frac": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-frac",
		"Returns the fractional part of x."),
	"frexp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-frexp",
		"Returns the mantissa and exponent of x."),
	"fwidth": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-fwidth",
		"Returns abs(ddx(x)) + abs(ddy(x))."),
	"GetRenderTargetSampleCount": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-getrendertargetsamplecount",
		"Returns the number of render-target samples."),
	"GetRenderTargetSamplePosition": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-getrendertargetsampleposition",
		"Returns a sample position (x,y) for a given sample index."),
	"GroupMemoryBarrier": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/groupmemorybarrier",
		"Blocks execution of all threads in a group until all group shared accesses have been completed."),
	"GroupMemoryBarrierWithGroupSync": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/groupmemorybarrierwithgroupsync",
		"Blocks execution of all threads in a group until all group shared accesses have been completed and all threads in the group have reached this call."),
	"InterlockedAdd": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedadd",
		"Performs a guaranteed atomic add of value to the dest resource variable."),
	"InterlockedAnd": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedand",
		"Performs a guaranteed atomic and."),
	"InerlockedCompareExchange": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedcompareexchange",
		"Atomically compares the input to the comparison value and exchanges the result."),
	"InterlockedCompareStore": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedcomparestore",
		"Atomically compares the input to the comparison value."),
	"InterlockedExchange": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedexchange",
		"Assigns value to dest and returns the original value."),
	"InterlockedMax": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedmax",
		"Performs a guaranteed atomic max."),
	"InterlockedMin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedmin",
		"Performs a guaranteed atomic min."),
	"InterlockedOr": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedor",
		"Performs a guaranteed atomic or."),
	"InterlockedXor": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/interlockedxor",
		"Performs a guaranteed atomic xor."),
	"isfinite": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-isfinite",
		"Returns true if x is finite, false otherwise."),
	"isinf": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-isinf",
		"Returns true if x is +INF or -INF, false otherwise."),
	"isnan": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-isnan",
		"Returns true if x is NAN or QNAN, false otherwise."),
	"ldexp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-ldexp",
		"Returns x * 2exp."),
	"length": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-length",
		"Returns the length of the vector v."),
	"lerp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-lerp",
		"Returns x + s(y - x)."),
	"lit": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-lit",
		"Returns a lighting vector (ambient, diffuse, specular, 1)."),
	"log": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-log",
		"Returns the base-e logarithm of x."),
	"log10": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-log10",
		"Returns the base-10 logarithm of x."),
	"log2": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-log2",
		"Returns the base-2 logarithm of x."),
	"mad": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/mad",
		"Performs an arithmetic multiply/add operation on three values."),
	"max": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-max",
		"Selects the greater of x and y."),
	"min": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-min",
		"Selects the lesser of x and y."),
	"modf": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-modf",
		"Splits the value x into fractional and integer parts."),
	"msad4": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-msad4",
		"Compares a 4-byte reference value and an 8-byte source value and accumulates a vector of 4 sums."),
	"mul": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-mul",
		"Performs matrix multiplication using x and y."),
	"noise": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-noise",
		"Generates a random value using the Perlin-noise algorithm."),
	"normalize": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-normalize",
		"Returns a normalized vector."),
	"pow": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-pow",
		"Returns x^y."),
	"printf": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/printf",
		"Submits a custom shader message to the information queue."),
	"Process2DQuadTessFactorsAvg": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/process2dquadtessfactorsavg",
		"Generates the corrected tessellation factors for a quad patch."),
	"Process2DQuadTessFactorsMax": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/process2dquadtessfactorsmax",
		"Generates the corrected tessellation factors for a quad patch."),
	"Process2DQuadTessFactorsMin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/process2dquadtessfactorsmin",
		"Generates the corrected tessellation factors for a quad patch."),
	"ProcessIsolineTessFactors": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processisolinetessfactors",
		"Generates the rounded tessellation factors for an isoline."),
	"ProcessQuadTessFactorsAvg": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processquadtessfactorsavg",
		"Generates the corrected tessellation factors for a quad patch."),
	"ProcessQuadTessFactorsMax": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processquadtessfactorsmax",
		"Generates the corrected tessellation factors for a quad patch."),
	"ProcessQuadTessFactorsMin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processquadtessfactorsmin",
		"Generates the corrected tessellation factors for a quad patch."),
	"ProcessTriTessFactorsAvg": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processtritessfactorsavg",
		"Generates the corrected tessellation factors for a tri patch."),
	"ProcessTriTessFactorsMax": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processtritessfactorsmax",
		"Generates the corrected tessellation factors for a tri patch."),
	"ProcessTriTessFactorsMin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/processtritessfactorsmin",
		"Generates the corrected tessellation factors for a tri patch."),
	"QuadReadAcrossDiagonal": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/quadreadaccrossdiagonal",
		"Returns the specified local value which is read from the diagonally opposite lane in this quad."),
	"QuadReadLaneAt": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/quadreadlaneat",
		"Returns the specified source value from the lane identified by the lane ID within the current quad."),
	"QuadReadAcrossX": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/quadswapx",
		"Returns the specified local value read from the other lane in this quad in the X direction."),
	"QuadReadAcrossY": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/quadswapy",
		"Returns the specified source value read from the other lane in this quad in the Y direction."),
	"radians": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-radians",
		"Converts x from degrees to radians."),
	"rcp": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/rcp",
		"Calculates a fast, approximate, per-component reciprocal."),
	"reflect": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-reflect",
		"Returns a reflection vector."),
	"refract": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-refract",
		"Returns the refraction vector."),
	"reversebits": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/reversebits",
		"Reverses the order of the bits, per component."),
	"round": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-round",
		"Rounds x to the nearest integer."),
	"rsqrt": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-rsqrt",
		"Returns 1 / sqrt(x)."),
	"saturate": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-saturate",
		"Clamps x to the range [0, 1]."),
	"sign": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-sign",
		"Computes the sign of x."),
	"sin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-sin",
		"Returns the sine of x."),
	"sincos": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-sincos",
		"Returns the sine and cosine of x."),
	"sinh": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-sinh",
		"Returns the hyperbolic sine of x."),
	"smoothstep": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-smoothstep",
		"Returns a smooth Hermite interpolation between 0 and 1."),
	"sqrt": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-sqrt",
		"Square root (per component)."),
	"step": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-step",
		"Returns (x >= a) ? 1 : 0."),
	"tan": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-tan",
		"Returns the tangent of x."),
	"tanh": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-tanh",
		"Returns the hyperbolic tangent of x."),
	"transpose": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-transpose",
		"Returns the transpose of the matrix m."),
	"trunc": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-trunc",
		"Truncates floating-point value(s) to integer value(s)."),
	"WaveActiveAllEqual": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveactiveallequal",
		"Returns true if the expression is the same for every active lane in the current wave (and thus uniform across it)."),
	"WaveActiveBitAnd": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallbitand",
		"Returns the bitwise AND of all the values of the expression across all active lanes in the current wave and replicates it back to all active lanes."),
	"WaveActiveBitOr": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallbitor",
		"Returns the bitwise OR of all the values of the expression across all active lanes in the current wave and replicates it back to all active lanes."),
	"WaveActiveBitXor": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallbitxor",
		"Returns the bitwise XOR of all the values of the expression across all active lanes in the current wave and replicates it back to all active lanes."),
	"WaveActiveCountBits": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveactivecountbits",
		"Counts the number of boolean variables which evaluate to true across all active lanes in the current wave, and replicates the result to all lanes in the wave."),
	"WaveActiveMax": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallmax",
		"Returns the maximum value of the expression across all active lanes in the current wave and replicates it back to all active lanes."),
	"WaveActiveMin": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallmin",
		"Returns the minimum value of the expression across all active lanes in the current wave replicates it back to all active lanes."),
	"WaveActiveProduct": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallproduct",
		"Multiplies the values of the expression together across all active lanes in the current wave and replicates it back to all active lanes."),
	"WaveActiveSum": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveallsum",
		"Sums up the value of the expression across all active lanes in the current wave and replicates it to all lanes in the current wave."),
	"WaveActiveAllTrue": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/wavealltrue",
		"Returns true if the expression is true in all active lanes in the current wave."),
	"WaveActiveAnyTrue": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveanytrue",
		"Returns true if the expression is true in any of the active lanes in the current wave."),
	"WaveActiveBallot": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveballot",
		"Returns a 4-bit unsigned integer bitmask of the evaluation of the Boolean expression for all active lanes in the specified wave."),
	"WaveGetLaneCount": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/wavegetlanecount",
		"Returns the number of lanes in a wave on this architecture."),
	"WaveGetLaneIndex": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/wavegetlaneindex",
		"Returns the index of the current lane within the current wave."),
	"WaveIsFirstLane": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveisfirstlane",
		"Returns true only for the active lane in the current wave with the smallest index."),
	"WavePrefixCountBits": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveprefixcountbytes",
		"Returns the sum of all the specified boolean variables set to true across all active lanes with indices smaller than the current lane."),
	"WavePrefixProduct": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveprefixproduct",
		"Returns the product of all of the values in the active lanes in this wave with indices less than this lane."),
	"WavePrefixSum": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/waveprefixsum",
		"Returns the sum of all of the values in the active lanes with smaller indices than this one."),
	"WaveReadLaneFirst": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/wavereadfirstlane",
		"Returns the value of the expression for the active lane of the current wave with the smallest index."),
	"WaveReadLaneAt": (
		"https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/wavereadlaneat",
		"Returns the value of the expression for the given lane index within the specified wave.")
}


def OpenMSDNLink(text):
	openStyle = 2
	openStyleSetting = sublime.load_settings("Victoria Syntax.sublime-settings").get("IntrinsicHoverLinkOpenStyle", "new_tab")
	if openStyleSetting == "same_window":
		openStyle = 0
	elif openStyleSetting == "new_window":
		openStyle = 1

	webbrowser.open(text, openStyle)


class IntrinsicHoverListener(sublime_plugin.EventListener):
	def on_hover(sef, view, point, hover_zone):
		if sublime.load_settings("Victoria Syntax.sublime-settings").get("IntrinsicHoverEnabled", True) == False:
			return
		if not view:
			return
		try:
			if view.syntax().name != "PdxShader":
				return
		except AttributeError:
			return

		scopesStr = view.scope_name(point)
		scopeList = scopesStr.split(' ')
		for scope in scopeList:
			if scope == "keyword.function.intrinsic.hlsl":
				posWord = view.word(point)
				intrinsicWord = view.substr(posWord)
				if intrinsicWord in IntrinsicList:
					url, desc = IntrinsicList[intrinsicWord]
					hoverBody = """
						<body id=show-intrinsic>
							<style>
								body {
									font-family: system;
								}
								p {
									font-size: 1.0rem;
									margin: 0;
								}
							</style>
							<p>%s</p>
							<br>
							<a href="%s">MSDN Link</a>
						</body>
					""" % (desc, url)

					view.show_popup(hoverBody, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point, max_width=1024, on_navigate=lambda x: OpenMSDNLink(x))
					return