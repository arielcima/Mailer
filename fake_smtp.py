import asyncio
from aiosmtpd.controller import Controller

class FakeSmtpHandler:
    async def handle_DATA(self, server, session, envelope):
        print("=========================================")
        print(f"Received message from: {envelope.mail_from}")
        print(f"Message addressed to : {envelope.rcpt_tos}")
        print("Message data:")
        print(envelope.content.decode('utf8', errors='replace'))
        print("=========================================\n")
        # Return 250 to tell the sender it was accepted for delivery
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    # Initialize the handler and controller
    handler = FakeSmtpHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=25)
    
    print("Starting fake SMTP server on 127.0.0.1:25...")
    print("Waiting for messages. Press Ctrl+C to quit.")
    
    # Start the server
    controller.start()
    
    try:
        # Keep the event loop running to listen for incoming connections
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        controller.stop()
