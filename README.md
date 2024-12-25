# 2024 Advent of Code Solutions

These are roughly a port of my [rust
solutions](https://github.com/mattcl/cl-aoc2024), with a similar
performance-oriented goal.


## Total runtime ~793.1 ms

```
❯ aoc-tools python-summary benchmarks.json -l bench-suffixes.json
+------------------------------------------------------+
| Problem                     Time (ms)   % Total Time |
+======================================================+
| 01 historian hysteria         0.77458          0.098 |
| 02 red nosed reports          3.09283          0.390 |
| 03 mull it over               1.30733          0.165 |
| 04 ceres search               6.11644          0.771 |
| 05 print queue                1.73810          0.219 |
| 06 guard gallivant           23.64848          2.982 |
| 07 bridge repair             16.60854          2.094 |
| 08 resonant collinearity      0.63158          0.080 |
| 09 disk fragmenter           15.75009          1.986 |
| 10 hoof it                    2.48683          0.314 |
| 11 plutonium pebbles         64.04271          8.075 |
| 12 garden groups             20.48014          2.582 |
| 13 claw contraption           0.80211          0.101 |
| 14 restroom redoubt          30.33278          3.825 |
| 15 warehouse woes             9.46622          1.194 |
| 16 reindeer maze             29.53723          3.724 |
| 17 chronospatial computer     0.74833          0.094 |
| 18 ram run                   14.55448          1.835 |
| 19 linen layout              16.88883          2.130 |
| 20 race condition            41.49726          5.233 |
| 21 keypad conundrum           1.25048          0.158 |
| 22 monkey market            485.25099         61.188 |
| 23 lan party                  2.63399          0.332 |
| 24 crossed wires              0.50582          0.064 |
| 25 code chronicle             2.90690          0.367 |
| Total                       793.05306        100.000 |
+------------------------------------------------------+
```
