with sales_2020 as (select * from {{ ref('stg_sales_2020') }}),

sales_2021 as (select * from {{ ref('stg_sales_2021') }}),

sales_2022 as (select * from {{ ref('stg_sales_2022') }}),

all_sales as (
    select
        *
    from stg_sales_2020
    union
    select
        *
    from stg_sales_2021
    union
    select
        *
    from stg_sales_2022
),

final as (
    select
        productkey as product_key,
        customerkey as customer_key,
        territorykey as territory_key,
        ordernumber as order_number,
        orderlineitem as order_line_item,
        to_date(orderdate) as order_date,
        to_date(stockdate) as stock_date,
        cast(orderquantity as int) as order_quantity
    from all_sales
)

select
    *
from final