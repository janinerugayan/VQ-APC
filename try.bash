CUDA_VISIBLE_DEVICES=1 python VQ-APC_downstream_try.py --exp_name=combined_sounds_shuffled \
--sound_file=./wavs/combined_sounds_shuffled.wav \
--pretrained_weights=./logs/feb-2_run1.dir/feb-2_run1__epoch_10.model
