import asyncio
import logging

from telethon import TelegramClient, events
from config import apis_telegram, master_account

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)


class TelegramClientHandler:
    resend_message = {}
    rsp_blocker = 5

    def __init__(self, session_name: str, api_id: int, api_hash: str):
        self.session_name = session_name
        self.client = TelegramClient(f"data/{session_name}", api_id, api_hash)
        self.user = None

    async def start(self):

        # logging.debug(f'Try start {self.session_name}')

        @self.client.on(events.NewMessage(outgoing=False))
        async def handler(event):
            logging.debug(f"[{self.client.session.filename}] Новое сообщение: {event.message.text}")
            if event.is_reply:
                logging.debug(f'replay={self.resend_message}')
                logging.debug(f'\n\nmessage replayed\n{event.message.reply_to.reply_to_msg_id}')
                user_id = self.resend_message.get(str(event.message.reply_to.reply_to_msg_id))
                if user_id:
                    await self.client.send_message(user_id, event.raw_text)
                    del self.resend_message[str(event.message.reply_to.reply_to_msg_id)]
            else:
                logging.debug(f'event.raw_text={event.raw_text}')
                user = await event.get_sender()
                frd = await self.client.forward_messages(master_account, event.message)
                self.resend_message[str(frd.id)] = user.id
                logging.debug(f"{frd}\nforward message\n{event}")

        await self.client.start()
        logging.debug(f"{self.client.session.filename} запущено")
        self.user = self.client.get_me()

    async def run_until_disconnected(self):
        await self.client.run_until_disconnected()


async def main():
    logging.debug('create clients')
    clients = [TelegramClientHandler(f'{i["user"]}', i["api_id"], i["api_hash"]) for i in apis_telegram]

    logging.debug('start clients')
    for client in clients:
        logging.debug(f"Запускаємо клієнт {client.session_name}")
        await client.start()

    logging.debug('work clients')
    await asyncio.gather(*(client.run_until_disconnected() for client in clients))
    logging.debug('stop clients')

if __name__ == "__main__":
    asyncio.run(main())
