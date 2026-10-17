# Ascend — Mobile App (Capacitor)

Native Android + iOS wrapper around the [Ascend | Self-Mastery & Habit Tracker](https://george-shenoda.github.io/Self_mastery/) web app.
The original `index.html` runs unchanged inside a WebView, with all data still kept
100% private in local storage (`https` origin, so storage is secure-context clean).

## What's in here

```
AscendMobile/
├── www/                      # the app's web layer (what ships inside the app)
│   ├── index.html            # original site + mobile/PWA head tags
│   ├── manifest.webmanifest  # installable-app manifest (name, theme, icons)
│   ├── icons/                # SVG + PNG icon set incl. maskable variant
│   └── vendor/               # Tailwind + Lucide bundled locally (works offline)
├── scripts/
│   ├── make_icons.py         # regenerates all launcher icons (PIL)
│   └── make_splash.py        # regenerates dark splash screens
├── android/                  # Android Studio project (built into an APK)
├── ios/                      # Xcode project (built into an IPA)
├── capacitor.config.json     # appId: com.georgeshenoda.ascend, app: "Ascend"
└── package.json
```

## Changes vs. the website

- **Viewport**: `viewport-fit=cover` + safe-area ready, prevents iOS rubber-banding zoom
- **Theme**: `theme-color` / status bar / navigation bar set to `#090d16` (app's dark bg)
- **Offline**: Tailwind and Lucide are served from `vendor/` instead of CDNs — the app
  works with no network (Google Fonts falls back to system fonts when offline)
- **Branding**: dark splash screens and emerald launcher icons on every density
- **Display**: `standalone` PWA manifest so it also installs from a browser

## Build the Android APK

Needs: Android Studio (or JDK 17 + Android SDK) — not available in this sandbox.

```bash
cd AscendMobile
npm install                     # if not already installed
npx cap sync                    # copy www/ into android/ + ios/
# Option A: Android Studio
npx cap open android            # then Build > Build Bundle(s)/APK(s) > Build APK(s)
# Option B: command line
cd android && ./gradlew assembleDebug
# -> android/app/build/outputs/apk/debug/app-debug.apk
./gradlew bundleRelease         # -> .aab for Google Play
```

## Build the iOS app

Needs: macOS + Xcode 15+.

```bash
cd AscendMobile
npm install && npx cap sync
cd ios && pod install           # if pods are needed
npx cap open ios                # then Product > Archive in Xcode
```

## Updating the app after editing `www/`

Every time `www/` changes, run `npx cap sync` before building.

## App-store metadata notes

- App ID: `com.georgeshenoda.ascend` (change in `capacitor.config.json` **before**
  your first store release — it cannot change later)
- The app requests only `INTERNET`; all user data stays on-device in local storage,
  which is a plus for privacy review on both stores.
- The site's account/reset/trigger log features need an interactive privacy policy
  URL for Play Store submission — add it to the Play Console listing.