with 
source as (select * from {{ source('adventureworks', 'adventureworks_sales_data_2020') }})

select 
  * 
from source