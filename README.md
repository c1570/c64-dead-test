# C64 Dead Test 781220
https://github.com/c1570/c64-dead-test

The C64 Ultimax Mode "Dead Test 781220" cartridge ROM.
Version 002 to 006 modifications by Kinzi.

## Synopsis

In short, on power up, the cartridge will...
1. set screen to light gray immediately after power on
2. do a simple RAM check with different byte patterns (blank screen/changing colors, about 9 seconds)
   - any bit errors will be shown by a blinking pattern, 1 flash = D7, 2 flashes = D6, etc., see [dead_test_ok.png](/dead_test_ok.png) for mappings to ICs
3. do a more thorough RAM check of $0000-$01FF (blank screen/fast changing colors, about 3 seconds)
   - errors will be shown by the screen flashing 10 times (indicating problems in RAM addressing, e.g., U13/U25 and surrounding PCB traces)
4. after that, the text screen will be shown, running more tests in an indefinite loop (each pass takes about 100 seconds)
   - note that screen corruption in the 4K RAM test is expected as the charset gets overwritten temporarily.

If all tests pass, you can assume that CPU, PLA, VIC-II and RAM (first 4k only) are working to some degree.
This test **does not** test ROMs nor RAM above 4k nor CIAs (properly).
In fact, this test will work fine without CIA1 (and often CIA2 as well) and without any ROMs.

Two low current LEDs connected to the tape port (anode to motor/sense pins, 1.8k resistor in series, wire to GND) will mirror any RAM bit error flashing (see step 2 above), or flip their status every few dozen seconds while the continuous tests are running (step 4).

For the original 781220 manual, search "781220 manual" on the net.

## Historical info

For Kinzi's original update notes, see [dead_test.txt](/dead_test.txt)
