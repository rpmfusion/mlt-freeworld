# needs nonfree/ndi-sdk
%bcond_with  ndi

#globals for https://github.com/mltframework/mlt/commit/ea973eb65c8ca79a859028a9e008360836ca4941
%global gitdate 20171213
%global commit ea973eb65c8ca79a859028a9e008360836ca4941
%global shortcommit %(c=%{commit}; echo ${c:0:7})
#global gver .%%{gitdate}git%%{shortcommit}

%global realname mlt

Name:           mlt-freeworld
Version:        7.12.0
Release:        1%{?dist}
Summary:        Toolkit for broadcasters, video editors, media players, transcoders

# mlt/src/win32/fnmatch.{c,h} are BSD-licensed.
# but is not used in Linux
License:        GPLv3 and LGPLv2+
URL:            http://www.mltframework.org/
Source0:        https://github.com/mltframework/mlt/archive/v%{version}/%{realname}-%{version}.tar.gz
#Patch0:         https://github.com/mltframework/mlt/compare/v6.4.1...%%{commit}.diff

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  sed
BuildRequires:  frei0r-devel
BuildRequires:  opencv-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qt3d-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL2-devel
%if ! (0%{?rhel} >= 8)
BuildRequires:  SDL_image-devel
BuildRequires:  SDL2_image-devel
%endif
BuildRequires:  gtk2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libatomic
BuildRequires:  libogg-devel
#Deprecated dv and kino modules are not built.
#https://github.com/mltframework/mlt/commit/9d082192a4d79157e963fd7f491da0f8abab683f
#BuildRequires:  libdv-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  ladspa-devel
BuildRequires:  libxml2-devel
BuildRequires:  sox-devel
BuildRequires:  freetype-devel
BuildRequires:  libexif-devel
BuildRequires:  fftw-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  vid.stab-devel
BuildRequires:  movit-devel
BuildRequires:  eigen3-devel
BuildRequires:  libebur128-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  xine-lib-devel

Requires:  mlt = %{version}

%description
MLT is in Fedora proper without ffmpeg support, this package give us
the ffmpeg support.

MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors,media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to use
tools, xml authoring components, and an extendible plug-in based API.


%prep
%autosetup -p1 -n %{realname}-%{version}

chmod 644 src/modules/qt/kdenlivetitle_wrapper.cpp
chmod 644 src/modules/kdenlive/filter_freeze.c
chmod -x demo/demo

# mlt/src/win32/fnmatch.{c,h} are BSD-licensed.
# be sure that aren't used
rm -r src/win32/

%build
%cmake -DCMAKE_SKIP_RPATH:BOOL=ON           \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON   \
       %{?with_ndi: -DMOD_NDI:BOOL=ON -DNDI_SDK_INCLUDE_PATH=%{_includedir}/ndi-sdk -DNDI_SDK_LIBRARY_PATH=%{_libdir} -DNDI_INCLUDE_DIR=%{_includedir}/ndi-sdk -DNDI_LIBRARY_DIR=%{_libdir}}

%cmake_build

%install
%cmake_install

# Debug before remove, list all files to check with main mlt package
# find %{buildroot} | grep -vP "mlt/avformat|libmltavformat.so"
# remove all execept avformat (ffmpeg part)
#find %{buildroot} -type f | grep -vP "mlt/avformat|libmltavformat.so" | xargs rm
find %{buildroot} -type f -print0 | grep -vPz "mlt-7/avformat|libmltavformat.so|libmltxine.so" | xargs -0 rm
find %{buildroot} -type l -delete
find %{buildroot} -type d -empty -delete

%ldconfig_scriptlets

%files
%{_libdir}/mlt-7/libmltavformat.so
%{_libdir}/mlt-7/libmltxine.so
%{_datadir}/mlt-7/avformat

%changelog
* Sun Nov 20 2022 Sérgio Basto <sergio@serjux.com> - 7.12.0-1
- Update mlt-freeworld to 7.12.0

