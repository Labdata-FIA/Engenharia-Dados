with sales as ( select * from {{ ref('fact_sales') }} ),

products as ( select * from {{ ref('dim_product') }} )

select
    year(order_date) as year,
    month(order_date) as month,
    sum(order_quantity) as total_quantity_sold,
    sum(order_quantity * p.product_price) as total_sales_amount
from sales s
join products p on s.product_key = p.product_key
group by year, month
order by year, month