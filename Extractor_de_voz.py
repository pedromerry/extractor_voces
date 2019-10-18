from pydub import AudioSegment
from repo.audioSegmentation import speakerDiarization,flags2segs
from repo import audioBasicIO
import subprocess
wav_file="interview.wav"
path_wav_file = "input/" + wav_file
sourceAudio = AudioSegment.from_wav(path_wav_file)
[fs, x] = audioBasicIO.readAudioFile(path_wav_file)
mt_step=0.2
result=speakerDiarization(path_wav_file,n_speakers=2,plot_res=True)
[intervals, classes]=flags2segs(result,mt_step)
wav_channel0=AudioSegment.empty()
wav_channel1=AudioSegment.empty()
wav_channel2=AudioSegment.empty()
wav_channel3=AudioSegment.empty()
video_channel0_str=""
video_channel1_str=""
video_channel2_str=""
video_channel3_str=""
for sample in zip(classes,intervals):
    if sample[0] == 0:
        wav_channel0 = wav_channel0 + sourceAudio[sample[1][0] * 1000:sample[1][1]*1000]
        video_channel0_str = video_channel0_str + "+"+"between(t,"+str(round(sample[1][0],2))+","+str(round(sample[1][1],2))+")"
    elif sample[0] == 1:
        wav_channel1 = wav_channel1 + sourceAudio[sample[1][0] * 1000:sample[1][1]*1000]
        video_channel1_str = video_channel1_str + "+"+"between(t," + str(round(sample[1][0], 2)) + "," + str(round(sample[1][1], 2)) + ")"
    elif sample[0] == 2:
        wav_channel2 = wav_channel2 + sourceAudio[sample[1][0] * 1000:sample[1][1]*1000]
        video_channel2_str = video_channel2_str + "+" + "between(t," + str(round(sample[1][0], 2)) + "," + str(round(sample[1][1], 2)) + ")"
    elif sample[0] == 3:
        wav_channel3 = wav_channel3 + sourceAudio[sample[1][0] * 1000:sample[1][1]*1000]
        video_channel3_str = video_channel3_str + "+" + "between(t," + str(round(sample[1][0], 2)) + "," + str(round(sample[1][1], 2)) + ")"
if wav_channel0 !=AudioSegment.empty():
    wav_channel0.export('output/wav_channel0.wav', format="wav") #Exports to a wav file in the current path.
if wav_channel1 !=AudioSegment.empty():
    wav_channel1.export('output/wav_channel1.wav', format="wav") #Exports to a wav file in the current path.
if wav_channel2 !=AudioSegment.empty():
    wav_channel2.export('output/wav_channel2.wav', format="wav") #Exports to a wav file in the current path.
if wav_channel3 !=AudioSegment.empty():
    wav_channel3.export('output/wav_channel3.wav', format="wav") #Exports to a wav file in the current path.

if video_channel0_str != "":
    video_command0="ffmpeg -i input/interview.mkv -vf \"select=\'"\
                  +video_channel0_str[1:]+"\',setpts=N/FRAME_RATE/TB\" -af \"aselect=\'"+ \
                  video_channel0_str[1:]+"\',asetpts=N/SR/TB\" output/video_channel0.mp4"
    subprocess.call(video_command0,shell=True)

if video_channel1_str != "":
    video_command1="ffmpeg -i input/interview.mkv -vf \"select=\'"\
                  +video_channel1_str[1:]+"\',setpts=N/FRAME_RATE/TB\" -af \"aselect=\'"+ \
                  video_channel1_str[1:]+"\',asetpts=N/SR/TB\" output/video_channel1.mp4"
    subprocess.call(video_command1,shell=True)

if video_channel2_str != "":
    video_command2="ffmpeg -i input/interview.mkv -vf \"select=\'"\
                  +video_channel2_str[1:]+"\',setpts=N/FRAME_RATE/TB\" -af \"aselect=\'"+ \
                  video_channel2_str[1:]+"\',asetpts=N/SR/TB\" output/video_channel2.mp4"
    subprocess.call(video_command2,shell=True)

if video_channel3_str != "":
    video_command3="ffmpeg -i input/interview.mkv -vf \"select=\'"\
                  +video_channel3_str[1:]+"\',setpts=N/FRAME_RATE/TB\" -af \"aselect=\'"+ \
                  video_channel3_str[1:]+"\',asetpts=N/SR/TB\" output/video_channel3.mp4"
    subprocess.call(video_command3,shell=True)
