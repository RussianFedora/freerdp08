%define rname freerdp

Name:           freerdp08
Version:        0.8.2
Release:        1%{?dist}
Summary:        Remote Desktop Protocol client

Group:          Applications/Communications
License:        GPLv2+
URL:            http://www.freerdp.com/
Source0:        http://downloads.sourceforge.net/freerdp/freerdp-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel
BuildRequires:  cups-devel
BuildRequires:  openssl-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel

Provides:       xfreerdp = %{version}-%{release}

%description 
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

FreeRDP is a fork of the rdesktop project and intends to rapidly
improve on it and re-implement what is needed.


%package        libs
Summary:        Core libraries implementing the RDP protocol
Group:          System Environment/Libraries
%description    libs
libfreerdp implements the core of the RDP protocol.

libfreerdpchanman can be used to load plugins that can handle channels
in the RDP protocol.

libfreerdpkbd implements functionality for handling keyboards in X.

%prep
%setup -q -n freerdp-%{version}


%build
%configure --disable-static --with-sound=alsa --with-crypto=openssl
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files libs
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/ipv6.txt ChangeLog
%{_libdir}/*.so.*
%dir %{_libdir}/%{rname}/
%{_datadir}/%{rname}/
%exclude %{_bindir}/xfreerdp
%exclude %{_mandir}/*/*
%exclude %{_libdir}/%{rname}/*.so
%exclude %{_includedir}/*
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig/%{rname}.pc


%changelog
* Mon Apr 23 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 0.8.2-1.R
- only libs

* Tue Nov 16 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.2-1
- freerdp-0.8.2
 
* Mon Nov 08 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.1-2
- make -devel require pkgconfig
- first official Fedora package

* Sun Nov 07 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.1-1
- freerdp-0.8.1

* Sat Sep 25 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-2
- hack the generated libtool to not set rpath on x86_64
- configure with alsa explicitly

* Tue Aug 24 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-1
- freerdp-0.7.4
- cleanup of packaging structure

* Wed Jul 28 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.3-1
- 0.7.3
- fix some minor pylint warnings

* Fri Jul 23 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.2-2
- 0.7.2
- Address many comments from cwickert:
- - cleanup of old formatting, alignment with spectemplate-lib.spec and
    cwickert spec from #616193
- - add alsa as build requirement
- - remove superfluous configure options and disable static libs
- - add missing rpm groups

* Sun Jun 13 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.0-1
- First official release, first review request
