from micro_ov2640 import *
from machine import I2C, SPI, Pin
from bme280 import BME280, BMP280_I2CADDR
from time import sleep
from rfm69 import RFM69


# BMP280
i2c = I2C(0)
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )


# RFM69
FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node
BASESTATION_ID = 100 # ID of the node (base station) to be contacted

nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
pin = Pin( 25, Pin.OUT )

spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )
print( 'Ground Station NODE:', BASESTATION_ID )

rfm.ack_retries = 3
rfm.ack_wait    = 0.5
rfm.destination = BASESTATION_ID

cam = ov2640()
cam.Camera_Init()
cam.spi_Test()

while True:
    values = bmp.raw_values
    ack = rfm.send_with_ack(bytes(f"{values[0]}, {values[1]}", "utf-8"))
    print("   +->", "ACK received" if ack else "ACK missing" )
    cam.read_fifo_burst()
    print("-----------------------------")
    pin.on()
    sleep(0.5)
    pin.off()
