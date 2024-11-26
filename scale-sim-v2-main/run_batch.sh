# server_google_tpu_os
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/lenet.csv -p output/lenet
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/alexnet.csv -p output/alexnet
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/mobilenet.csv -p output/mobilenet
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/Resnet18.csv -p output/resnet18
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/Googlenet.csv -p output/Googlenet
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/dlrm/DLRM.csv -p output/DLRM
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/mlperf/AlphaGoZero.csv -p output/AlphaGoZero
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/mlperf/DeepSpeech2.csv -p output/DeepSpeech2
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/mlperf/FasterRCNN.csv -p output/FasterRCNN
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/mlperf/NCF_recommendation.csv -p output/NCF_recommendation
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/mlperf/Sentimental_seqCNN.csv -p output/Sentimental_seqCNN
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/transformer/transformer_fwd.csv -p output/transformer_fwd
python3 scalesim/scale.py -c configs/server_google_tpu_v1.cfg -t topologies/conv_nets/yolo_tiny.csv -p output/yolo_tiny

# edge_samsung_exynos_os
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/lenet.csv -p output/lenet
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/alexnet.csv -p output/alexnet
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/mobilenet.csv -p output/mobilenet
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/Resnet18.csv -p output/resnet18
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/Googlenet.csv -p output/Googlenet
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/dlrm/DLRM.csv -p output/DLRM
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/mlperf/AlphaGoZero.csv -p output/AlphaGoZero
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/mlperf/DeepSpeech2.csv -p output/DeepSpeech2
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/mlperf/FasterRCNN.csv -p output/FasterRCNN
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/mlperf/NCF_recommendation.csv -p output/NCF_recommendation
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/mlperf/Sentimental_seqCNN.csv -p output/Sentimental_seqCNN
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/transformer/transformer_fwd.csv -p output/transformer_fwd
python3 scalesim/scale.py -c configs/edge_samsung_exynos.cfg -t topologies/conv_nets/yolo_tiny.csv -p output/yolo_tiny