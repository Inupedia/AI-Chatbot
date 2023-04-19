from bilibili_api import live, sync
import queue


class BilibiliLive:
    def __init__(self, room_id, message_queue: queue.Queue = None):
        self.room_id = room_id
        self.message_queue = message_queue

    async def on_danmaku(self, event):
        message = event["data"]["info"][1]
        username = event["data"]["info"][2][1]
        self.message_queue.put((username, message))

    def start(self):
        room = live.LiveDanmaku(self.room_id)
        room.on("DANMU_MSG")(self.on_danmaku)
        sync(room.connect())
