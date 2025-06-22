with territory as (select * from {{ ref('stg_territory') }}),

final as (
    select
        salesterritorykey as sales_territory_key,
        region,
        country,
        continent
    from territory
)

select
    *
from final