# C64 Dead Test 781220
https://github.com/c1570/c64-dead-test

The C64 Ultimax Mode "Dead Test 781220" cartridge ROM with lots of improvements and much better RAM check.
This version checks Stack and Screen RAM during the RAM 4KB test.

Version 002 to 006 modifications by Kinzi.

![Passing a test run](/dead_test.gif)

**[Download](https://github.com/c1570/c64-dead-test/raw/refs/heads/main/dead_test.bin)**

## Synopsis

In short, on power up, the cartridge will...
1. set screen to light gray immediately after power on
2. do a simple RAM check with different byte patterns (blank screen/changing colors, about 9 seconds)
   - any bit errors will be shown by a blinking pattern, 1 flash = D7, 2 flashes = D6, etc., see [dead_test_ok.png](/dead_test_ok.png) for mappings to ICs
3. do a more thorough RAM check of $0002-$01FF (blank screen/fast changing colors, about 3 seconds)
   - errors will be shown by the screen flashing 10 times (indicating problems in RAM addressing - check U13/U25 and surrounding PCB traces)
4. after that, the text screen will be shown, running more tests in an infinite loop
   - during the RAM 4K test, screen output will be (mostly) random text (VIC-II screen mem set to $0000, charset to cartridge ROM $F800; otherwise screen mem $0400 and charset RAM $0800)
   - sound will play about 40 seconds after initial power on
   - each loop of step 4 takes about 40 seconds
   - if no text is readable (only) during the RAM 4K test, the VIC-II cannot access ROM properly (check U26 and surrounding PCB traces or PLA)
   - `ADRFAIL` in the RAM 4K test indicates addressing problems similar to failing in step 3

If all tests pass, you can assume that CPU, PLA, VIC-II and RAM (first 4k only) are working to some degree.
This test **does not** test ROMs nor RAM above 4k nor CIAs (properly).
In fact, this test will work fine without CIA1 (and often CIA2 as well) and without any ROMs.

Two low current LEDs connected to the tape port (anode to motor/sense pins, 1.8k resistor in series, wire to GND) will mirror any RAM bit error flashing (see step 2 above), or flip their status every few dozen seconds while the continuous tests are running (step 4).

For the original 781220 manual, search "781220 manual" on the net.

## Historical info

For Kinzi's original update notes, see [dead_test.txt](/dead_test.txt)
