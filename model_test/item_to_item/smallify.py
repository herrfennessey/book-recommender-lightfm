import polars as pl

precomputed_recs = pl.read_parquet("item_to_item_precomputed.parquet")
filtered_df = precomputed_recs.filter(pl.col("work_id") == "21580644")
filtered_df.write_parquet("smaller.parquet")
