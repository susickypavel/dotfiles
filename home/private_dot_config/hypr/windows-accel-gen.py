#!/usr/bin/env python3
"""Generate a Hyprland/libinput custom accel curve that replicates Windows
"Enhance pointer precision" (Enhanced Pointer Precision, EPP).

Implements the algorithm from Microsoft's "Pointer Ballistics for Windows XP"
whitepaper as used by Windows 7/10/11:

  1. Per USB packet, mouse speed for the curve lookup: v = counts_per_packet / 3.5
  2. Gain from the default SmoothMouseX/YCurve registry points:
     gain(v) = Y(v) / v   (Y interpolated linearly between points,
                           extrapolated linearly beyond the last point)
  3. Pixels moved = counts * slider_multiplier * gain(v) / (3.5 * 150 / 96)
     (150 = Win7+ hard-coded update rate, 96 = assumed screen DPI)

Windows never measures real time -- it uses counts PER PACKET -- so its accel
depends on the mouse's polling rate. libinput's custom profile x-axis is
device units per millisecond (real time), so we convert using POLL_HZ.

Tunables below. Rerun after changing:  python3 ~/.config/hypr/windows-accel-gen.py
then paste the output line into the accel_profile string in mouse.lua.
When using chezmoi, edit the repository copy, apply it, and reload Hyprland.
"""

# ---- tunables ---------------------------------------------------------------
POLL_HZ = 1000   # your mouse's polling rate on this machine (VXE 1K dongle = 1000)
                 # set 125 for the "classic" much stronger EPP accel feel
SLIDER = 1.0     # Windows pointer-speed slider with EPP on:
                 # 1..11 -> 0.1 0.2 0.4 0.6 0.8 [1.0=6/11 default] 1.2 1.4 1.6 1.8 2.0
EXTRA_SENS = 1.0 # extra flat multiplier on top (1.0 = authentic Windows)

# libinput custom motion profile: 64 points max, uniform step in device-units/ms
STEP = 0.25
NPOINTS = 57     # covers 0 .. 14 du/ms; beyond that libinput's linear
                 # extrapolation exactly matches Windows' own extrapolation

# ---- Windows default SmoothMouseCurve (registry 16.16 fixed point) -----------
XC = [0x00000000, 0x00006E15, 0x00014000, 0x0003DC29, 0x00280000]
YC = [0x00000000, 0x00015EB8, 0x00054CCD, 0x00184CCC, 0x02380000]
XC = [v / 65536 for v in XC]  # 0, 0.43, 1.25, 3.86, 40
YC = [v / 65536 for v in YC]  # 0, 1.37, 5.30, 24.30, 568

GAIN_UNITY = 3.5 * 150 / 96   # Win7+ 1:1 normalization = 5.46875


def y_curve(v):
    """SmoothMouseYCurve(v): linear interpolation, linear extrapolation."""
    if v <= 0:
        return 0.0
    for i in range(1, len(XC)):
        if v <= XC[i]:
            t = (v - XC[i - 1]) / (XC[i] - XC[i - 1])
            return YC[i - 1] + t * (YC[i] - YC[i - 1])
    slope = (YC[-1] - YC[-2]) / (XC[-1] - XC[-2])
    return YC[-1] + slope * (v - XC[-1])


def f(x_du_per_ms):
    """libinput custom profile: output speed for input speed x (du/ms)."""
    if x_du_per_ms == 0:
        return 0.0
    counts_per_packet = x_du_per_ms * 1000 / POLL_HZ
    v = counts_per_packet / 3.5
    gain = (y_curve(v) / v) / GAIN_UNITY * SLIDER * EXTRA_SENS
    return x_du_per_ms * gain


points = " ".join(f"{f(STEP * k):.4f}" for k in range(NPOINTS))
print(f"custom {STEP} {points}")
