%define revision 144745
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
%define basever 21.0.1171.0
%define patchver() ([ -f %{_src}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_src}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-unstable
Version: 21.0.1180.15
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
URL: https://www.chromium.org/getting-involved/dev-channel
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source1000: patch-21.0.1171.0-21.0.1180.0.diff.xz
Source1001: binary-21.0.1171.0-21.0.1180.0.tar.xz
Source1002: script-21.0.1171.0-21.0.1180.0.sh
Source1003: patch-21.0.1180.0-21.0.1180.4.diff.xz
Source1004: binary-21.0.1180.0-21.0.1180.4.tar.xz
Source1005: script-21.0.1180.0-21.0.1180.4.sh
Source1006: patch-21.0.1180.4-21.0.1180.11.diff.xz
Source1007: binary-21.0.1180.4-21.0.1180.11.tar.xz
Source1008: script-21.0.1180.4-21.0.1180.11.sh
Source1009: patch-21.0.1180.11-21.0.1180.15.diff.xz
Source1010: binary-21.0.1180.11-21.0.1180.15.tar.xz
Source1011: script-21.0.1180.11-21.0.1180.15.sh
Patch0: chromium-21.0.1171.0-remove-inline.patch
Provides: %{crname}
Conflicts: chromium-browser-stable
Conflicts: chromium-browser-beta
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, expat-devel, gperf
BuildRequires: nspr-devel, nss-devel, libalsa-devel
BuildRequires: glib2-devel, bzip2-devel, zlib-devel, libpng-devel
BuildRequires: jpeg-devel, mesagl-devel, mesaglu-devel
BuildRequires: libxscrnsaver-devel, dbus-glib-devel, cups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel pam-devel
BuildRequires: libevent-devel libflac-devel pulseaudio-devel
BuildRequires: elfutils-devel udev-devel yasm
BuildRequires: pkgconfig(libusb-1.0)
ExclusiveArch: i586 x86_64 armv7l

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the developer preview channel Chromium browser. It contains the
latest features but can be unstable at times, and new features may
require manual configuration to be enabled. If you prefer a stable and
tested browser, install the chromium-browser-stable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%prep
%setup -q -n chromium-%{basever}
%patch0 -p1 -b .remove-inline
%patchver 21.0.1171.0 21.0.1180.0
tar xvf %{_src}/binary-21.0.1171.0-21.0.1180.0.tar.xz
sh -x %{_src}/script-21.0.1171.0-21.0.1180.0.sh
%patchver 21.0.1180.0 21.0.1180.4
tar xvf %{_src}/binary-21.0.1180.0-21.0.1180.4.tar.xz
sh -x %{_src}/script-21.0.1180.0-21.0.1180.4.sh
%patchver 21.0.1180.4 21.0.1180.11
tar xvf %{_src}/binary-21.0.1180.4-21.0.1180.11.tar.xz
sh -x %{_src}/script-21.0.1180.4-21.0.1180.11.sh
%patchver 21.0.1180.11 21.0.1180.15
tar xvf %{_src}/binary-21.0.1180.11-21.0.1180.15.tar.xz
sh -x %{_src}/script-21.0.1180.11-21.0.1180.15.sh

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_crdir}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_crdir}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D use_gconf=0 \
	-D werror='' \
	-D use_system_v8=0 \
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
	-D use_system_xdg_utils=1 \
	-D use_system_yasm=1	\
	-D use_system_libusb=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
	-D use_system_vpx=0 \
	-D use_system_icu=0 \
%ifarch i586
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i586"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D disable_nacl=1 \
	-D linux_use_tcmalloc=0 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_crdir}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_src}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/ui_resources_standard.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/theme_resources_standard.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
