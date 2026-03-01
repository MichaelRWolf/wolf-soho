# Disk cleanup phase 1

man## 1. Keep one iPhone backup, remove the rest (manual)

**Location:** `~/Library/Application Support/MobileSync/Backup/`

**Current contents:**

| Item | Size | Notes |
|------|------|--------|
| `00008030-001578A111D2402E` | **50 GB** | Keep this one (most recent; modified Jan 10 2025) |
| `00008110-001104E402F2601E` | 0 B | Empty folder — safe to remove |
| `a7b806b91eb5bcec0eae5c8d2f945bc0e15067d1` | 0 B | Empty folder — safe to remove |
| `2017-07-27_timestamp` | file | Legacy — safe to remove |
| `files_today.ksh` | 4 KB | Legacy script — safe to remove |

**Steps:**

1. Quit Finder if it has the Backup folder open.
2. Open Finder → Go → Go to Folder (Cmd+Shift+G).
3. Paste: `~/Library/Application Support/MobileSync/Backup/`
4. **Keep** the folder `00008030-001578A111D2402E` (your 50 GB backup).
5. **Delete** (move to Trash or Delete immediately):
   - `00008110-001104E402F2601E`
   - `a7b806b91eb5bcec0eae5c8d2f945bc0e15067d1`
   - `2017-07-27_timestamp`
   - `files_today.ksh`
6. Empty Trash.

**Alternative (Terminal):** From your home directory:

```bash
cd ~/Library/Application\ Support/MobileSync/Backup/
rm -rf 00008110-001104E402F2601E a7b806b91eb5bcec0eae5c8d2f945bc0e15067d1
rm 2017-07-27_timestamp files_today.ksh
```

(Only removes the empty/legacy items; keeps the 50 GB backup.)

---

## 2. Chrome ML/cache

**Done:** The folder `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel/` (~4 GB) has been removed. Chrome will recreate it if needed.

---

## 3. Large voice memos, audiobooks, and music

### Voice memos (total ~1.6 GB)

**Location:** `~/Library/Application Support/com.apple.voicememos/Recordings/`

**Largest files (size, date, path):**

| Size | Date | Path |
|------|------|------|
| 701.0 MB | Mar 6 2022 | `.../Recordings/20210503 224257-49B0C64D.m4a` |
| 31.6 MB | May 17 2023 | `.../Recordings/20230517 110510-96EAA525.m4a` |
| 8.1 MB | May 31 2023 | `.../Recordings/20230528 162319-39347470.m4a` |
| 4.7 MB | Jun 18 2022 | `.../Recordings/20220616 133348-B2289DA2.m4a` |
| 4.4 MB | Jun 14 2022 | `.../Recordings/20220614 100305-A9BBD2E3.m4a` |
| 4.3 MB | Jan 30 2021 | `.../Recordings/20200503 143844-919D8205.m4a` |
| 4.0 MB | Jul 18 2022 | `.../Recordings/20220718 105458-31D893A5.m4a` |
| 2.9 MB | Aug 17 2023 | `.../Recordings/20230816 215335-FD60125B.m4a` |
| 2.6 MB | Oct 17 2022 | `.../Recordings/20221015 215349-41344B42.m4a` |
| 2.3 MB | Jan 30 2021 | `.../Recordings/20200121 220754-DC65F3D2.m4a` |

The 701 MB file (May 3 2021 recording) dominates; consider moving it to NAS or deleting if no longer needed.

### Audiobooks (total ~205 MB)

**Location:** `~/Audiobooks/`

| Size | Date | Path |
|------|------|------|
| 205 MB | Jul 1 2016 | `~/Audiobooks/Reinventing Organizations Audiobook 32.m4b` |

Single file; move to NAS if you want to free the space.

### Music (total ~14 GB)

**Location:** `~/Music/iTunes/iTunes Media/`

**Largest files:**

| Size | Date | Path |
|------|------|------|
| 222.0 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-08-29 Sat - Mary.m4a` |
| 211.7 MB | Apr 25 2020 | `.../Unknown Artist/Unknown Album/Laura_L.WendyRW.m4a` |
| 209.9 MB | Jul 21 2019 | `.../Unknown Artist/Unknown Album/ErinB_audio_only.m4a` |
| 201.0 MB | Apr 25 2020 | `.../Unknown Artist/Unknown Album/Laura_L.WendyRW2.m4a` |
| 201.0 MB | Apr 25 2020 | `.../Unknown Artist/Unknown Album/Laura_L.WendyRW 1.m4a` |
| 188.9 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-02-28 Friday - DDD.m4a` |
| 177.7 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-08-29 Sat - Mary 1.m4a` |
| 177.7 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-08-29 Resting in Truth...` |
| 175.7 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-02-28 Fri - DDD.m4a` |
| 175.7 MB | Mar 2 2020 | `.../Unknown Artist/Unknown Album/2020-02-28 Delight in the Deliciousness...` |

Most of the largest items are workshop/recording m4a files in Unknown Artist/Unknown Album. Consider moving whole albums or the Unknown Album folder to NAS if rarely played locally.

---

## 4. NLTK data

**Done:** `~/nltk_data` (3.3 GB) has been removed. Reinstall with `python -m nltk.downloader <resource>` when needed (e.g. `punkt`, `maxent_treebank_pos_tagger`).
