# gs2video

This software can be used to convert google slide with notes to video. 

It will perform the procedures below: 

1. Access google slide and generate a screenshot for each slide. 

2. Extract the notes and convert the text to speech using `gTTS (Google Text-to-Speech)`.
   The speech is saved as mp3 file. 

3. Merge the screenshots into a video with durations equal to the duration of the correpsonding audio. 


## Support Me
Like what I do, Please consider supporting me.

<a href="https://coindrop.to/xie186" target="_blank"><img src="https://coindrop.to/embed-button.png" style="border-radius: 10px;" alt="Coindrop.to me" style="height: 57px !important;width: 229px !important;" ></a>


## Configure API 



https://developers.google.com/drive/api/quickstart/python

https://console.cloud.google.com/auth/scopes;verificationMode=true?project=gs2slide

How To Make a Demo Video for Google OAuth


## Example 

```
python gs2video.py -p 1-aTBNXcSIqlMRzn-FHnRmRPbGlh5eY8MgZNaBwo15IM -o test.mp4 --keep
python gs2slide/cli.py -p 1s5xjByZyT6oLRRSsO-cpPOQHRZkhXM1Jr36JMhWKv1g -o phred_score.mp4 --keep --force
```



