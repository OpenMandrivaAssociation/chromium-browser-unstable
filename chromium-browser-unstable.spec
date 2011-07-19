%define revision 93027
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define basever 14.0.794.0
%define patchver() ([ -f %{_sourcedir}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_sourcedir}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-unstable
Version: 14.0.825.0
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
URL: http://www.chromium.org/getting-involved/dev-channel
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source1000: patch-14.0.794.0-14.0.797.0.diff.xz
Source1001: binary-14.0.794.0-14.0.797.0.tar.xz
Source1002: patch-14.0.797.0-14.0.803.0.diff.xz
Source1003: binary-14.0.797.0-14.0.803.0.tar.xz
Source1004: patch-14.0.803.0-14.0.825.0.diff.xz
Source1005: binary-14.0.803.0-14.0.825.0.tar.xz
Patch0: chromium-14.0.825.0-skip-builder-tests.patch
Patch1: chromium-14.0.797.0-gcc46.patch
Patch2: chromium-13.0.782.1-exclude-chromeos-options.patch
Provides: %{crname}
Conflicts: chromium-browser-stable
Conflicts: chromium-browser-beta
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libalsa-devel
BuildRequires: libglib2-devel, libbzip2-devel, libz-devel, libpng-devel
BuildRequires: libjpeg-devel, libmesagl-devel, libmesaglu-devel
BuildRequires: libxscrnsaver-devel, libdbus-glib-devel, libcups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel libpam-devel
BuildRequires: libevent-devel libflac-devel
ExclusiveArch: i586 x86_64 armel

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
%patchver 14.0.794.0 14.0.797.0
tar xvf %{_sourcedir}/binary-14.0.794.0-14.0.797.0.tar.xz
%patchver 14.0.797.0 14.0.803.0
tar xvf %{_sourcedir}/binary-14.0.797.0-14.0.803.0.tar.xz
%patchver 14.0.803.0 14.0.825.0
tar xvf %{_sourcedir}/binary-14.0.803.0-14.0.825.0.tar.xz

%patch0 -p1 -b .skip-builder-tests
%patch1 -p1 -b .gcc46
%patch2 -p1 -b .exclude-chromeos-options
echo "%{revision}" > build/LASTCHANGE.in

sed -i -e '/test_support_common/s/^/#/' \
	chrome/browser/sync/tools/sync_tools.gyp

# Hard code extra version
FILE=chrome/common/chrome_version_info_linux.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

# Remove old files
# 14.0.803.0
rm chrome/app/theme/pageinfo_internal.png
# 14.0.825.0
rm app/resources/app_top_center.png
rm app/resources/app_top_left.png
rm app/resources/app_top_right.png
rm app/resources/browser_action_badge_center.png
rm app/resources/browser_action_badge_left.png
rm app/resources/browser_action_badge_right.png
rm app/resources/close.png
rm app/resources/close_h.png
rm app/resources/close_p.png
rm app/resources/close_sa.png
rm app/resources/close_sa_h.png
rm app/resources/close_sa_p.png
rm app/resources/content_bottom_center.png
rm app/resources/content_bottom_left_corner.png
rm app/resources/content_bottom_right_corner.png
rm app/resources/content_left_side.png
rm app/resources/content_right_side.png
rm app/resources/default_favicon.png
rm app/resources/folder_closed.png
rm app/resources/folder_closed_rtl.png
rm app/resources/folder_open.png
rm app/resources/folder_open_rtl.png
rm app/resources/frame_app_panel_default.png
rm app/resources/frame_default.png
rm app/resources/frame_default_inactive.png
rm app/resources/input_good.png
rm app/resources/large_throbber.png
rm app/resources/linux_close.png
rm app/resources/linux_close_h.png
rm app/resources/linux_close_p.png
rm app/resources/linux_maximize.png
rm app/resources/linux_maximize_h.png
rm app/resources/linux_maximize_p.png
rm app/resources/linux_minimize.png
rm app/resources/linux_minimize_h.png
rm app/resources/linux_minimize_p.png
rm app/resources/linux_restore.png
rm app/resources/linux_restore_h.png
rm app/resources/linux_restore_p.png
rm app/resources/maximize.png
rm app/resources/maximize_h.png
rm app/resources/maximize_p.png
rm app/resources/menu_arrow.png
rm app/resources/menu_check.png
rm app/resources/menu_droparrow.png
rm app/resources/menu_droparrow_sharp.png
rm app/resources/minimize.png
rm app/resources/minimize_h.png
rm app/resources/minimize_p.png
rm app/resources/restore.png
rm app/resources/restore_h.png
rm app/resources/restore_p.png
rm app/resources/textbutton_b_h.png
rm app/resources/textbutton_b_p.png
rm app/resources/textbutton_bl_h.png
rm app/resources/textbutton_bl_p.png
rm app/resources/textbutton_br_h.png
rm app/resources/textbutton_br_p.png
rm app/resources/textbutton_c_h.png
rm app/resources/textbutton_c_p.png
rm app/resources/textbutton_l_h.png
rm app/resources/textbutton_l_p.png
rm app/resources/textbutton_r_h.png
rm app/resources/textbutton_r_p.png
rm app/resources/textbutton_t_h.png
rm app/resources/textbutton_t_p.png
rm app/resources/textbutton_tl_h.png
rm app/resources/textbutton_tl_p.png
rm app/resources/textbutton_tr_h.png
rm app/resources/textbutton_tr_p.png
rm app/resources/throbber.png
rm app/resources/window_bottom_center.png
rm app/resources/window_bottom_left_corner.png
rm app/resources/window_bottom_right_corner.png
rm app/resources/window_left_side.png
rm app/resources/window_right_side.png
rm app/resources/window_top_center.png
rm app/resources/window_top_left_corner.png
rm app/resources/window_top_right_corner.png
rm app/test/data/data_pack_unittest/sample.pak
rm chrome/app/theme/chromium/chromium_icon_32.png
rm chrome/app/theme/ntp_store_favicon.png
rm chrome/app/theme/ntp_themes_gallery_favicon.png
rm chrome/app/theme/ntp_welcome_favicon.png
rm chrome/app/theme/statusbar_window_center.png
rm chrome/app/theme/statusbar_window_left.png
rm chrome/app/theme/statusbar_window_right.png
rm chrome/app/theme/statusbar_window_switcher.png
rm remoting/webapp/me2mom/chromoting128.png
rm third_party/WebKit/Source/WebCore/Resources/crossHairCursor.png
rm third_party/WebKit/Source/WebCore/Resources/notAllowedCursor.png

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_crdir}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_crdir}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D use_gconf=0 \
	-D werror='' \
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
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

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_sourcedir}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
install -m 644 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_sourcedir}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 32 48 256; do
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
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/themes
%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
