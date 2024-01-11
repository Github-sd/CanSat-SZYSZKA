from machine import SPI, Pin
from rfm69 import RFM69
import time
import uos

FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 100 # ID of this node

spi = SPI(0, polarity=0, phase=0, firstbit=SPI.MSB) # baudrate=50000,
uart = machine.UART(0, baudrate=50000)
#uart.init(50000, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
#uos.dupterm(uart)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
pin = Pin(25, Pin.OUT)

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ

rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )

print("Waiting for packets...")
while True:
    packet = rfm.receive( with_ack=True )
    try:
        packet_text = str(packet, "utf-8").split(", ")
    except:
        continue
    print(f"{packet_text[0]} C, {packet_text[1]} hPa")
    pin.on()
    time.sleep(0.2)
    pin.off()
