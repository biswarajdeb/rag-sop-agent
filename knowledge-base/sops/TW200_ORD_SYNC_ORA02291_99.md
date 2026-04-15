# SOP: TW200_ORD_SYNC – ORA-02291 Foreign Key Violation

## Batch Name
TW200_ORD_SYNC

## Error Code
ORA-02291

## Error Pattern
ORA-02291: error occurred in batch processing

## Tags
TW200_ORD_SYNC, TW200, ORA-02291, batch failure

## Description
This error occurs in batch TW200_ORD_SYNC due to foreign key violation.

## Root Cause
- Data inconsistency
- Upstream dependency failure
- Incorrect data mapping

## Resolution Summary
Fix the issue causing ORA-02291 and rerun the batch.

## Steps to Resolve

### Step 1: Check logs
/apps/logs/TW200_ORD_SYNC_*.log

### Step 2: Identify issue
SELECT * FROM error_table WHERE batch = 'TW200_ORD_SYNC';

### Step 3: Fix data issue
- Correct data inconsistencies
- Insert missing records if needed

### Step 4: Re-run batch
Re-run TW200_ORD_SYNC from scheduler.

## Validation
- Batch completes successfully
- No ORA-02291 error

## Category
Oracle Batch Failure