* Sun Nov 06 2022 Sérgio Basto <sergio@serjux.com> - 7.10.0-1
- Update mlt-freeworld to 7.10.0

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 7.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Aug 04 2022 Sérgio Basto <sergio@serjux.com> - 7.8.0-1
- Update mlt-freeworld to 7.8.0

* Thu Apr 07 2022 Sérgio Basto <sergio@serjux.com> - 7.6.0-1
- Update mlt-freeworld to 7.6.0

* Sun Feb 13 2022 Sérgio Basto <sergio@serjux.com> - 7.4.0-1
- Update to 7.4.0

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 6.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 6.26.1-3
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 29 2021 Sérgio Basto <sergio@serjux.com> - 6.26.1-1
- Update mlt-freeworld to 6.26.1

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
- On epel8 not BR SDL_images

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 6.24.0-2
- Rebuilt for new ffmpeg snapshot

* Sat Dec 26 2020 Sérgio Basto <sergio@serjux.com> - 6.24.0-1
- Update mlt-freeworld to 6.24.0

* Thu Aug 20 2020 Sérgio Basto <sergio@serjux.com> - 6.22.1-1
- Update to 6.22.1
- Sync with Fedora

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 6.20.0-2
- Rebuild for ffmpeg-4.3 git

* Tue Feb 18 2020 Martin Gansser <martinkg@fedoraproject.org> - 6.20.0-1
- Update to 6.20.0

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Sérgio Basto <sergio@serjux.com> - 6.18.0-1
- Update to 6.18.0

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 6.16.0-2
- Rebuild for new ffmpeg version

* Sat May 11 2019 Sérgio Basto <sergio@serjux.com> - 6.16.0-1
- Update MLT to 6.16.0

* Mon Apr 29 2019 Sérgio Basto <sergio@serjux.com> - 6.14.0-1
- Update mlt-6.14.0
- Sync with Fedora
- Modernize spec

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Martin Gansser <martinkg@fedoraproject.org> - 6.12.0-1
- Update to 6.12.0

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Sérgio Basto <sergio@serjux.com> - 6.10.0-1
- Update to 6.10.0

* Sun May 13 2018 Sérgio Basto <sergio@serjux.com> - 6.8.0-1
- Update to 6.8.0 (as in Fedora proper)

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 6.6.0-3
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 6.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Sérgio Basto <sergio@serjux.com> - 6.6.0-1
- Update to 6.6.0

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 6.5.0-0.7.20171213gitea973eb
- Rebuilt for ffmpeg-3.5 git
- MLT doesn't needs or use libquicktime

* Sun Dec 24 2017 Sérgio Basto <sergio@serjux.com> - 6.5.0-0.6.20171213gitea973eb
- Update snapshot
- Add vid.stab support

* Fri Nov 17 2017 Sérgio Basto <sergio@serjux.com> - 6.5.0-0.5.20171114git73bfefd
- Update snapshot

* Sun Nov 05 2017 Sérgio Basto <sergio@serjux.com> - 6.5.0-0.4.20171105gitddc40aa
- Update snapshot

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 6.5.0-0.3
- Rebuild for ffmpeg update

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 6.5.0-0.2
- Sync with fedora proper

* Sat Oct 07 2017 Sérgio Basto <sergio@serjux.com> - 6.5.0-0.1
- Update to 6.5.0 pre-version and switch to SDL2
- Enable movit support

* Fri Sep 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 6.4.1-5
- Add xlocale.h fix from fedora mlt

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 6.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 6.4.1-3
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 6.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Sérgio Basto <sergio@serjux.com> - 6.4.1-1
- New upstream vesion, 6.4.1

* Sun Aug 28 2016 Sérgio Basto <sergio@serjux.com> - 6.2.0-3
- Initial version of freeworld

* Fri Jul 08 2016 Sérgio Basto <sergio@serjux.com> - 6.2.0-2
- Package review and fix mlt-ruby installation

* Wed May 25 2016 Sérgio Basto <sergio@serjux.com> - 6.2.0-1
- Update MLT to 6.2.0
- Drop backport patch.

