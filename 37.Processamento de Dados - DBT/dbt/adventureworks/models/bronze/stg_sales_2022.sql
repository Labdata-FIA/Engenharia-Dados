with 
source as (select * from {{ source('adventureworks', 'adventureworks_sales_data_2022') }})

select 
  * 
from source