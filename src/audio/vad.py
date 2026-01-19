import numpy as np;

def calculate_rms(audio_chunk):

    {/*root mean square calculate kara rha mtlb loudness of sound*/}

    data=np.frombuffer(audio_chunk,dtype=np.int16)

    if len(data)==0:
        return 0 
    
    return np.sqrt(np.mean(data**2))