#install -m 755 out/Release/xdg-mime %{buildroot}%{_crdir}/
#install -m 755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# Strip NaCl IRT
./native_client/toolchain/linux_x86_newlib/bin/x86_64-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_64.nexe
./native_client/toolchain/linux_x86_newlib/bin/i686-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_32.nexe

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_src}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 22 24 26 32 48 64 128 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{crname}
%{_crdir}/chromium-wrapper
%{_crdir}/chrome
%{_crdir}/chrome-sandbox
%{_crdir}/chrome.pak
%{_crdir}/libffmpegsumo.so
%ifnarch armv7l
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/nacl_helper_bootstrap
%{_crdir}/nacl_helper
%{_crdir}/nacl_irt_*.nexe
%endif
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/ui_resources_standard.pak
%{_crdir}/theme_resources_standard.pak
%{_crdir}/themes
%{_crdir}/default_apps
#%{_crdir}/xdg-mime
#%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png


%changelog
* Mon Jul 09 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1180.15-1mdv2012.0
+ Revision: 808665
- new upstream release 21.0.1180.15 (144745)
  * fixes a small sync problem (Issue: 134715)
- new upstream release 21.0.1180.11
  * Updated V8 - 3.11.10.12
  * Several crash fixes (Issues: 129884, 133692)
- new upstream release 21.0.1180.4
  * Updated V8 - 3.11.10.10
  * Fixed regression in alignment (Issue: 120859)
  * Fixed scrollbar layers being misplaced with a clipped owner layer
    (Issue: 132839)
- new upstream release 21.0.1180.0 (142910)
  * Updated V8 - 3.11.10.6
  * Content settings for Cookies now also show protected storage granted
    to hosted apps
  * Chromoting client plugin correctly up-scales on when page-zoom is >100%%.

* Mon Jun 18 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1171.0-3
+ Revision: 806139
- remove inlining for compatibility with legacy Mandriva releases
- use internal v8 for compatibility with legacy Mandriva releases
- add missing ui_resources and theme_resources pak files

  + Alexander Khrukin <akhrukin@mandriva.org>
    - BR: pkgconfig(libusb-1.0)
    - rel up

* Thu Jun 14 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1171.0-1
+ Revision: 805726
- update dependencies
- address rpmlint issues
- new upstream release 21.0.1171.0 (141382)
- new upstream release 19.0.1077.3 (128359)
- new upstream release 19.0.1068.1 (126852)

* Thu Jan 05 2012 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.26-1
+ Revision: 757966
- new upstream release 17.0.963.26 (116225)
  * Updated V8 - 3.7.12.12
  * Make webstore installs work when the Downloads folder is missing. (Issue:
    108812)
- detailed changelog: http://goo.gl/7H0bc

* Fri Dec 16 2011 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.12-1
+ Revision: 743128
- fix pam-devel package name in requires
- new upstream release 17.0.963.12 (114667)
  * stability and feature improvements
- remove inline for 2010.1

* Mon Dec 12 2011 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.2-2
+ Revision: 740525
- temporarily use internal libjpeg to prevent color problems

* Fri Dec 09 2011 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.2-1
+ Revision: 739455
- new upstream release 17.0.963.2 (113542)
  * stability and feature improvements
- detailed changelog: http://goo.gl/KfwCD

* Thu Dec 08 2011 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.0-1
+ Revision: 739077
- fix libcups-devel package name in requires
- new upstream release 17.0.963.0 (113143)
  * Updated V8 - 3.7.12.6
  * r113121 Omnibox suggestions will now be prerendered if our confidence of
    the user following the suggestion is high.
  * Support for <meta name="referrer">
  * Content Settings (in Options, Under the Hood) now has UI for "Mouse Cursor",
    which controls the Mouse Lock API permissions.
  * r110556 Fixed a renderer crash that could happen when opening a new tab
    with many tabs open.
  * WebKit Issue 73056 - Small fix for BiDi selection.
  * WebKit Issue 63903 - Fixed WebKit's implementation of bdo, bdi, and
    output elements to match HTML5 spec section 10.3.5.
- known issues
  * Extension/App/Themes installs on Linux/ChromeOS are currently not working.
    This includes sync-driven installs. (Bug 106599)
- fix elfutils-devel package name in requires
- new upstream release 17.0.942.0 (110446)
  * Updated V8 - 3.7.7.0.
  * Fixed New Tab page apps re-ordering issue.
  * Policy support for disabling the Cloud Print Connector has been added.
