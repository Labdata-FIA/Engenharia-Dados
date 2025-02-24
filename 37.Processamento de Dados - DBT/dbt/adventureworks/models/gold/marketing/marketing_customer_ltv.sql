with sales as ( select * from {{ ref('fact_sales') }} ),

customers as ( select * from {{ ref('dim_customer') }} )

select
    c.customer_key,
    c.full_name,
    sum(s.order_quantity * p.product_price) as lifetime_value
from sales s
join customers c on s.customer_key = c.customer_key
join {{ ref('dim_product') }} p on s.product_key = p.product_key
group by c.customer_key, c.full_name
order by lifetime_value desc