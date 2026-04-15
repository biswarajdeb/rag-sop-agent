# SOP: TW100_INV_LOAD – ORA-00001 Unique Constraint Violation

## Batch Name
TW100_INV_LOAD

## Error Code
ORA-00001

## Error Pattern
ORA-00001: error occurred in batch processing

## Tags
TW100_INV_LOAD, TW100, ORA-00001, batch failure

## Description
This error occurs in batch TW100_INV_LOAD due to unique constraint violation.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-00001 and rerun the batch.

## Steps to Resolve

### Step 1: Check logs
/apps/logs/TW100_INV_LOAD_*.log

### Step 2: Identify issue
SELECT * FROM error_table WHERE batch = 'TW100_INV_LOAD';

### Step 3: Fix data issue
- Correct data inconsistencies
- Insert missing records if needed

### Step 4: Re-run batch
Re-run TW100_INV_LOAD from scheduler.

## Validation
- Batch completes successfully
- No ORA-00001 error

## Category
Oracle Batch Failure
