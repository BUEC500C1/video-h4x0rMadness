# video-h4x0rMadness
Twitter report to video summarizer - "DailyFeed"

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
  <img src="/graphs/architecture.png" width="80%">
</p>


## Description:

  1. the script get all feed texts
  
  2. texts being converted into images:
  
  <p align="center">
  <img width="80%" src="/graphs/images.png">
</p>

  <p align="center">
  <img width="80%" src="/graphs/19.png">
</p>

  3. images are converted into video and then images are deleted:
  
   <p align="center">
  <img width="80%" src="/graphs/video.png">
</p>

  4. user will see the progress bar in command line:
  
   <p align="center">
  <img width="80%" src="/graphs/progress.png">
</p>



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
      
 
