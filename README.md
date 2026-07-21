# Casio Link
Casio protocol reverse engineering (Casio Link FA-124 protocol) for my Casio fx-7400G PLUS calculator.
Unfortunatelly original software is gone...

## Connection
Calculator uses 2.5 mm jack for serial communication.

Make sure your serial converter output/input is working with 3.3V levels. Higher voltages will damage your calculator.

I would recommend puting a small resistor (~330 Ohm) in series with TxD and RxD lines.

| 2.5 mm jack | Calculator function | Serial converter (3.3V CMOS) connection |
| --- | --- | --- |
| Tip | TxD (output) | RxD |
| Ring | RxD (input) | TxD |
| Sleeve | GND | GND |

## Serial port parameters
Calculator works with standard serial communication 9600 8N2

## Serial protocol
For now most of the information is to be found in the source. I will try to update the section as I make some progress.

### Initial synchronization
Initial synchronization is started by the transmitting side (TX), by sending ENQ (0x16).

The recieving side (RX) must response within the timeout with DC3 (0x13).

Afterwards a first header would be transmitted.

### Checksum
Each header's or payload's last byte is a checksum.

The checksum value is: (0x13A - sum(all_bytes_expect_checksum)) & 0xFF

### Header
Each "chunk" of data is preceeded by the header. The header length is exactly 50 bytes.

Header carries information:
* Transfer type (like TXT, VAL, ...)
* Transfer category (like PG for programs)
* Payload length
* File/variable/... name

Header might be accepted by sending ACK (0x06) or rejected (for example when file exists) by sending 0x21. Only after header is accepted the payload is transmitted. There seem to be no timeout on this operation.

### Graph Header
There is a special header for graph/image transfer. The graph header length is exactly 40 bytes.

| Byte no | Information |
| ------- | ----------- |
| 0 - 2   | Image heder indicator = `:DD` |
| 3       | Image height in pixels |
| 4       | Image width in pixels |
| 5 - 8   | Some unknown data |
| 9 - 48  | 0xFF |
| 49      | Checksum |

After acking this a payload of size of N = (Image height) * (Image width) / 8 + 2 is transmitted.

| Byte no   | Information |
| --------- | ----------- |
| 0         | Frame start = `:` |
| 1 - (N-2) | Image data |
| (N-1)     | Checksum |

For image data decoding see source code. Each byte represents a row of 8 pixels, starting from left bottom corner, and progressing up and then right.

### END Header
There is a special header (length is still 50 bytes) containing `:END` information.

All other bytes are padded with 0xFF, and the checksum is applied as a last byte.

This header indicates that the connection is complete from TX side.

Note: full calculator backup does not send END packed after is completed.

### Payload
Carries data indicated by preeceding header.

Last byte is probably a checksum.

### Rejection (0x21)
If RX rejects a header this fact must be acknowledged by sending ACK (0x06).

After this RX will respond with ACK (0x06) as well and the communication might continue.

### Communication error (0x22)
If the communication error is detected (ex. wrong checksum, wrong response to rejection, wrong handshake) the side that want to indicate error sends 0x22.
After this the communication must be started from scratch (calculator asks to press AC that will exit transmit/recieve modes)

## Appendix
Below there are some interesting observations, tips and tricks.

### Test mode
In order to enter test mode of the calculator you need to press and hold [▶] and [a b/c] and then press [AC/ON], then release all three buttons.

**Please be aware that after you exit test mode all the memory would be wiped! Make backup before!**

### Password protected programs
The calculator allows for pasword protected programs, which source code is available for edit/view and transfer only after entering correct password.

First note about this is that in order to give user time to enter password in file transfer mode you need to increase timeout in the software (maybe in the future this wil be handled in a better way).

Second security observation is the fact, that still you can execute full backup. During this process user is not asked to enter any password - and after rewieving the backup content both password and the file contents can be extracted.

## Disclaimer / Use at Your Own Risk

**IMPORTANT: Read this before using any hardware designs, schematics, or software in this repository.**

1. **No Warranty:** This project is provided "as is" and "with all faults." The author(s) make no representations or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, typographical errors, or other harmful components of this software or hardware. 
2. **Risk of Damage:** Working with electronics carries inherent risks, including but not limited to electric shock, fire, burns, short circuits, and permanent damage to your equipment, components, or computer. 
3. **Limitation of Liability:** In no event shall the authors or copyright holders be liable for any injury, property damage, data loss, or financial loss arising from the use, modification, or distribution of this project.
4. **User Responsibility:** You are solely responsible for verifying the schematics, code correctness, and power requirements before flashing any firmware or powering up any hardware.

**By using these materials, you agree to assume all risks associated with their use.**
