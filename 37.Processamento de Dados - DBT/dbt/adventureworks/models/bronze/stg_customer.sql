with 
source as (select * from {{ source('adventureworks', 'adventureworks_customer_lookup') }})

select 
  * 
from source