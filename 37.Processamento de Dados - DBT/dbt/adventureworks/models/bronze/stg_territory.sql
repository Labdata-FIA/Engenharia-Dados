with 
source as (select * from {{ source('adventureworks', 'adventureworks_territory_lookup') }})

select 
  * 
from source