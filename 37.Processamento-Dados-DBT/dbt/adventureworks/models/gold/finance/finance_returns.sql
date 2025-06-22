with returns as ( select * from {{ ref('fact_returns') }} ),
products as ( select * from {{ ref('dim_product') }} )

select
    year(return_date) as year,
    month(return_date) as month,
    sum(return_quantity) as total_quantity_returned,
    sum(return_quantity * p.product_price) as total_returns_amount
from returns r
join products p on r.product_key = p.product_key
group by year, month
order by year, month