- known issues:
  * Crash when notification occurs [Issue: 103427]
- detailed changelog: http://goo.gl/jJeBR

* Thu Nov 17 2011 Claudio Matsuoka <claudio@mandriva.com> 17.0.938.0-1
+ Revision: 731467
- only include glib.h directly
- new upstream release 17.0.938.0 (109848)
- new upstream release 16.0.912.21 (108057)
  * stability fixes
- detailed changelog: http://goo.gl/30Te8

* Fri Oct 28 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.15-1
+ Revision: 707724
- new upstream release 16.0.912.15 (107511)
  * stability fixes
- detailed changelog: http://goo.gl/QVb1A

* Wed Oct 26 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.12-1
+ Revision: 707407
- new upstream release 16.0.912.12 (107048)
- detailed changelog: http://goo.gl/CmVI0

* Fri Oct 21 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.4-1
+ Revision: 705607
- new upstream release 16.0.912.4 (106469)
  * Updated V8 - 3.6.6.5
  * Fixed stability issue in Print and Instant
- detailed changelog: http://goo.gl/uhLg4

* Wed Oct 19 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.0-1
+ Revision: 705409
- new upstream release 16.0.912.0 (106036)
  * Updated V8 - 3.6.6.3
  * Native Client and Pepper plug-ins will be able to go use First Person
    controls for games and other applications after they go full screen and
    lock the mouse cursor. See PPB_MouseLock::LockMouse.
  * Printing does not work - crashes the tab.
  * Crash in Instant (Issue 100521). Fixed on trunk; workaround is to disable
    Instant (if it's already disabled and still crashes, please re-enable and
    disable, using the checkbox in Preferences -> Basics).
- detailed changelog at http://goo.gl/a3sMm

* Fri Oct 14 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.904.0-1
+ Revision: 704728
- new upstream release 16.0.904.0 (104662)
- detailed changelog at http://goo.gl/8fzZF
- add missing NaCl helper
- add missing XDG MIME utility
- add default apps
- add extra icons
- drop unnecessary patches
- build requires libelfutils-devel
- new upstream release 16.0.899.0 (103668)
  * Updated V8 - 3.6.4.1
  * FTP: fixed compatibility issue with ftp.comconlink.co.za, issue 98212
  * HTML5 audio uses faster method of communications between host and
    renderer, thus reducing lag for Javascript <audio> objects; should be
    most noticeable in games, issue 61022
  * Fixed many known stability issues.
  * Enabled Native Client for 32-bit Linux and also addresses a performance
    issue for Native Client on Intel Atom CPUs. [Issue: 92964],
    [nativeclient: 480]
- detailed changelog at http://goo.gl/UnP8S, http://goo.gl/Rny0U
- add support to armv7l

* Thu Sep 22 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.21-1
+ Revision: 700990
- new upstream release 15.0.874.21 (101896)
  * Fixed a bug that caused a crash if you tried to use the speech input
    keystroke (Ctrl+Shift+Period) on a (non-speech-enabled) textarea.
  * Fixed many known stability issues.
- detailed changelog at http://goo.gl/sl7Re

* Fri Sep 16 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.15-1
+ Revision: 700059
- new upstream release 15.0.874.15 (101261)
  * Updated V8 3.5.10.9
  * JavaScript fullscreen API now enabled by default.
  * Bug fixes and visual improvements for the New Tab Page.
  * Fixed many known stability issues.
- known Issue
  * Chrome crashes with Ctrl+P. [Issue: 96734]
- detailed changelog at http://goo.gl/7helU

* Wed Sep 14 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.12-1
+ Revision: 699791
- new upstream release 15.0.874.12 (100838)
  * Updated V8 3.5.10.7
  * Print preview issues with self-closing popups have been fixed
  * Fixed many known stability issues
- detailed changelog at http://goo.gl/tl9v7

