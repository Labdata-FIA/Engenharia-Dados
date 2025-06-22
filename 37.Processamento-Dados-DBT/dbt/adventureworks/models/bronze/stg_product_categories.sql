with 
source as (select * from {{ source('adventureworks', 'adventureworks_product_categories_lookup') }})

select 
  * 
from source