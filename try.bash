CUDA_VISIBLE_DEVICES=1 python VQ-APC_downstream_try.py --exp_name=combined_sounds_shuffled \
--sound_file=./wavs/combined_sounds_shuffled.wav \
--pretrained_weights=./logs/feb-3_vqextract_trial1.dir/feb-3_vqextract_trial1__epoch_1.model \
--pretrained_VQ=./logs/feb-4_vqextract.dir/feb-4_vqextract-VQlayers__epoch_1.model 
