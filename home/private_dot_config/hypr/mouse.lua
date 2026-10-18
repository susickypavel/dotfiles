-- Windows "Enhance pointer precision" profile for a 1000 Hz mouse.
-- Default curve and Windows pointer-speed slider 6/11.
-- Generate a new curve with: python3 ~/.config/hypr/windows-accel-gen.py
hl.config({
  input = {
    accel_profile = "custom 0.25 0.0000 0.1456 0.2913 0.4369 0.5826 0.7282 0.8739 1.0915 1.3106 1.5297 1.7488 1.9679 2.1870 2.4061 2.6252 2.8443 3.0634 3.2825 3.5584 3.8912 4.2240 4.5568 4.8895 5.2223 5.5551 5.8879 6.2207 6.5535 6.8863 7.2190 7.5518 7.8846 8.2174 8.5502 8.8830 9.2158 9.5485 9.8813 10.2141 10.5469 10.8797 11.2125 11.5453 11.8780 12.2108 12.5436 12.8764 13.2092 13.5420 13.8747 14.2075 14.5403 14.8731 15.2059 15.5387 16.2122 16.9000",
    sensitivity = 0,
  },
})
