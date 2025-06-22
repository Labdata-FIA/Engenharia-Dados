with product as (select * from {{ ref('stg_product') }}),

final as (
    select
        productkey as product_key,
        productsku as product_sku,
        productsubcategorykey as product_subcategory_key,
        productname as product_name,
        modelname as model_name,
        productsize as product_size,
        productcolor as product_color,
        productstyle as product_style,
        productdescription as product_description,
        round(productprice, 2) as product_price,
        round(productcost, 2) as product_cost,
        round(productprice - productcost, 2) as product_profit
    from product
)

select
    *
from final