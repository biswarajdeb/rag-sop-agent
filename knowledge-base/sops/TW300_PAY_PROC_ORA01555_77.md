# SOP: TW300_PAY_PROC – ORA-01555 Snapshot Too Old

## Batch Name
TW300_PAY_PROC

## Error Code
ORA-01555

## Error Pattern
ORA-01555: error occurred in batch processing

## Tags
TW300_PAY_PROC, TW300, ORA-01555, batch failure

## Description
This error occurs in batch TW300_PAY_PROC due to snapshot too old.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-01555 and rerun the batch.

## Steps to Resolve

### Step 1: Check logs
/apps/logs/TW300_PAY_PROC_*.log

### Step 2: Identify issue
SELECT * FROM error_table WHERE batch = 'TW300_PAY_PROC';

### Step 3: Fix data issue
- Correct data inconsistencies
- Insert missing records if needed

### Step 4: Re-run batch
Re-run TW300_PAY_PROC from scheduler.

## Validation
- Batch completes successfully
- No ORA-01555 error

## Category
Oracle Batch Failure
