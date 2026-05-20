{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'COMPLETED'
)

select
    cast(order_timestamp as date) as sales_date,
    product_id,
    count(distinct order_id) as total_orders,
    sum(quantity) as total_units_sold,
    sum(total_amount) as total_revenue
from orders
group by 1, 2