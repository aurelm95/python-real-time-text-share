#!/usr/bin/env python

import asyncio
import websockets
import json


class ShareTXT_Client():
    def __init__(self):
        pass
    
    async def connect_websocket(self):
        async with websockets.connect("wss://sharetxt.tk") as self.websocket:
            print("conexion iniciada")
            await self.websocket.send(json.dumps({"roomName":"default", "type":"connection"}))
            while True:
                # action=input("plus or minus?\t")
                # await websocket.send(json.dumps({"action":action}))
                response = await self.websocket.recv()
                response=json.loads(response)
                # print(response)
                if response['type']=='msg':
                    self.on_new_text_recieved(response['msg'])
                else:
                    print("Num users connected:",response['numUsers'])
    
    def on_new_text_recieved(self,message):
        print(message,end='\r')
    
    def send_text(self,text):
        asyncio.run(self.websocket.send(json.dumps({"roomName":"default", "type":"message", "text":text})))
    
    def start_client(self):
        print("Starting client...")
        asyncio.run(self.connect_websocket())


if __name__=='__main__':
    import threading
    import time
    sc=ShareTXT_Client()
    # https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c
    client_thread=threading.Thread(target=sc.start)
    client_thread.daemon=True
    client_thread.start()
    time.sleep(3)
    print("Sending text...")
    sc.send_text("hola")