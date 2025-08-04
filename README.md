# C64 Dead Test
https://github.com/c1570/c64-dead-test

The C64 "Dead Test" ROM, trying to coax your C64 to life even if its ROMs and RAM are mostly gone.

Compared with the original CBM "Dead Test 781220", this version gives better indications of the type of RAM errors, and features additional tests.
In standard Ultimax cartridge mode, it can only check the first 4KBytes of RAM.
If removing the GAME jumper during sound check or using the ROM as KERNAL ROM, it checks the full 64KBytes.

Version 002 to 006 modifications by Kinzi.

![Passing a test run](/dead_test.gif)

**[Download](https://github.com/c1570/c64-dead-test/raw/refs/heads/main/dead_test.bin)**

## Synopsis
Named aptly, the Dead Test ROM is your first go to point in case your C64 only presents a black screen after power up.
As long as the CPU has access to the cartridge ROM (i.e., address bus and data lines are working, PLA and CPU and logic ICs aren't completely broken), Dead Test will do _something_.

## Tape port LEDs
Two low current LEDs connected to the tape port (anode to motor/sense pins, 1.8k resistor in series, wire to GND) will mirror any RAM bit error flashing (see step 4 above), or flip their status every few dozen seconds while the tests are looping.

In case the Dead Test still gives a black screen, and even these LEDs don't do anything, there is a bigger problem with the buses, logic ICs, and/or PLA.

## Testing steps
The cartridge will set the screen to light gray immediately after power on.

After that, tests will be run as follows.

### Integrity test of the Dead Test ROM
Takes a few milliseconds. 15 black/white flashes in case of an error.

### RAM addressing check
Takes a few milliseconds. 25 red/blue flashes in case of an error for about 15 seconds, **continues** even after detecting an error.

This test reads RAM location $0b55 (just an arbitrary location really) then writes to all other RAM addresses, then rechecks $0b55 and reports an error in case that changed.

An error in this check indicates a problem with U13/U25 and surrounding PCB traces but can also happen due to RAM chips forcing address lines low or having floating outputs.

### Pattern based RAM check
Blank screen/changing colors, takes about 9 seconds.

This fills RAM (4k, up to $0fff) with a one byte test pattern, then reads again and checks, then repeats with another pattern (from a set of 22 pattern bytes).

Any bit errors will be shown by a blinking pattern, 1 flash = D7, 2 flashes = D6, etc., see [dead_test_ok.png](/dead_test_ok.png) for mappings to ICs

### More thorough RAM check of $0002-$01FF
Blank screen/fast changing colors, about 3 seconds.

This fills zeropage/stack with 00,01,02... and checks, then with 01,02,03... then checks, etc.

Errors will be shown by the screen flashing 10 times and indicate problems in RAM addressing similar to the __RAM addressing check__.

### Initialize screen
With lower RAM having checked out okay, the text screen will be initialized.

Screen mem is at $0400, charset in RAM $0800.

### Zero page test
Similar to the pattern based RAM check.

### Color RAM test
Again, similar to the pattern based RAM check.

### RAM test 4k
Fills $006b-$0fff with pseudo-random data, then checks.

During this test, screen output will be (mostly) random text (VIC-II screen mem set to $0000, charset from cartridge ROM $F800 (or CHARROM if using the Dead Test ROM as KERNAL).

In case the "ram test is running, screen will be restored in a few seconds" message/charset is garbled, the VIC-II cannot access ROM properly (check U26 and surrounding PCB traces or PLA).

`ADRFAIL` in this test indicates addressing problems similar to failing in the __RAM addressing check__.

### CIA1 Timer A test
Tests whether CIA1 Timer A can be programmed and fires correctly. This timer is used by BASIC V2 to generate interrupts (read keyboard, blink cursor).

Failing this check indicates a broken CIA1, broken PCB traces, broken PLA, or broken logic ICs processing PLA output.

If this test passes but BASIC V2 still shows no cursor, the IRQ line is probably shorted or disconnected (check IC sockets).

### Sound test
Plays 6 notes using voice 1, then the same 6 notes one octave higher using voice 2 and a bit louder, then again one octave higher using voice 3 and again a bit louder.
The first pass uses sine, the next sawtooth, the next square, the last pass uses the noise waveform.

This runs about 40 seconds after initial power on.

**During sound check, remove the GAME jumper** from the cartridge to have it run additional checks. Removing must be quick and **bounce free**, or the C64 will crash.

### Additional tests
If the GAME jumper gets removed during sound test or the Dead Test ROM is used as KERNAL ROM, a few additional tests get run.

### RAM test 64k
This is similar to __RAM test 4k__ but checks $1000-$FFFF and uses the RAM charset.

### ROM CRC
Compare the CRCs displayed against this list.
If the CRCs displayed are not stable between test runs, there is definitely a problem.
```
0493 kernal-906145-02
1a9d chargen-901225-01
20dc chargen-906143-02
22ef JiffyDOS V6.01 SX64
2f69 kernal-901227-01
5283 Dead Test 20250804
6a8d basic-901226-01
8271 kernal-251104-04
9fcd kernal-901246-01
bccf kernal-901227-02
c2bc JiffyDOS V6.01 C64
cc25 kernal-390852-01
ffd0 kernal-901227-03
```

### Keyboard check
The keyboard check is active for some seconds, during which you can press some keys, or move the joystick.
The two bars of stars are the bit patterns of $DC00/$DC01.
Leftmost position of the first bar is PA7, rightmost position is PA0; leftmost for the second is PB7, rightmost is PB0.
For example, `0******* *******0` means the key at position PA7/PB0 has been pressed (see [keyboard matrix](https://www.c64-wiki.com/wiki/Keyboard#Keyboard_Matrix): it's the `1` key).

To check all lines, try keys `1`, `*`, `L`, `0`, `B`, `F`, `E`, CrsrDown.

If no reaction is visible at all, CIA1 or PCB traces or PLA/logic ICs are broken.
Partial faults may be due to cable or PCB trace or keyboard switch issues.

**VIC-II bank check**

During the keyboard check, a screen test pattern gets displayed on the VIC-II banks that are not actually selected for display by CIA2.
If the screen is garbled during Dead Test in general, but shows numbers in the upper quarter of the screen about a minute after the sound check and when in RAM mode, then there's a problem with CIA2 VIC-II bank selection (CIA2, logic ICs, PLA, PCB traces).

### Test looping
- In Ultimax mode, after the Sound Check, tests will loop to the Zero Page test.
- In RAM mode (GAME jumper removed during Sound Check), tests will loop after the keyboard test and restart from the 64k check.
- In KERNAL mode, tests will loop after the keyboard test to the Zero Page test.

### NMI handling
An NMI (e.g., pressing RESTORE) changes screen background color.
NMIs clobber the stack and may cause RAM tests to fail.

## Tests interpretation
If all Ultimax mode (cartridge and GAME jumper enabled) tests pass, you can assume that CPU, PLA, VIC-II and RAM (first 4k only) are working to some degree.
This test **does not** test ROMs nor RAM above 4k nor CIAs (properly) on its own.

If all tests including the __additional tests__ (GAME jumper removed/KERNAL mode) pass, and correct ROM checksums are displayed, the C64 should be able to start to BASIC V2.

## Historical info

For the original 781220 manual, search "781220 manual" on the net.

For Kinzi's original update notes, see [dead_test.txt](/dead_test.txt)
