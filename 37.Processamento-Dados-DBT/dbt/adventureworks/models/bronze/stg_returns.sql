with 
source as (select * from {{ source('adventureworks', 'adventureworks_returns_data') }})

select 
  * 
from source