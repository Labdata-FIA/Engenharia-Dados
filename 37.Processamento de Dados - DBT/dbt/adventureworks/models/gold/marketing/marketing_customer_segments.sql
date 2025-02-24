with customers as ( select * from {{ ref('dim_customer') }} )

select
    case
        when annual_income < 50000 then 'Low Income'
        when annual_income between 50000 and 100000 then 'Middle Income'
        else 'High Income'
    end as income_segment,
    count(distinct customer_key) as total_customers
from customers
group by income_segment
order by income_segment