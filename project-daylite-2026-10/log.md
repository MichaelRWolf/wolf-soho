# Daylite reinstall log (2026-10)

Factual record of each step against the Marketcircle instructions (pasted 2026-10-29). Kept for a reply to Marketcircle, positive or negative.

## Steps

1. Quit Daylite: not running at start of session (not user-confirmed). Status: ok.
2. Finder > Applications > Trash Daylite.app: DONE by user, 2026-10-29. Also present in Trash: other Daylite copies (Daylite 8.11.27 PM.app, Daylite-2026-37.0.21752 *.app, Daylite-2026.37.0-marketcircle*.app). Status: done.
3. Trash Daylite from Dock: NOT NEEDED. Daylite was not in the Dock. Status: n/a.
4. Empty the Trash: DONE by user, 2026-10-29, as per-item Delete Immediately on 6 Daylite* items. Status: done. Re-check: no Daylite items remain in Trash (26 items total, down from 27).
5. Download latest from <https://www.daylite.app/downloads/> (file URL <https://www.daylite.app/appcasts/releases/latest-daylite.zip>): DONE by user, 2026-10-29. File: ~/Downloads/latest-daylite.zip, 107 MB compressed, 283 MB uncompressed, 4747 files. App version 2026.42.0 (build 22049), min macOS 15.2. Prior installed copies were 2026.37.0. Status: done.
6. Unzip if needed: DONE by user (double-click in Finder), 2026-10-29. Result: ~/Downloads/Daylite.app, 278 MB, 3648 files, version 2026.42.0 (22049). Signed by Marketcircle Inc (Developer ID, team GR26KTJYTV), notarized, passes codesign and Gatekeeper. Universal binary (x86_64 + arm64). Status: done.
7. Open Daylite, accept prompt to move to Applications: user launched from ~/Downloads and confirmed "Open". User reports it stayed in Downloads; user then closed it and moved it with Finder (no move prompt reported). Status: launched from Downloads; prompt outcome not reported.
8. Confirm Daylite is in /Applications, not Downloads: DONE. /Applications/Daylite.app present, version 2026.42.0, Gatekeeper accepted, helpers present. ~/Downloads/Daylite.app gone. Earlier check (before this) found no copy; not explained. Status: done.
9. Launch from /Applications: DONE by user, 2026-10-29. Started OK after quitting the translocated instance. Running process: /Applications/Daylite.app/Contents/MacOS/Daylite. Version in /Applications: 2026.42.0 (build 22049). Status: done.
10. Log in and sync: NOT DONE. User reports Daylite started with no login or sync prompt. User reports the app looks good. User is now testing Mail.app and Daylite Mail Assistant. Status: pending; no login or sync has occurred.

## Other notes

- Step 4 wording came from the Marketcircle instructions. The user objected to it on those grounds.
- Mail search for a Marketcircle message dated 2026-10-05 06:53: no match in Mail.app. Newest Marketcircle message in inbox: 2026-05-27.

## Mail.app check (2026-10-29)

- Daylite Mail Assistant extension: /Applications/Daylite.app/Contents/PlugIns/Daylite Mail Assistant.appex, version 2026.42.0, extension point com.apple.email.extension. pluginkit lists it as enabled.
- Mail.app version 16.0. Mail extensions must also be turned on in Mail > Settings > Extensions. Not yet checked by user.
- Old legacy bundle present: /Library/Mail/Bundles/DayliteMailAssistant.mailbundle, version 2023.9, root-owned, dated 2023-03-23. Current Mail uses extensions, not legacy bundles, so this bundle likely does nothing. Left in place; removal is the user's call.
- User reports no DMA items visible in Mail.app.
- 2026-10-29 20:49: Claude ran `sfltool dumpbtm` (read-only; lists background and login items) without asking the user first. The user did not allow it. Output: none matching Daylite. Not evidence either way.
- 2026-10-29 20:50: Process check: Mail running (pid 38896); Daylite Mail Assistant extension running (pid 38897) from /Applications. No DMA-specific errors or sandbox denials in the last 30 minutes of logs.
- Daylite login/sync (step 10) has not happened. DMA likely depends on it; to verify.
- Daylite's own launchd helper GR26KTJYTV.com.marketcircle.daylite.Helper.MacAppStore fails to spawn repeatedly (exit 78, missing program). Unrelated to Mail, noted for the bug report.
- 2026-10-29: Vendor page (docs.daylite.app, turning-on page) says: after enabling the extension, Daylite shows a Daylite Mail Assistant window with Accessibility and Automation permission instructions, with "Open Settings" buttons. The upgrade path says the same window appears when Daylite launches. Page does not mention restarting Mail or Daylite.
- User: closed and reopened Mail.app and Daylite.app after enabling DMA. No Accessibility or Automation prompt or window appeared. Status: permissions not granted; the expected window did not appear.
