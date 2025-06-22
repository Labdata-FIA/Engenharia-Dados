with product_categories as (select * from {{ ref('stg_product_categories') }}),

final as (
    select
        productcategorykey as product_category_key,
        categoryname as category_name
    from product_categories
)

select
    *
from final