* Sun Feb 21 2016 Sérgio Basto <sergio@serjux.com> - 6.0.0-2
- Add license tag.
- More spec modernizations and rpmlint fixes.
- Configure conditional build for Ruby.
- Remove old BuilRequires that aren't needed anymore.
- Remove old config options (avformat-swscale and qimage-libdir) that no longer
  exist in configure.
- Fix Ruby build.

* Fri Feb 19 2016 Sérgio Basto <sergio@serjux.com> - 6.0.0-1
- Update 6.0.0 (This is a bugfix and minor enhancement release. Note that our
  release versioning scheme has changed. We were approaching 1.0 but decided to
  synchronize release version with the C library ABI version, which is currently
  at v6)
- Switch to qt5 to fix rfbz #3810 and copy some BRs from Debian package.

* Wed Nov 18 2015 Sérgio Basto <sergio@serjux.com> - 0.9.8-1
- Update MLT to 0.9.8

* Mon May 11 2015 Sérgio Basto <sergio@serjux.com> - 0.9.6-2
- Workaround #3523

* Thu May 07 2015 Sérgio Basto <sergio@serjux.com> - 0.9.6-1
- Update mlt to 0.9.6 .
- Added BuildRequires of libexif-devel .

* Thu May 07 2015 Sérgio Basto <sergio@serjux.com> - 0.9.2-4
- Added BuildRequires of opencv-devel, rfbz #3523 .

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.9.2-3
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.9.2-2
- Rebuilt for FFmpeg 2.4.x

* Mon Sep 15 2014 Sérgio Basto <sergio@serjux.com> - 0.9.2-1
- New upstream release.

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-6
- Rebuilt for ffmpeg-2.3

* Sat Jul 26 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-5
- Rebuild for new php, need by mlt-php

* Sun Mar 30 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-4
- Rebuilt for ffmpeg-2.2 and fix for freetype2 changes.

* Wed Dec 04 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-3
- Update License tag .

* Wed Nov 20 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-2
- Enable gplv3 as asked in rfbz #3040
- Fix a changelog date.
- Fix Ruby warning with rpmbuild "Use RbConfig instead of obsolete and deprecated Config".
- Remove obsolete tag %%clean and rm -rf

* Mon Oct 07 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-1
- Update to 0.9.0

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-7
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-6
- Rebuilt for FFmpeg 2.0.x

