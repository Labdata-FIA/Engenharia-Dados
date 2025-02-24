with 
source as (select * from {{ source('adventureworks', 'adventureworks_calendar_lookup') }})

select 
  * 
from source