# SOP: TW300_PAY_PROC – ORA-00001 Unique Constraint Violation

## Batch Name
TW300_PAY_PROC

## Error Code
ORA-00001

## Error Pattern
ORA-00001: error occurred in batch processing

## Tags
TW300_PAY_PROC, TW300, ORA-00001, batch failure

## Description
This error occurs in batch TW300_PAY_PROC due to unique constraint violation.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-00001 and rerun the batch.

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
- No ORA-00001 error

## Category
Oracle Batch Failure
