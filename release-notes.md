## SC Utility Suite v1.0.1 - Production Release

Standalone v1.0.1 release. Microsoft Store packages use package identity 1.0.1.0 and remain in the existing certification submission; they predate the latest standalone binaries.

### Included Applications
- **Archive Unpacker**: Fast multi-format archive extraction (.zip, .7z, .tar, .gz, .bz2, .rar) and inspection
- **Dup Scrub**: Multi-phase duplicate file scanner (file size -> sampled XxHash64 -> full XxHash64; byte comparison before recycling) with Recycle Bin safety
- **HEIC Studio**: Batch convert Apple HEIC/HEIF photos, WebP, and AVIF to JPG, PNG, and PDF offline
- **Media Trim**: Video trimming, keyframe-dependent lossless video cuts and MP3/WAV audio extraction powered by embedded static FFmpeg
- **PDF Knife**: Local PDF page manipulation (split ranges, merge documents, burst pages) with zero cloud dependencies
- **Screen Lens**: Screen recording and optimized GIF creation with region selection and floating pause/resume/stop controls
- **USB Flasher**: Bootable UEFI ISO burning and raw sector disk imaging (.img, .bin) to removable drives

### Verified SHA256 Package Checksums

| File | Type | SHA256 Hash |
| :--- | :--- | :--- |
| SC_Utility_Suite_AllInOne_Setup_v1.0.1.exe | Master Installer | 17b82c13a377469e27918fcbaf65116fcf5ed484a34507884ce26a6aa979b114 |
| SC_Utility_Suite_AllInOne_v1.0.1_Portable.zip | Master Portable | d93a5641659dd86c107e398e6fb4aa23a6bf579f39d7a37db6af9eb4c6f4737e |
| ArchiveUnpacker_Setup_v1.0.1.exe | Setup Wizard | 8336557cf5ce27be8404a0464cc1bca15ffb66bd83ba4add93cce243e1ee5808 |
| ArchiveUnpacker_v1.0.1_Portable.zip | Portable ZIP | 5c6300366928101b9442c7af580a6b59edec6bb8edb899a556be8710556df6b3 |
| DupScrub_Setup_v1.0.1.exe | Setup Wizard | e244e0716dd67eaab4dd9f56931e0da82ac8b2a25aaf9ef01f6889e180b34c2b |
| DupScrub_v1.0.1_Portable.zip | Portable ZIP | 67fac2b1b2a966490e8a8f54eaf43723e7d1b16bef1aa756e4e0f8dc518594de |
| HeicStudio_Setup_v1.0.1.exe | Setup Wizard | a01aae722d65f47c46ffabfafe4861cc53dcad2960955dc7441ea4b50175f29e |
| HeicStudio_v1.0.1_Portable.zip | Portable ZIP | 9649f6ca721ebbb8c643801234cdb3569d2ad413bae7f688a733b68d9f1d2229 |
| MediaTrim_Setup_v1.0.1.exe | Setup Wizard | 5a929b8a0ef4585dfe5b6688c5444c44637b916ed87eba6b765a9804af081601 |
| MediaTrim_v1.0.1_Portable.zip | Portable ZIP | 17f27e9ee71e1fcd4abcd4f59f9f8b401412a8930b7d86dbdabd6eaafbbf95ab |
| PdfKnife_Setup_v1.0.1.exe | Setup Wizard | a4bae8c0d824545e7f1a637b00a1ce2d7224e5fddabf13628b438bf4eef8e617 |
| PdfKnife_v1.0.1_Portable.zip | Portable ZIP | 864a3223295c82231d3e9574696bbac2460a5b6691303debeb979b8d8e80634e |
| ScreenLens_Setup_v1.0.1.exe | Setup Wizard | 41385f5c66c589b04fa985fc30fa3fda055f1632af3b7cf364834fbb76f79a78 |
| ScreenLens_v1.0.1_Portable.zip | Portable ZIP | 1bb025afa444c51405608f99ebea46a16095b90dcab854f4235c8f8acdf44f31 |
| UsbFlasher_Setup_v1.0.1.exe | Setup Wizard | 8874ce4dce67a650e8e1666bee7c6c207858c7979a024ffaa61de8f9ff203191 |
| UsbFlasher_v1.0.1_Portable.zip | Portable ZIP | aebee5988ef96bb8a8ffa02977c80fa5a6ece66d7eb2dc657d085171fe55aa6a |

### System Requirements
- Windows 10 (Build 19041+) or Windows 11
- 64-bit (x64) processor architecture
- Completely self-contained .NET 8 runtime included; no external prerequisites required
### Signing and channel status

Current standalone installers are unsigned. The hashes above establish file integrity, not trusted publisher identity. Microsoft Store certification and Winget catalog merges are pending; passing manifest validation does not establish catalog availability or Store approval. File processing is local; purchase/activation checks contact Microsoft Store or Gumroad.

Media Trim edits one file at a time in both tiers; no batch queue or multipass feature is provided. PRO hides the upgrade strip. Other PRO limits are described on the showcase page. The exact source/build/dependency delivery for the included FFmpeg build remains an unresolved distribution requirement, separate from binary integrity checks.
