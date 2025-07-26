# C64 Dead Test
https://github.com/c1570/c64-dead-test

The C64 "Dead Test" ROM, trying to coax your C64 to life even if its ROMs and RAM are mostly gone.

Compared with the original CBM "Dead Test 781220", this version comes with lots of improvements and much better RAM check.
In standard Ultimax cartridge mode, it can only check the first 4KBytes of RAM.
If removing the GAME jumper during sound check or using the ROM as KERNAL ROM, it checks the full 64KBytes.

Version 002 to 006 modifications by Kinzi.

![Passing a test run](/dead_test.gif)

**[Download](https://github.com/c1570/c64-dead-test/raw/refs/heads/main/dead_test.bin)**

## Synopsis

Named aptly, the Dead Test ROM is your first go to point in case your C64 only presents a black screen after power up.
As long as the CPU has access to the cartridge ROM (i.e., address bus and data lines are working, PLA and CPU and logic ICs aren't completely broken), Dead Test will do _something_.

On power up, the cartridge will...
1. set screen to light gray immediately after power on
2. perform a simple self integrity check that checks reading the dead test ROM (15 flashes in case of an error)
3. run a simple RAM check with different byte patterns (blank screen/changing colors, about 9 seconds)
   - any bit errors will be shown by a blinking pattern, 1 flash = D7, 2 flashes = D6, etc., see [dead_test_ok.png](/dead_test_ok.png) for mappings to ICs
4. run a more thorough RAM check of $0002-$01FF (blank screen/fast changing colors, about 3 seconds)
   - errors will be shown by the screen flashing 10 times (indicating problems in RAM addressing - check U13/U25 and surrounding PCB traces)
5. after that, the text screen will be shown, running more tests in an infinite loop
   - during the RAM test, screen output will be (mostly) random text (VIC-II screen mem set to $0000, charset to cartridge ROM $F800; otherwise screen mem $0400 and charset RAM $0800)
   - sound will play about 40 seconds after initial power on
   - **during sound check, remove the GAME jumper** from the cartridge to have it run additional checks (see "RAM mode" below). Removing must be quick and **bounce free**, or the C64 will crash, so perhaps use a good mechanical switch.
   - each loop of step 5 takes about 40 seconds
   - during the RAM test, in case the "ram test is running, screen will be restored in a few seconds" message/charset is garbled, the VIC-II cannot access ROM properly (check U26 and surrounding PCB traces or PLA)
   - `ADRFAIL` in the RAM test indicates addressing problems similar to failing in step 4
   - failing CIA1 check means that CIA1 timer A failed to run properly (CIA1 broken, PCB traces broken, PLA broken, logic ICs processing PLA output broken). This is far from a complete test but passing it should be enough for general BASIC V2 needs.

If all Ultimax mode tests pass, you can assume that CPU, PLA, VIC-II and RAM (first 4k only) are working to some degree.
This test **does not** test ROMs nor RAM above 4k nor CIAs (properly) on its own.
You need to switch to RAM mode during sound check for testing a bit more thoroughly.

An NMI (e.g., pressing RESTORE) changes screen background color.
NMIs clobber the stack and may cause RAM tests to fail.

### Tape port LEDs
Two low current LEDs connected to the tape port (anode to motor/sense pins, 1.8k resistor in series, wire to GND) will mirror any RAM bit error flashing (see step 3 above), or flip their status every few dozen seconds while the continuous tests are running (step 5).

In case the Dead Test still gives a black screen, and even these LEDs don't do anything, there is a bigger problem with the buses, logic ICs, and/or PLA.

## RAM mode
RAM mode is triggered by removing the cartridge's GAME jumper while the sound check is running.
This mode runs a few additional checks (see below).
If all checks pass, and correct ROM checksums are displayed, the C64 should be able to start to BASIC V2.
When looping tests, RAM mode cannot loop back to the zeropage and screen memory checks due to memory constraints.

### Keyboard check
The keyboard checks is active for some seconds, during which you can press some keys, or move the joystick.
The two bars of stars are the bit patterns of $DC00/$DC01.
Leftmost position of the first bar is PA7, rightmost position is PA0; leftmost for the second is PB7, rightmost is PB0.
For example, `0******* *******0` means the key at position PA7/PB0 has been pressed (see [keyboard matrix](https://www.c64-wiki.com/wiki/Keyboard#Keyboard_Matrix): it's the `1` key).

To check all lines, try keys `1`, `*`, `L`, `0`, `B`, `F`, `E`, CrsrDown.

If no reaction is visible at all, CIA1 or PCB traces or PLA/logic ICs are broken.
Partial faults may be due to cable or PCB trace or keyboard switch issues.

### VIC-II bank check
During the keyboard check, a screen test pattern gets displayed on the VIC-II banks that are not actually selected for display by CIA2.
If the screen is garbled during Dead Test in general, but shows numbers in the upper quarter of the screen about a minute after the sound check and when in RAM mode, then there's a problem with CIA2 VIC-II bank selection (CIA2, logic ICs, PLA, PCB traces).

### ROM CRC
Compare the CRCs displayed against this list.
If the CRCs displayed are not stable between test runs, there is definitely a problem.
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

## KERNAL ROM mode
If used as KERNAL ROM, after the sound check, similar to the RAM mode, a 64k RAM test as well as other additional tests get run.
During RAM tests, the charset from the CHARROM will be enabled.
If you get broken characters during the KERNAL mode RAM check, your CHARROM is broken, missing, or PLA/logic ICs do not enable it properly.

## Historical info

For the original 781220 manual, search "781220 manual" on the net.

For Kinzi's original update notes, see [dead_test.txt](/dead_test.txt)
