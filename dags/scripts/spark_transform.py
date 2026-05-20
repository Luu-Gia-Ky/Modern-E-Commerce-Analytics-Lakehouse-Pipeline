import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp, to_timestamp

def main():
    # 1. Khởi tạo Spark Session với JDBC Driver để ghi vào Postgres sau này
    spark = SparkSession.builder \
        .appName("Ecommerce-Silver-Transformation") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("WARN")
    
    bronze_path = "/opt/airflow/data/bronze/*.json"
    silver_parquet_path = "/opt/airflow/data/silver/orders"
    
    print(f" Reading raw data from: {bronze_path}")
    df_raw = spark.read.option("multiLine", True).json(bronze_path)
    
    # 2. DATA CLEANING & DEFENSIVE ENGINEERING
    # Lọc bỏ bản ghi lỗi (Price <= 0), chuẩn hóa trạng thái thành viết hoa
    df_cleaned = df_raw.filter(col("price") > 0) \
                       .withColumn("status", when(col("status") == "pending", "PENDING")
                                            .when(col("status") == "completed", "COMPLETED")
                                            .otherwise(col("status"))) \
                       .withColumn("order_date", to_timestamp(col("order_date"), "yyyy-MM-dd HH:mm:ss")) \
                       .withColumn("updated_at", to_timestamp(col("updated_at"), "yyyy-MM-dd HH:mm:ss")) \
                       .withColumn("ingested_at", current_timestamp())
                       
    # 3. LƯU DỰ LIỆU XUỐNG DẠNG PARQUET (Tối ưu hóa Data Lake)
    # Ghi đè (Overwrite) hoặc Append tùy thuộc vào chiến lược bài toán
    print(f" Writing cleaned data to Parquet at: {silver_parquet_path}")
    df_cleaned.write.mode("overwrite").parquet(silver_parquet_path)
    
    # 4. LOAD VÀO POSTGRES (Giai đoạn chuyển tiếp sang Warehouse)
    print(" Loading data into PostgreSQL raw schema...")
    df_cleaned.drop("ingested_at").write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/ecommerce_dw") \
        .option("dbtable", "raw.orders") \
        .option("user", "warehouse_user") \
        .option("password", "warehouse_password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
        
    spark.stop()

if __name__ == "__main__":
    main()