* Mon Jun 10 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.8-5
- mlt-ruby FTBFS, omit until fixed (#2816)

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-4
- Rebuilt for x264/FFmpeg

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Feb 1  2013 Ryan Rix <ry@n.rix.si> - 0.8.8-1
- Fix ABI requirement to Ruby 1.9

* Fri Feb 1  2013 Ryan Rix <ry@n.rix.si> - 0.8.8-1
- Update to 0.8.8

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.6-2
- Rebuilt for ffmpeg

* Sun Dec 30 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.6-1
- Update to 0.8.6

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-3
- Rebuilt for FFmpeg 1.0

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-2
- Rebuilt for FFmpeg

* Tue Jun 19 2012 Richard Shaw <hobbes1069@gmail.com> - 0.8.0-1
- Update to latest upstream release.

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 0.7.8-3
- fix filter

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 0.7.8-2
- update PHP requirement for PHP Guildelines
- add php extension configuration file
- filter php private shared so

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-1
- 0.7.8

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-8
- rebuild (sox)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-7
- Rebuilt for c++ ABI breakage

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-6
- Rebuilt for x264/FFmpeg

* Fri Jan 27 2012 Ryan Rix <ry@n.rix.si> 0.7.6-5
- Include patch to fix building on gcc47 (upstreaming)

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Ryan Rix <ry@n.rix.si> 0.7.6-3
- s/%%[?_isa}/%%{?_isa}

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-2
- rebuild

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-1
- 0.7.6
- track files/sonames closer
- tighten subpkg deps via %%{?_isa}
- drop dup'd %%doc items

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-2
- Rebuilt for ffmpeg-0.8

* Thu Jul 21 2011 Ryan Rix <ry@n.rix.si> - 0.7.4-1
- New upstream

* Sun Apr 10 2011 Ryan Rix <ry@n.rix.si> - 0.7.0-2
- Add SDL_image-devel BR per Kdenlive wiki page

* Thu Apr 7 2011 Ryan Rix <ry@n.rix.si> - 0.7.0-1
- New upstream

* Tue Dec 21 2010 Ryan Rix <ry@n.rix.si> - 0.5.4-2
- Fix build, needed a patch from mlt's git repo.

* Sat Nov 20 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.5.4-1.1
- rebuilt - was missing in repo

* Wed Apr 21 2010 Ryan Rix <ry@n.rix.si> - 0.5.4-1
- New upstream version to fix reported crashes against Kdenlive

* Fri Feb 19 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-2
- disabled xine module for PPC arch.

* Thu Feb 18 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-1
- new version

* Wed Dec 09 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.10-1
- new version
- added subpackage for ruby

* Wed Oct 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.6-1
- new version
- added subpackages for: python, PHP

* Mon Sep 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.4-1
- new version
- renamed melt binary to mlt-melt

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.2-1
- new version
- removed obsolete patches

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-3
- added linker and license patches
- set license of MLT devel subpackage to LGPLv2+ 

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-2
- some PPC clearing

* Mon May 18 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-1
- update to 0.4.0

* Wed May 13 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-2
- spec cleaning

* Mon May 11 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-1
- new release
- MLT++  is now a part of this package

* Fri May  8 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-3
- unused-direct-shlib-dependency fix

* Fri Apr 17 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-2
- spec clearing
- added patches for resolving broken lqt-config, lib64 and execstack

* Wed Apr 15 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-1
- New release

* Thu Apr  9 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-3
- Enabled MMX support (not for PPC & PPC64)
- include demo files
- some spec cosmetics

* Thu Mar 12 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-2
- Change URL address
- devel Requires: pkgconfig

* Fri Feb 20 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.3.6-1
- Update to 0.3.6

* Wed Nov  5 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.1-0.1.svn1180
- update to upstream r1180
- add --avformat-swscale configure option

* Tue Nov  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.0-5
- rebuilt with proper qt4 paths

* Mon Oct 13 2008 jeff <moe@blagblagblag.org> - 0.3.0-4
- Build without fomit-frame-pointer ffmath
- Add BuildRequires: prelink
- clear-execstack libmltgtk2.so
- Don't strip binaries
- Group: Development/Libraries
- Prefix albino, humperdink, and miracle binaries with mlt-

* Sun Oct  5 2008 jeff <moe@blagblagblag.org> - 0.3.0-3
- License: GPLv2+ and LGPLv2+
- Group: Development/Tools
- ExcludeArch: x86_64 s390 s390x ppc ppc64
- %%defattr(-,root,root)
- %%doc docs/
- %%{_libdir}/%%{name} to main package


* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-2
- Change BuildRoot:
- Full source URL
- ExcludeArch: x86_64
- -devel Requires: pkgconfig, Requires: %%{name} = %%{version}-%%{release}

* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-1
- Update to 0.3.0
- --enable-gpl
- mlt-filehandler.patch

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f10
- Build for blaghead

* Mon Jul  7 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f9
- Update to svn r1155
- Remove sox-st.h.patch
- Add configure --disable-sox as it breaks build

* Sun Nov 11 2007 jeff <moe@blagblagblag.org> - 0.2.4-0blag.f7
- Update to 0.2.4
- Clean up spec

* Sat Jun 23 2007 jeff <moe@blagblagblag.org> - 0.2.3-0blag.f7
- Update to 0.2.3

* Sat Dec 30 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc6
- Rebuild for 60k
- Remove --disable-sox
- Add mlt-0.2.2-sox-st.h.patch

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc5
- Update to 0.2.2

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.1-0blag.fc5
- BLAG'd
- Removed "olib" from path, name, etc.
- Add changelog
- Update summary/description

