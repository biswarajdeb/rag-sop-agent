# SOP: TW100_CUST_LOAD – ORA-02291 Foreign Key Violation

## Batch Name
TW100_CUST_LOAD

## Error Code
ORA-02291

## Error Pattern
ORA-02291: error occurred in batch processing

## Tags
TW100_CUST_LOAD, TW100, ORA-02291, batch failure

## Description
This error occurs in batch TW100_CUST_LOAD due to foreign key violation.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-02291 and rerun the batch.

## Steps to Resolve

### Step 1: Check logs
/apps/logs/TW100_CUST_LOAD_*.log

### Step 2: Identify issue
SELECT * FROM error_table WHERE batch = 'TW100_CUST_LOAD';

### Step 3: Fix data issue
- Correct data inconsistencies
- Insert missing records if needed

### Step 4: Re-run batch
Re-run TW100_CUST_LOAD from scheduler.

## Validation
- Batch completes successfully
- No ORA-02291 error

## Category
Oracle Batch Failure
