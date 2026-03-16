# HOWTO: Understanding APFS Snapshots and "Missing Disk Space" on macOS

## Overview (Concepts)

### Files vs. Blocks

- **Files** are directory entries you can see (`ls`, Finder, etc.).
- **Disk blocks** are the physical storage units on the filesystem.
- Deleting a file removes the **directory entry**, but blocks remain
    allocated if something still references them.

### Processes Holding Files Open

- If a process has a file open, deleting the filename does **not free
    the blocks**.
- The blocks are released only when the process closes the file.

### APFS Snapshots

- A **snapshot** is a read‑only view of the filesystem at a moment in
    time.
- Snapshots reference the disk blocks that existed when they were
    created.
- If a file existed when a snapshot was taken, its blocks remain
    allocated until the snapshot disappears.

Important implications:

- A file may be **deleted and invisible** but still consume space.
- Snapshot space is **not visible to tools that scan directories**.

------------------------------------------------------------------------

## Useful Tools

### Show filesystem allocation

df shows how many blocks the filesystem has allocated.

    df -h /System/Volumes/Data

### Show reachable files

du walks the directory tree and sums blocks reachable from directories.

    sudo du -xhs /System/Volumes/Data

Difference between `df` and `du` is often **snapshot-pinned space**.

### Find deleted-but-open files

    lsof +L1

Shows files whose directory entry is gone but which are still open.

### List APFS snapshots

    diskutil apfs listSnapshots /System/Volumes/Data

Sample Output:

    Snapshots for disk1s2 (2 found)
    |
    +-- 4C7FC5C1-8EF8-4A37-93FF-8F5AAE91F288
    |   Name:        com.apple.TimeMachine.2026-03-15-114613.local
    |   XID:         44035845
    |   Purgeable:   Yes
    |   NOTE:        This snapshot limits the minimum size of APFS Container disk1
    |
    +-- 8CF363DB-8C06-431B-A0D7-0D190B9BC6FD
        Name:        com.apple.TimeMachine.2026-03-16-105854.local
        XID:         44039123
        Purgeable:   Yes

or

    tmutil listlocalsnapshots /

Sample Output:

    Snapshots for volume group containing disk /:
    com.apple.TimeMachine.2026-03-15-114613.local
    com.apple.TimeMachine.2026-03-16-105854.local
    com.apple.os.update-6A25AE9FD434A625043F39C8C5A6AC094327D2E0FBB1A1928D698D54766F9D44

### Delete a specific snapshot

    sudo tmutil deletelocalsnapshots YYYY-MM-DD-HHMMSS

### Thin snapshots (free space quickly)

    sudo tmutil thinlocalsnapshots / 100g 4

### Trigger a normal Time Machine cleanup

Running a real Time Machine backup typically removes most local
snapshots.

------------------------------------------------------------------------

## Workflow: Diagnosing Missing Disk Space

### Step 1 --- Confirm filesystem usage

    df -h /System/Volumes/Data

### Step 2 --- Compare with reachable files

    sudo du -xhs /System/Volumes/Data

If `df` \>\> `du`, snapshots are holding blocks.

### Step 3 --- Check for open deleted files

    lsof +L1

If found, stop the process holding the file.

### Step 4 --- Check snapshots

    tmutil listlocalsnapshots /

### Step 5 --- Free snapshot space

Option A: Run a Time Machine backup.

Option B: Delete or thin snapshots manually:

    sudo tmutil thinlocalsnapshots / 100g 4

------------------------------------------------------------------------

## Notes

- Time Machine **exclusions affect backups**, not snapshots.
- Snapshots capture the **entire filesystem state**, regardless of
    exclusions.
- Snapshot blocks are marked **purgeable**, so macOS will remove them
    automatically when space is tight.

------------------------------------------------------------------------

## Mental Model

Think of snapshots as **time layers of the filesystem**:

    current files
        |
        +-- snapshot (older blocks)
        +-- snapshot (older blocks)

Deleting a file removes it from the present layer, but blocks remain
while snapshots still reference them.
