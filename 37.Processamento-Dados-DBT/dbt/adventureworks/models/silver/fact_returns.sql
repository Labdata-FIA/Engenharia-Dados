with returns as (select * from {{ ref('stg_returns') }}),

final as (
    select
        productkey as product_key,
        territorykey as territory_key,
        to_date(returndate) as return_date,
        cast(returnquantity as int) as return_quantity
    from returns
)

select
    *
from final