with 
source as (select * from {{ source('adventureworks', 'adventureworks_product_lookup') }})

select 
  * 
from source