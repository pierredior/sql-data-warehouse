-- This file contains the SQLite-compatible transformation scripts for the Silver layer.

-- Empty the silver tables before loading new data
DELETE FROM silver_crm_cust_info;
DELETE FROM silver_crm_prd_info;
DELETE FROM silver_crm_sales_details;
DELETE FROM silver_erp_cust_az12;
DELETE FROM silver_erp_loc_a101;
DELETE FROM silver_erp_px_cat_g1v2;

-- Load silver.crm_cust_info
INSERT INTO silver_crm_cust_info (
    cst_id, cst_key, cst_firstname, cst_lastname, cst_marital_status, cst_gndr, cst_create_date
)
SELECT
    cst_id,
    cst_key,
    TRIM(cst_firstname),
    TRIM(cst_lastname),
    CASE 
        WHEN UPPER(TRIM(cst_marital_status)) = 'S' THEN 'Single'
        WHEN UPPER(TRIM(cst_marital_status)) = 'M' THEN 'Married'
        ELSE 'n/a'
    END,
    CASE 
        WHEN UPPER(TRIM(cst_gndr)) = 'F' THEN 'Female'
        WHEN UPPER(TRIM(cst_gndr)) = 'M' THEN 'Male'
        ELSE 'n/a'
    END,
    cst_create_date
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY cst_id ORDER BY cst_create_date DESC) as flag_last
    FROM bronze_crm_cust_info
    WHERE cst_id IS NOT NULL
) t
WHERE flag_last = 1;

-- Load silver.crm_prd_info
INSERT INTO silver_crm_prd_info (
    prd_id, cat_id, prd_key, prd_nm, prd_cost, prd_line, prd_start_dt, prd_end_dt
)
SELECT
    prd_id,
    REPLACE(SUBSTR(prd_key, 1, 5), '-', '_'),
    SUBSTR(prd_key, 7, LENGTH(prd_key)),
    prd_nm,
    IFNULL(prd_cost, 0),
    CASE 
        WHEN UPPER(TRIM(prd_line)) = 'M' THEN 'Mountain'
        WHEN UPPER(TRIM(prd_line)) = 'R' THEN 'Road'
        WHEN UPPER(TRIM(prd_line)) = 'S' THEN 'Other Sales'
        WHEN UPPER(TRIM(prd_line)) = 'T' THEN 'Touring'
        ELSE 'n/a'
    END,
    DATE(prd_start_dt),
    DATE(LEAD(prd_start_dt) OVER (PARTITION BY prd_key ORDER BY prd_start_dt), '-1 day')
FROM bronze_crm_prd_info;

-- Load crm_sales_details
INSERT INTO silver_crm_sales_details (
    sls_ord_num, sls_prd_key, sls_cust_id, sls_order_dt, sls_ship_dt, sls_due_dt, sls_sales, sls_quantity, sls_price
)
SELECT 
    sls_ord_num,
    sls_prd_key,
    sls_cust_id,
    CASE 
        WHEN sls_order_dt = 0 OR LENGTH(CAST(sls_order_dt AS TEXT)) != 8 THEN NULL
        ELSE SUBSTR(sls_order_dt, 1, 4) || '-' || SUBSTR(sls_order_dt, 5, 2) || '-' || SUBSTR(sls_order_dt, 7, 2)
    END,
    CASE 
        WHEN sls_ship_dt = 0 OR LENGTH(CAST(sls_ship_dt AS TEXT)) != 8 THEN NULL
        ELSE SUBSTR(sls_ship_dt, 1, 4) || '-' || SUBSTR(sls_ship_dt, 5, 2) || '-' || SUBSTR(sls_ship_dt, 7, 2)
    END,
    CASE 
        WHEN sls_due_dt = 0 OR LENGTH(CAST(sls_due_dt AS TEXT)) != 8 THEN NULL
        ELSE SUBSTR(sls_due_dt, 1, 4) || '-' || SUBSTR(sls_due_dt, 5, 2) || '-' || SUBSTR(sls_due_dt, 7, 2)
    END,
    CASE 
        WHEN sls_sales IS NULL OR sls_sales <= 0 OR sls_sales != sls_quantity * ABS(sls_price) 
            THEN sls_quantity * ABS(sls_price)
        ELSE sls_sales
    END,
    sls_quantity,
    CASE 
        WHEN sls_price IS NULL OR sls_price <= 0 
            THEN sls_sales / CASE WHEN sls_quantity = 0 THEN NULL ELSE sls_quantity END
        ELSE sls_price
    END
FROM bronze_crm_sales_details;

-- Load erp_cust_az12
INSERT INTO silver_erp_cust_az12 (cid, bdate, gen)
SELECT
    CASE
        WHEN cid LIKE 'NAS%' THEN SUBSTR(cid, 4, LENGTH(cid))
        ELSE cid
    END, 
    CASE
        WHEN DATE(bdate) > CURRENT_DATE THEN NULL
        ELSE bdate
    END,
    CASE
        WHEN UPPER(TRIM(gen)) IN ('F', 'FEMALE') THEN 'Female'
        WHEN UPPER(TRIM(gen)) IN ('M', 'MALE') THEN 'Male'
        ELSE 'n/a'
    END
FROM bronze_erp_cust_az12;

-- Load erp_loc_a101
INSERT INTO silver_erp_loc_a101 (cid, cntry)
SELECT
    REPLACE(cid, '-', ''), 
    CASE
        WHEN TRIM(cntry) = 'DE' THEN 'Germany'
        WHEN TRIM(cntry) IN ('US', 'USA') THEN 'United States'
        WHEN TRIM(cntry) = '' OR cntry IS NULL THEN 'n/a'
        ELSE TRIM(cntry)
    END
FROM bronze_erp_loc_a101;

-- Load erp_px_cat_g1v2
INSERT INTO silver_erp_px_cat_g1v2 (id, cat, subcat, maintenance)
SELECT id, cat, subcat, maintenance FROM bronze_erp_px_cat_g1v2;