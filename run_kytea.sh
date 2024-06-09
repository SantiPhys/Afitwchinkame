# Training commands for L2 regularized SVM (default solver in KyTea)
train-kytea -full data/1_kaiju_corpus.full -model models/1_kaiju_model_L2SVM.dat &
train-kytea -full data/2_kaiju_corpus.full -model models/2_kaiju_model_L2SVM.dat &
train-kytea -full data/3_kaiju_corpus.full -model models/3_kaiju_model_L2SVM.dat &
train-kytea -full data/4_kaiju_corpus.full -model models/4_kaiju_model_L2SVM.dat &
train-kytea -full data/5_kaiju_corpus.full -model models/5_kaiju_model_L2SVM.dat &
train-kytea -full data/6_kaiju_corpus.full -model models/6_kaiju_model_L2SVM.dat &
train-kytea -full data/7_kaiju_corpus.full -model models/7_kaiju_model_L2SVM.dat &
train-kytea -full data/8_kaiju_corpus.full -model models/8_kaiju_model_L2SVM.dat &
train-kytea -full data/9_kaiju_corpus.full -model models/9_kaiju_model_L2SVM.dat &

# Training commands for L1 regularized SVM
train-kytea -full data/1_kaiju_corpus.full -solver 5 -model models/1_kaiju_model_L1SVM.dat &
train-kytea -full data/2_kaiju_corpus.full -solver 5 -model models/2_kaiju_model_L1SVM.dat &
train-kytea -full data/3_kaiju_corpus.full -solver 5 -model models/3_kaiju_model_L1SVM.dat &
train-kytea -full data/4_kaiju_corpus.full -solver 5 -model models/4_kaiju_model_L1SVM.dat &
train-kytea -full data/5_kaiju_corpus.full -solver 5 -model models/5_kaiju_model_L1SVM.dat &
train-kytea -full data/6_kaiju_corpus.full -solver 5 -model models/6_kaiju_model_L1SVM.dat &
train-kytea -full data/7_kaiju_corpus.full -solver 5 -model models/7_kaiju_model_L1SVM.dat &
train-kytea -full data/8_kaiju_corpus.full -solver 5 -model models/8_kaiju_model_L1SVM.dat &
train-kytea -full data/9_kaiju_corpus.full -solver 5 -model models/9_kaiju_model_L1SVM.dat &


# Wait for all training commands to finish
wait

# Prediction commands for L2SVM
kytea -model models/1_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/1_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/2_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/2_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/3_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/3_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/4_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/4_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/5_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/5_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/6_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/6_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/7_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/7_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/8_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/8_kaiju_L2SVM_king_kong_pred.full &
kytea -model models/9_kaiju_model_L2SVM.dat < data/king_kong_eval.2char > data/9_kaiju_L2SVM_king_kong_pred.full &

# Prediction commands for L1SVM
kytea -model models/1_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/1_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/2_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/2_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/3_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/3_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/4_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/4_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/5_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/5_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/6_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/6_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/7_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/7_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/8_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/8_kaiju_L1SVM_king_kong_pred.full &
kytea -model models/9_kaiju_model_L1SVM.dat < data/king_kong_eval.2char > data/9_kaiju_L1SVM_king_kong_pred.full &

# Wait for all prediction commands to finish
wait
