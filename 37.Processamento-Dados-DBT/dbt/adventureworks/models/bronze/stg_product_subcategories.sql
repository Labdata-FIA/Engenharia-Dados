with 
source as (select * from {{ source('adventureworks', 'adventureworks_product_subcategories_lookup') }})

select 
  * 
from source