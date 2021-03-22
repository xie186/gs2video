# gs2video

This software can be used to convert google slide with notes to video. 

It will perform the procedures below: 

1. Access google slide and generate a screenshot for each slide. 

2. Extract the notes and convert the text to speech using `gTTS (Google Text-to-Speech)`.
   The speech is saved as mp3 file. 

3. Merge the screenshots into a video with durations equal to the duration of the correpsonding audio. 


## Example 

```
python gs2video.py -p 1-aTBNXcSIqlMRzn-FHnRmRPbGlh5eY8MgZNaBwo15IM -o test.mp4
```



