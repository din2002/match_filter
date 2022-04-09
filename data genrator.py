import librosa
import os
import random
import soundfile as sf

# TODO:: typos in docstring
class DataGenrator():
    """
        Class will be used to genrate dataset for different speakers

        Attributes: 
            dataset: it will store dataset genrated from last genrate call or None
            sample_rate: it will store sample rate of sound sapmle or None
    """
    dataset = None
    sample_rate = None


    def __init__(self, background_folder_path, speakers_folder_path):
        """
            Creates Data for training model from background noise and speakers audio

            Arguments:
            background_folder_path: Path to the folder containing background audio file with .wav format atleast of 10 sec length
            speaker_folder_path: Path to the folder containing speakers folder containg their audio with .wav format atleast of 2 sec length

            Return:
            Void
        """
        self._background_folder_path = background_folder_path
        self._speakers_folder_path = speakers_folder_path
        self._speakers = []
        for i in os.listdir(self._speakers_folder_path):
            if os.path.isdir(os.path.join(self._speakers_folder_path, i)):
                self._speakers.append(i)
        assert(len(self._speakers) != 0)

    def random_time_segment(self):
        """
            Generates random position where speaker clip will be imposed 

            Arguments:
                None
            return:
                time_segment: tuple of start and end index of time segment (start, end)
        """
        start = random.randint(0, self.sample_rate * 8)
        end = start + 2 * self.sample_rate
        return (start, end)

    def insert_clip(self, background, speaker, time_segment):
        """
            Inserts the speaker clip in bacground for given time segment

            Arguments:
                background: a 10 sec audio file converted to numpy array
                speaker: a 2 sec audio file converted to numpy array 
                time_segment: tuple of start and end index of time segment (start, end)
            Return:
                background: background clip with added speaker sound in clip duration
        """
        background[time_segment[0]:time_segment[1]] += speaker
        return background
    
    def insert_ones(self, y: list, time_segment: tuple, error_tolurance: int):
        """
            It will add 1 where speakers sound is present it will also plus error tolarnce

            Arguments:
                y: Ground truth list 
                time_segment: tuple of start and end index of time segment (start, end)
                error_tolurance: number of 1 to be added after speakers clip ends
            Returns:
                y: ground truth list with 1's added in time segment  
        """
        for i in range(time_segment[0], time_segment[1]+error_tolurance):
            y[i] = 1
        return y
    
    def generate_example(self, background, speaker, others):
        """
            It generates example for a given speaker, background and others

            Arguments:
                background(str): name of background file
                speaker(str): name of speaker
                others(list): name of other speaker
            Return:
                audio_clip: numpy array representing ausio file
                y: ground truth 
        """
        y = [0 for i in range(self.sample_rate*10)]
        number_of_speaker_clips = random.randint(1, 3)
        number_of_other_speaker_clips = random.randint(0, 3)

        speaker_clip_time_segments = [self.random_time_segment() for i in range(number_of_speaker_clips)]
        other_speaker_clip_time_segments = [self.random_time_segment() for i in range(number_of_other_speaker_clips)]

        speaker_clips = [i for i in os.listdir( os.path.join(self._speakers_folder_path, speaker))]
        #TODO:: to make code others clip appendable in background

        # TODO:: add more sample to raw_data
        speaker_clips = random.sample(speaker_clips, 1)
        speaker_clips = [librosa.load(os.path.join(self._speakers_folder_path, speaker, i))[0][:2*self.sample_rate] for i in speaker_clips]

        background, self.sample_rate = librosa.load(os.path.join(self._background_folder_path, background))
        background = background[:10*self.sample_rate]

        print(type(background), speaker_clips, speaker_clip_time_segments)
        for i in range(1):
            print(f"start: {speaker_clip_time_segments[i][0]/self.sample_rate} end: {speaker_clip_time_segments[i][1]/self.sample_rate}")
            background = self.insert_clip(background, speaker_clips[i], speaker_clip_time_segments[i])
            y = self.insert_ones(y, speaker_clip_time_segments[i], 150)

        return background, y
    
    # TODO:: implement
    def generate_dataset(self, speaker :str, number:int, other_speaker :bool = True):
        """
            It generates dataset for a given speaker and saves dataset in dataset attributes

            Arguments:
                speaker(str): name of speaker
                number(int): number of example to be genrated
                other_speaker(bool): default True
            Return:
                void   
        """
        pass


dataGenrator = DataGenrator('./raw_data/background', './raw_data/speaker')
temp, dataGenrator.sample_rate = librosa.load('raw_data/background/1.wav')
audio, y=  dataGenrator.generate_example('1.wav', 'narendra modi', '')
print(len(audio))
print(len(y))

sf.write('./audio.wav', audio, dataGenrator.sample_rate)





        
    
    