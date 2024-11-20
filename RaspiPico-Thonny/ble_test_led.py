from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

BLE_NAME = "picow"

ble = bluetooth.BLE()

sp = BLESimplePeripheral(ble, name=BLE_NAME )

led = Pin("LED", Pin.OUT)

state_led = 0

def on_rx( data ):
    print( f"Received Data: {data}" )
    global state_led

    if( data == b'change' ):
        if( state_led == 0 ):
            state_led = 1
            led.value( state_led )
            sp.send( "LED ON" )
        else:
            state_led = 0
            led.value( state_led )
            sp.send( "LED OFF" )

while True:
    if( sp.is_connected() ):
        sp.on_write( on_rx )
