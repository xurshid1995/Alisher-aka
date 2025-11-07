# Store/Warehouse ID Collision Fix - Complete

## Problem Summary
User reported: "Sotuvchiga 2 ta joylashuv ruxsat berdim, lekin 3 ta ko'rsatilmoqda"
- sotuvchi user was assigned 2 locations but saw 3 locations
- Root cause: Store ID=1 and Warehouse ID=1 overlapped

## Root Cause Analysis
1. **Original Data:**
   - Store ID=1: Sergeli 1/4/3
   - Warehouse ID=1: UY Sergeli
   - Warehouse ID=2: Akfa

2. **Migration Issue:**
   - `migrate_allowed_locations.py` converted old format `[1, 2]` to new format
   - ID=1 found in BOTH stores and warehouses tables
   - Result: Created 3 entries instead of 2:
     * `{'id': 1, 'type': 'store'}` - Sergeli 1/4/3
     * `{'id': 1, 'type': 'warehouse'}` - UY Sergeli (UNWANTED)
     * `{'id': 2, 'type': 'warehouse'}` - Akfa

## Solution Implemented
**Variant 1: Separate ID ranges**
- Stores: ID starts from 1
- Warehouses: ID starts from 1001

### Steps Executed

1. **Database Backup** ✅
   - Created backup before structural changes
   - File: `/tmp/dokon_db_backup_*.sql` (29K)

2. **Recreate Warehouses with New IDs** ✅
   - Created `recreate_warehouses.py`
   - Warehouse ID=1001: UY Sergeli
   - Warehouse ID=1002: Akfa
   - Set auto-increment to 1003

3. **Recreate Store** ✅
   - Created `recreate_stores.py`
   - Store ID=1: Sergeli 1/4/3
   - Set auto-increment to 2

4. **Update User Permissions** ✅
   - Created `fix_sotuvchi_permissions.py`
   - Updated sotuvchi.allowed_locations:
     * `{'id': 1, 'type': 'store'}` - Sergeli 1/4/3
     * `{'id': 1002, 'type': 'warehouse'}` - Akfa (NEW ID)
   - Updated sotuvchi.transfer_locations with same data

## Final State

### Database Structure
```
Stores:
- ID=1: Sergeli 1/4/3

Warehouses:
- ID=1001: UY Sergeli
- ID=1002: Akfa
```

### User Permissions
```json
sotuvchi.allowed_locations: [
  {"id": 1, "type": "store"},
  {"id": 1002, "type": "warehouse"}
]

sotuvchi.transfer_locations: [
  {"id": 1, "type": "store"},
  {"id": 1002, "type": "warehouse"}
]
```

## Verification Results ✅
- Total stores: 1
- Total warehouses: 2
- sotuvchi locations: 2 (CORRECT!)
- **No ID conflicts between stores and warehouses**

## Files Created
1. `migrate_warehouse_ids.py` - Initial migration attempt (found 0 warehouses)
2. `recreate_warehouses.py` - Recreated warehouses with IDs 1001, 1002
3. `recreate_stores.py` - Recreated store with ID=1
4. `fix_sotuvchi_permissions.py` - Updated user permissions to use new warehouse IDs
5. `verify_fix.py` - Verification script to check final state
6. `ID_COLLISION_FIX.md` - This documentation

## Testing Checklist
- [ ] Test sotuvchi login
- [ ] Verify only 2 locations show in sales page dropdown
- [ ] Confirm locations are: Sergeli 1/4/3 (Store) + Akfa (Warehouse)
- [ ] Test creating new sale from each location
- [ ] Test transfer between locations
- [ ] Verify no errors in console

## Future Prevention
To prevent this issue in the future:
1. Always use separate ID ranges for different entity types
2. When migrating data, check for ID conflicts first
3. Add database constraints to enforce ID separation if needed
4. Consider using composite keys (type + id) for location references

## Date Completed
2025-11-07 09:00 UTC