* Fri Sep 09 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.1-1
+ Revision: 699069
- new upstream release 15.0.874.1 (99955)
  * Updated V8 3.6.0.0
  * Fixed a possible sync crash triggered by encryption of all sync data.
  * The --enable-accelerated-plugins flag was changed to --disable-
    accelerated-plugins. Pepper Plugins are now accelerated by default.
  * Fixed a crash when deleting cookies from chrome://settings/
    clearBrowserData.
  * Enable new client-side phishing detection for non-UMA users (previously
    UMA-only). When local heuristics trigger, sends only limited information
    that does not identify the page, such as a prefix of the hash of the URL,
    and other non-identifiable features such as whether you've visited the
    page before. [r99582]
  * Fixed many known stability issues.
- detailed changelog at http://goo.gl/pe8c8

* Thu Sep 01 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.865.0-1
+ Revision: 697658
- new upstream release 15.0.865.0 (98568)
- move Chromium 14 from unstable to beta

* Fri Aug 12 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.35-1
+ Revision: 694246
- new upstream release 14.0.835.35 (96116)
  * fixes for a number of stability issues
- detailed changelog at http://goo.gl/rVuhv

* Tue Aug 09 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.29-1
+ Revision: 693781
- new upstream release 14.0.835.29 (95793)
- detailed changelog at http://goo.gl/JKKD0

* Mon Aug 08 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.18-1
+ Revision: 693663
- new upstream release 14.0.835.18 (95190)
  * fixes for print preview and other stability issues
- detailed changelog at http://goo.gl/H1AmY
- new upstream release 14.0.835.15 (94879)
  * fixes for sync and stability
- detailed changelog at http://goo.gl/ixdJb
- new upstream release 14.0.835.8 (94414)
  * Updated V8 - 3.4.14.2
- detailed changelog at http://goo.gl/XQqe4
- new upstream release 14.0.825.0 (94025)
  * Updated V8 - 3.4.13.0
  * Implemented WebSocket HyBi 10 handshake and framing
  * [r93421] Fixed build without libgcrypt
  * [r93214] Fixed an issue with going back to a page with plugins
  * WebSocket HyBi 10 is incompatible with HyBi 00, which was implemented
    in older versions of Chrome
- fixed incorrect revision number in spec
- detailed changelog at http://goo.gl/w2qO7

* Tue Jul 19 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.825.0-1
+ Revision: 690622
- new upstream release 14.0.825.0 (93027)
  * Updated V8 - 3.4.12.1
- detailed changelog at http://goo.gl/G6gkT

* Tue Jun 28 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.803.0-1
+ Revision: 687619
- new upstream release 14.0.803.0 (90703)
  * Updated V8 - 3.4.6.2
  * [r90216] Change the meaning of third-party cookie blocking to allow
    whitelists (Issue 82039)
  * [r90417] Remove the global bookmarks menu by default. Currently, it can't
    be implemented efficiently. (Issue 86715)
- detailed changelog at http://goo.gl/8FXiF

* Tue Jun 21 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.797.0-1
+ Revision: 686539
- fix extra version to match new version modifier
- new upstream release 14.0.797.0 (dev)
  * Updated V8 - 3.4.4.0
- resolved issues
  * Crash when canceling print (Issue: 86229)
  * Mouse back and forward buttons stopped working  (Issue: 84836)
- detailed changelog at http://goo.gl/V3fgO

* Mon Jun 20 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.794.0-2
+ Revision: 686289
- apply version modifier patch

* Sat Jun 18 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.794.0-1
+ Revision: 685886
- new upstream release 14.0.794.0 (dev)
  * Updated V8 - 3.4.3.0
  * When installing items from the chrome webstore, always prompt with a
    native confirmation dialog.
  * Fix for failing navigation with chrome://newtab showing.
  * Added a makeshift multiprofile button.
  * DNSSEC authenticated HTTPS supported.
  * Intermittent connectivity issues with broken SSLv3 servers fixed.
- detailed changelog at http://goo.gl/RFH5T
- move Chromium 13 from unstable to beta

* Thu Jun 16 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.24-1
+ Revision: 685617
- new upstream release 13.0.782.24 (dev)
  * stability fixes
- detailed changelog at http://goo.gl/CN7TD

