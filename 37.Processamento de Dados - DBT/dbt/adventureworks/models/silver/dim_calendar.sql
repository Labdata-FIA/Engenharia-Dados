with calendar as (select * from {{ ref('stg_calendar') }}),

final as (
    select
        to_date(date) as date,
        year(to_date(date)) as year,
        month(to_date(date)) as month,
        day(to_date(date)) as day
    from calendar
)

select
    *
from final