## Copyright 2020 Kefan Zhang
import tweepy
import os
import ffmpeg
import queue
from PIL import Image
from PIL import ImageDraw
from threading import Thread
from progress.bar import Bar
import glob


API_key = "sH7ldVlm3k9RhpJ8nC5bd4ksY"
API_secret_key = "kAgGmzXD6ngdaWwDiZWfeEDkFYce5kHNhtTSP1Zq6fCgT3pNen"

Access_token = "1171844680603951104-IRA3NyRuOm7WBWeN2wxQXURZ1lE6GD"
Access_token_secret = "QeKUCAdkerfuRTNL8vgfUWCFOWKNHmpFrOXhYInKH5vkV"

class DailyFeed:
    def __init__(self, API_key, API_secret_key, Access_token, Access_token_secret):
        self.api = self.authenticate(API_key, API_secret_key, Access_token, Access_token_secret)
        self.height = 700
        self.width = 400
        self.feed_number = 20
        self.q = queue.Queue()
        self.num_threads = 4


    def Start(self):
        self.msg = self.get_home_feed(self.api)
        self.bar = Bar('Total Progress of Daily Feed', max=self.feed_number, fill='@', suffix='%(percent)d%%')
        self.per = 0
        self.create_folder()
        self.thread_main()
        self.merge_to_video()
        self.delete_pictures()

    def delete_pictures(self):
        path = "./"
        paths = glob.glob(os.path.join(path, '*.png'))
        for file in paths:
            os.remove(file)

    def threadProcessing(self):
        while True:
            task_num = self.q.get()
            if task_num is None:
                print("Workflow Queue is Empty!")
                break
            self.txt2img(task_num)
            if self.per < self.feed_number:
                self.bar.next()
                self.per += 1
            else:
                self.bar.finish()

            self.q.task_done()

    def txt2img(self, seq):
        self.text = self.msg[seq]
        self.para, self.note_height, self.line_height = self.split_text()
        self.draw_text(seq)

    def thread_main(self):
        for i in range(self.num_threads):
            t = Thread(target=self.threadProcessing)
            t.daemon = True
            t.start()
        for item in range(self.feed_number):
            self.q.put(item)
        self.q.join()

    def authenticate(self, API_key, API_secret_key, Access_token, Access_token_secret):
        auth = tweepy.OAuthHandler(API_key, API_secret_key)
        auth.set_access_token(Access_token, Access_token_secret)
        api = tweepy.API(auth)
        return api

    def get_home_feed(self, api):
        msg = []
        statuses = api.home_timeline(count=self.feed_number)
        for status in statuses:
            text = status._json['text']
            for i in range(len(text)):
                if ord(text[i]) > 256:
                    text = text.replace(text[i], " ")
            msg.append(text)
        return msg

    def create_folder(self):
        dirName = 'UniquePicturesFolder'
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        except FileExistsError:
            print("Directory ", dirName, " already exists")
        path = "./UniquePicturesFolder"
        os.chdir(path)

    def split_text(self):
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            para, line_height, line_count = self.get_para(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((para, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def get_para(self, text):
        txt = Image.new('RGBA', (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(txt)
        para = ""
        sum_width = 0
        line_count = 1
        line_height = 0
        for char in text:
            width, height = draw.textsize(char)
            sum_width += width
            if sum_width > self.height:
                line_count += 1
                sum_width = 0
                para += '\n'
            para += char
            line_height = max(height, line_height)
        if not para.endswith('\n'):
            para += '\n'
        return para, line_height, line_count

    def draw_text(self, image_seq):
        img = Image.new(mode="RGB", size=(self.height, self.width), color=(0, 0, 0))
        img.save("test.png")
        note_img = Image.open("test.png").convert("RGBA")
        draw = ImageDraw.Draw(note_img)
        x, y = 0, 150
        for para, line_count in self.para:
            draw.text((x, y), para, fill=(255, 255, 255))
            y += self.line_height * line_count
        name = str(image_seq) + ".png"
        note_img.save(name)

    def merge_to_video(self):
        path = "./"
        files = path + "*.png"
        ffmpeg.input(files, pattern_type='glob', framerate=0.3*self.num_threads).output('dailyfeed.mov').run()


if __name__ == '__main__':
    obj = DailyFeed(API_key, API_secret_key, Access_token, Access_token_secret)
    obj.Start()