* Tue Jun 14 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.20-1
+ Revision: 685135
- new upstream release 13.0.782.20 (dev)
  * stability fixes
  * put hardware accelerated Canvas 2D back behind a flag
- detailed changelog at http://goo.gl/n8rMh

* Fri Jun 10 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.15-1
+ Revision: 683812
- new upstream release 13.0.782.15
  * stability fixes
- detailed changelog at http://goo.gl/2cc7Z

* Thu Jun 09 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.13-1
+ Revision: 683316
- new upstream release 13.0.782.13 (dev)
  * UI tweaks and stabilities fixes
- detailed changelog at http://goo.gl/wjL2e

* Wed Jun 08 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.11-1
+ Revision: 683143
- new upstream release 13.0.782.11 (dev)
  * UI tweaks and stabilities fixes
- detailed changelog at http://goo.gl/VcZ2z

* Fri Jun 03 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.1-1
+ Revision: 682566
- new upstream release 13.0.782.1 (dev)
  * Print preview refinements
  * IndexedDB+LevelDB made available in about:flags
  * Canvas 2D moved out from behind a flag (on by default)
- detailed changelog at http://goo.gl/cOQg2
- new upstream release 13.0.772.0 (dev)
  * Updated V8 - 3.3.8.1
  * Continued work on Print Preview
  * Making progress on rel:preload
  * Crash fixes
- detailed changelog at http://goo.gl/LkPWt

* Thu May 19 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.767.1-1
+ Revision: 676095
- new upstream release 13.0.767.1 (dev)
  * Print preview work continues
  * Omnibox string matching improvements
- detailed changelog at http://goo.gl/j6VMi

* Sat May 14 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.761.0-1
+ Revision: 674602
- new upstream release 13.0.761.0 (dev)

* Fri May 06 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.21-1
+ Revision: 670676
- new upstream release 12.0.742.21 (dev)
  * UI, performance, and stability issues
- detailed changelog at http://goo.gl/h82lP

* Thu May 05 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.16-1
+ Revision: 669305
- new upstream release 12.0.746.16 (dev)
  * address UI and performance issues
- detailed changelog at http://goo.gl/Zk7IX

* Fri Apr 29 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.12-1
+ Revision: 660588
- new upstream release 12.0.742.12 (dev)
  * address UI and performance issues
  * update Sync preferences UI
- detailed changelog at http://goo.gl/rzt6F

* Tue Apr 26 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.9-1
+ Revision: 659302
- new upstream release 12.0.742.9 (dev)
  * address UI and performance issues
  * update sync preferences UI
  * detailed changelog at http://goo.gl/wrdot
