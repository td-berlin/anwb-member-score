import pandas as pd


def transform_to_rfm(file_path: str) -> None:
    data = pd.read_parquet(file_path)
    data["date"] = pd.to_datetime(data["date"])
    analysis_date = data["date"].max()
    rfm = data.groupby("id").agg(
        {
            "date": [lambda x: (x.max() - x.min()).days, lambda x: (analysis_date - x.min()).days],
            "id": "count",
            "spent": "mean",
        }
    )
    rfm.columns = ["recency", "T", "frequency", "monetary_value"]
    rfm = rfm.reset_index()
    rfm.rename(columns={"id": "customer_id"}, inplace=True)
    rfm["frequency"] = rfm["frequency"] - 1
    rfm = rfm[rfm["frequency"] > 0]
    rfm.to_parquet("data/rfm_data/rfm_df.parquet")


if __name__ == "__main__":
    file_path = "notebooks/mock_data.parquet"
    transform_to_rfm(file_path)
    print("Data Transformed")
