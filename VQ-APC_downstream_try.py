import librosa, pickle
import os
import argparse

import torch
import torch.nn.functional as F

from vqapc_model import GumbelAPCModel


wav_path = './wavs/combined_sounds_shuffled.wav'


'''
    mel spectrogram - 80-dimensional
'''

x, sr = librosa.load(wav_path, sr=44100)
mel_per_wav = librosa.feature.melspectrogram(x, sr=sr, n_mels=80).T
print("for wav file " + wav_path + ", mfcc shape:")
print(mel_per_wav.shape)

n = len(mel_per_wav)
f = open('mel_spectrogram.txt' , 'w')
for i in range(n):
    for item in mel_per_wav[i]:
        f.write(str(item) + ' ')
    f.write('\n')
f.close()


'''
    prepare data - following APC pipeline
'''

max_seq_len = 1600
save_dir = './preprocessed'
utt_id = 'combined_sounds_shuffled'

id2len = {}
with open('mel_spectrogram.txt', 'r') as f:
    # process the file line by line
    log_mel = []

    for line in f:
        data = line.strip().split()
        log_mel.append([float(i) for i in data])

    id2len[utt_id + '.pt'] = min(len(log_mel), max_seq_len)
    log_mel = torch.FloatTensor(log_mel)  # convert the 2D list to a pytorch tensor
    log_mel = F.pad(log_mel, (0, 0, 0, max_seq_len - log_mel.size(0))) # pad or truncate
    torch.save(log_mel, os.path.join(save_dir, utt_id + '.pt'))

with open(os.path.join(save_dir, 'lengths.pkl'), 'wb') as f:
    pickle.dump(id2len, f, protocol=4)


'''
    loading pretrained model
'''

pretrained_vqapc = GumbelAPCModel(input_size=80,
                     hidden_size=512,
                     num_layers=3,
                     dropout=0.1,
                     residual=' ',
                     codebook_size=128,
                     code_dim=512,
                     gumbel_temperature=0.5,
                     vq_hidden_size=-1,
                     apply_VQ=0 0 1).cuda()

pretrained_weights_path = './log/jan-30_run1.dir/jan-30_run1__epoch_9.model'
pretrained_vqapc.load_state_dict(torch.load(pretrained_weights_path))