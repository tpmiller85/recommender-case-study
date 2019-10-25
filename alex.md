**Table 1**: Modeling Methods and results

| Movielens(100k)	| RMSE | Time |
|---:|-----------:|----:|
|GlobalMean|1.126|0:00:01|
|MeanofMeans|	1.017	|	0:00:01|
|ALS_Surprise|	0.944|	0:00:01|
|ALS_Spark| 0.92| 0:00:03|
<!-- |SVD	|0.937|0:00:16|
|NMF|	0.964|0:00:17|
|SlopeOne|	0.946|0:00:13|
|k-NN|	0.98|0:00:13|
|k-NN Means|0.951|0:00:13|
|k-NN Baseline	|0.931|	0:00:16|
|Co-Clustering	|0.962|	0:00:06|
|NormalPredictor|	1.519|0:00:01| -->


| Movielens(1M)	| RMSE | Time |
|---:|-----------:|----:|
|MeanofMeans|1.126|0:00:08|
|ALS_Surprise|	0.944|	0:00:05|
|ALS_Spark| 0.92| 0:00:02|