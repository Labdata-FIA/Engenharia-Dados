with customer as (select * from {{ ref('stg_customer') }}),

final as (
    select
        customerkey as customer_key,
        lastname as last_name,
        firstname as first_name,
        concat(firstname, ' ', lastname) as full_name,
        prefix,
        emailaddress as email_address,
        occupation,
        case 
            when cast(birthdate as string) = '' or birthdate is null then null  
            else to_date(birthdate)
        end as birth_date,
        gender,
        maritalstatus as maritial_status,
        totalchildren as total_children,
        educationlevel as education_level,
        homeowner as home_owner,
        cast(annualincome as float) as annual_income
    from customer
)

select
    *
from final