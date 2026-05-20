{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        user_id,
        cast(order_date as timestamp) as order_timestamp,
        product_id,
        quantity,
        price,
        -- Tính toán diễn giải thêm để thể hiện tư duy phân tích
        (quantity * price) as total_amount,
        upper(status) as order_status,
        updated_at
    from source
)

select * from renamed