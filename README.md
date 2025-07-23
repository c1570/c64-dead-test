# C64 Dead Test 781220
https://github.com/c1570/c64-dead-test

The C64 "Dead Test 781220" ROM with lots of improvements and much better RAM check.
This version checks stack and screen RAM during the normal RAM test.

In Ultimax cartridge mode, it can only check the first 4KBytes of RAM.
If used as KERNAL ROM, it checks the full 64KBytes.

Version 002 to 006 modifications by Kinzi.

![Passing a test run](/dead_test.gif)

**[Download](https://github.com/c1570/c64-dead-test/raw/refs/heads/main/dead_test.bin)**

## Synopsis

In short, on power up, the cartridge will...
1. set screen to light gray immediately after power on
2. perform a simple self integrity check that checks reading the dead test ROM (15 flashes in case of an error)
3. run a simple RAM check with different byte patterns (blank screen/changing colors, about 9 seconds)
   - any bit errors will be shown by a blinking pattern, 1 flash = D7, 2 flashes = D6, etc., see [dead_test_ok.png](/dead_test_ok.png) for mappings to ICs
4. run a more thorough RAM check of $0002-$01FF (blank screen/fast changing colors, about 3 seconds)
   - errors will be shown by the screen flashing 10 times (indicating problems in RAM addressing - check U13/U25 and surrounding PCB traces)
5. after that, the text screen will be shown, running more tests in an infinite loop
   - during the RAM test, screen output will be (mostly) random text (VIC-II screen mem set to $0000, charset to cartridge ROM $F800; otherwise screen mem $0400 and charset RAM $0800)
   - sound will play about 40 seconds after initial power on
   - each loop of step 5 takes about 40 seconds
   - during the RAM test, in case the "ram test is running, screen will be restored in a few seconds" message/charset is garbled, the VIC-II cannot access ROM properly (check U26 and surrounding PCB traces or PLA)
   - `ADRFAIL` in the RAM test indicates addressing problems similar to failing in step 4

If all tests pass, you can assume that CPU, PLA, VIC-II and RAM (**first 4k only**) are working to some degree.
This test **does not** test ROMs nor RAM above 4k nor CIAs (properly).
In fact, this test will work fine without CIA1 (and often CIA2 as well), without SID, and without any ROMs.

Two low current LEDs connected to the tape port (anode to motor/sense pins, 1.8k resistor in series, wire to GND) will mirror any RAM bit error flashing (see step 3 above), or flip their status every few dozen seconds while the continuous tests are running (step 5).

## KERNAL ROM mode
If used as KERNAL ROM, after the sound check, another RAM test pass up to the full 64KBytes is done.
During RAM tests, the charset from the CHARROM will be enabled.
If you get broken characters during the KERNAL mode RAM check, your CHARROM is broken, missing, or the PLA does not enable it properly.

## ROM CRC
```
0493 kernal-906145-02
1a9d chargen-901225-01
20dc chargen-906143-02
22ef JiffyDOS V6.01 SX64
2f69 kernal-901227-01
6a8d basic-901226-01
8271 kernal-251104-04
9fcd kernal-901246-01
bccf kernal-901227-02
c2bc JiffyDOS V6.01 C64
cc25 kernal-390852-01
ffd0 kernal-901227-03
```

## Historical info

For the original 781220 manual, search "781220 manual" on the net.

For Kinzi's original update notes, see [dead_test.txt](/dead_test.txt)
