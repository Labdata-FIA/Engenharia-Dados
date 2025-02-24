with product_subcategories as (select * from {{ ref('stg_product_subcategories') }}),

final as (
    select
        productcategorykey as product_category_key,
        productsubcategorykey as product_subcategory_key,
        subcategoryname as subcategory_name
    from product_subcategories
)

select
    *
from final