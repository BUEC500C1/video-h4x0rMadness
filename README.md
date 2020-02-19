# video-h4x0rMadness
video-h4x0rMadness created by GitHub Classroom

## Function:

**Generate a short video of text version of twitter daily feed**

## Usage:
  
  - download twitter-feed-ffmpeg.py
  
  - in terminal: 
      
        python twitter-feed-ffmpeg.py 
    
    then the twitter feed short video should be in the path:
    
        ./UniquePicturesFolder/dailyfeed.mov
      
## Design:

        
<p align="center">
  <img width="700" height="400" src="/graphs/architecture.png">
</p>


## Description:

  - initialize the variables:
  
    ~~~~
    class DailyFeed:
    def __init__(self, API_key, API_secret_key, Access_token, Access_token_secret):
        self.api = self.authenticate(API_key, API_secret_key, Access_token, Access_token_secret)
        self.height = 700
        self.width = 400
        self.feed_number = 20
        self.q = queue.Queue()
        self.num_threads = 4
    ~~~~
  
  - start function:
  
    ~~~
    def Start(self):
        self.msg = self.get_home_feed(self.api)
        self.bar = Bar('Total Progress of Daily Feed', max=self.feed_number, fill='@', suffix='%(percent)d%%')
        self.per = 0
        self.create_folder()
        self.thread_main()
        self.merge_to_video()
        self.delete_pictures()
    ~~~

  - main function:
  
    ~~~
    if __name__ == '__main__':
      obj = DailyFeed(API_key, API_secret_key, Access_token, Access_token_secret)
      obj.Start()
      ~~~
