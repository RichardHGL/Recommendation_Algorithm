#!/bin/sh
./reconstruct -train ../train_graph -output train_graph_dense.txt -depth 2 -k-max 1000
./line -train train_graph_dense.txt -output vec_1st_wo_norm.txt -binary 1 -size 128 -order 1 -negative 5 -samples 10000 -threads 40
./line -train train_graph_dense.txt -output vec_2nd_wo_norm.txt -binary 1 -size 128 -order 2 -negative 5 -samples 10000 -threads 40
./normalize -input vec_1st_wo_norm.txt -output vec_1st.txt -binary 0
./normalize -input vec_2nd_wo_norm.txt -output vec_2nd.txt -binary 0
./b2n -input vec_1st_wo_norm.txt -output vec_1st_unnormal -binary 0
./b2n -input vec_2nd_wo_norm.txt -output vec_2nd_unnormal -binary 0
python vec_deal.py vec_1st.txt ../testset.txt res_1st
python vec_deal.py vec_2nd.txt ../testset.txt res_2nd
python vec_deal.py vec_1st_unnormal ../testset.txt res_1st_unnormal
python vec_deal.py vec_2nd_unnormal ../testset.txt res_2nd_unnormal