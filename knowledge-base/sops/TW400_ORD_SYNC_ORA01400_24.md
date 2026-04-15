# SOP: TW400_ORD_SYNC – ORA-01400 Cannot Insert NULL

## Batch Name
TW400_ORD_SYNC

## Error Code
ORA-01400

## Error Pattern
ORA-01400: error occurred in batch processing

## Tags
TW400_ORD_SYNC, TW400, ORA-01400, batch failure

## Description
This error occurs in batch TW400_ORD_SYNC due to cannot insert null.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-01400 and rerun the batch.

## Steps to Resolve

### Step 1: Check logs
/apps/logs/TW400_ORD_SYNC_*.log

### Step 2: Identify issue
SELECT * FROM error_table WHERE batch = 'TW400_ORD_SYNC';

### Step 3: Fix data issue
- Correct data inconsistencies
- Insert missing records if needed

### Step 4: Re-run batch
Re-run TW400_ORD_SYNC from scheduler.

## Validation
- Batch completes successfully
- No ORA-01400 error

## Category
Oracle Batch Failure