- new upstream release 12.0.742.5 (dev)
  * fix for sync regression
  * other bugfixes (detailed changelog at http://goo.gl/jGjPO)

* Thu Apr 21 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.0-1
+ Revision: 656378
- new upstream release 12.0.742.0 (dev)
  * stability and performance fixes
- detailed changelog at http://goo.gl/vT3Uf

* Thu Apr 14 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.733.0-1
+ Revision: 652954
- new upstream release 12.0.733.0 (dev)
  * stability and UI tweaks
- detailed changelog at http://goo.gl/wKW5I

* Thu Apr 07 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.725.0-1
+ Revision: 651782
- fix gcc 4.6 build issues
- new upstream release 12.0.725.0 (dev)
  * update V8 to 3.2.6.0
  * lots of code cleanup and refactoring under the covers
  * 78475 regression: Bidi Chrome UI lost directional display in menu
  * 78501 regression: NACL apps are no longer working
  * 78509 regression: Autofill fails on certain forms
  * 78073 regression: Autocomplete sometimes pops up in the upper left corner
- detailed changelog at http://goo.gl/6qDLq
- use system libflac, drop speex requirement

* Sat Mar 26 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.712.0-1
+ Revision: 648558
- new upstream release 12.0.712.0 (dev)
  * lots of behind the scenes work (code cleanup and refactorings)
  * numerous crash and regresson fixes
  * updated V8 to 3.2.3.1
  * detailed changelog at http://goo.gl/XF7wu

* Tue Mar 22 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.16-1
+ Revision: 647589
- revert some changes introduced in revision 647140, Chromium doesn't
  build with some of the system libraries including libicu44.
- new upstream release 11.0.696.16 (dev)
  * fix clicking on the labels closing content settings dialog (Issue 76115)
  * fix keyring unlocking making chrome unusable (Issue 72499)
  * fix sample extension for chrome.experimental.proxy API (Issue 62700)
  * fix several known crashes (Issues 76401, 75264)

  + Funda Wang <fwang@mandriva.org>
    - build with more system libs

* Fri Mar 18 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.14-1
+ Revision: 646473
- new upstream release 11.0.696.14 (dev)
  * blacklist a small number of HTTPS certificates
  * translation updates
  * fix about:gpu launching GPU process even if GPU is blocked by software
    rendering list (Issue 76115)
  * fix restore infobar after crash (Issue 75654)
  * fix app context-menu after uninstalling the extension (Issue 75662)
  * fix for a known crash (Issue 74777)
  * fix SPDY-related check failure (Issue 75657)

* Wed Mar 16 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.12-1
+ Revision: 645448
- new upstream release 11.0.696.12 (dev)
  * fix New York Times Chrome app crashes (Issue 75563)
  * fix sync login dlg is truncated (Issue 72490)
  * fix status bar/target URL not shown when hovering over links (Issue 75268)
  * fix several known crashes (Issues 75171, 75443 and 75828)
  * fix bookmark focus not lost when moved away from bookmark bar (Issue 75367)
  * fix tooltips from browser tabs persisting for too long (Issue 75334)
  * fix for content settings updates not reflecting current Incognito
    session (Issue 74466)
  * fix for NewTabPage not updating when a new theme is applied (Issue 74311)
  * fixed download requests in chrome frame which occur in response to top
    level POSTs (Issue 73985)
  * fix lock up on form submit, constantly duplicating autofill settings to
    blame (Issue 74911)
- updated chromium theme art from 11.0.696.12
- check presence of patch files

* Sat Mar 12 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.3-2
+ Revision: 643869
- new upstream release 11.0.696.1 (dev)
  * updated V8 to 3.2.0.1
  * New cookies and other data page in tabbed settings (Issue 64154).
- update to 11.0.696.3 (dev)
  * fix omnibox auto suggested entries selection (Issue 75366).
  * fix "Behavior" string is externalized on the Exceptions page (Issue 74080).
  * fix Chromium not loading some plugins (Issue 75351).
  * fix POST omits body after NTLM authentication (Issue 62687).
- apply patches correctly

* Wed Mar 09 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.686.3-1
+ Revision: 643155
- new upstream release 11.0.686.3 (dev)
  * fix autofill related crash (issue 74511)
- new upstream release 11.0.686.1 (dev)
  * fixes the HTML5 issue noted in 11.0.686.0 (Issue 74451).

* Tue Mar 01 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.686.0-1
+ Revision: 641208
- new upstream release 11.0.686.0 (dev)
  * Updated V8 - 3.1.6.1
  * Accelerated compositing turned on by default (use
    --disable-accelerated-layers to disable).
  * Fixed a bug affecting the bookmark manager and other extensions.
    (Issue 43448)
  * FTP: fixed a compatibility issue. (Issue 72060)
  * Known issue: HTML5 videos don't play on Vimeo.com (Issue 74451)
  * More details about additional changes available at http://goo.gl/fDmIa
- add libpam-devel as build requirement

* Fri Feb 18 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.672.2-1
+ Revision: 638543
- remove unnecessary webkit svn revision patch
- new upstream release 11.0.672.2
- move 10.0.648.82 patch from unstable to beta
- move 10.0.648.45 base tarball from unstable to beta

* Thu Feb 17 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.82-1
+ Revision: 638250
- new upstream release 10.0.648.82 (dev)
- conflict with chromium-browser beta
- add beta browser to the downgrade notice in spec description
- don't obsolete chromium-browser
- add obsoletes entry for old (canary) chromium-browser package

* Thu Feb 10 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.45-1
+ Revision: 637113
- imported package chromium-browser-unstable

