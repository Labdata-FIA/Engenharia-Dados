with 
source as (select * from {{ source('adventureworks', 'adventureworks_sales_data_2021') }})

select 
  * 
from source