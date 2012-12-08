%define major 6
%define libname %mklibname esmtp %{major}
%define develname %mklibname esmtp -d

%define plugindir %{_libdir}/esmtp%{major}-plugins

Summary:	SMTP client library
Name:		libesmtp
Version:	1.0.6
Release:	6
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.stafford.uklinux.net/libesmtp/
Source0:	ttp://www.stafford.uklinux.net/libesmtp/%{name}-%{version}.tar.gz
Patch0:		libesmtp-build.patch
BuildRequires:	pkgconfig(openssl)
BuildRequires:	libltdl-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool

%description
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim. It may be used as part of a Mail User Agent (MUA) or another
program that must be able to post electronic mail but where mail
functionality is not the program's primary purpose.

%package -n	%{libname}
Summary:	%{summary}
Group:		%{group}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim. It may be used as part of a Mail User Agent (MUA) or another
program that must be able to post electronic mail but where mail
functionality is not the program's primary purpose.


%package -n	%{develname}
Summary:	Headers and development libraries for libESMTP
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim.

The libesmtp-devel package contains headers and development libraries
necessary for building programs against libesmtp.

%prep
%setup -q
%patch0 -p1 -b .build

%build
rm -f configure
libtoolize --copy --force; aclocal; autoconf; autoheader; automake --gnu --add-missing --copy

if pkg-config openssl ; then
    export CFLAGS="$CFLAGS %{optflags} `pkg-config --cflags openssl`"
    export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I openssl`"
    export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi

%configure2_5x \
    --with-auth-plugin-dir=%{plugindir} \
    --enable-pthreads \
    --enable-require-all-recipients \
    --enable-etrn \
    --enable-ntlm \
    --disable-static

%make

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/libesmtp-config

%files -n %{libname}
%doc AUTHORS COPYING* ChangeLog NEWS Notes README TODO
%{_libdir}/libesmtp.so.%{major}*
%{plugindir}

%files -n %{develname}
%{multiarch_bindir}/libesmtp-config
%{_bindir}/libesmtp-config
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-5mdv2011.0
+ Revision: 661956
- bump release

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-4
+ Revision: 661458
- mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-2mdv2011.0
+ Revision: 627617
- don't force the usage of automake1.7

* Wed Aug 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-1mdv2011.0
+ Revision: 568983
- 1.0.6

* Thu Apr 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.0.4-8mdv2010.1
+ Revision: 533277
- rebuild for openssl-1.0.0

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-7mdv2010.1
+ Revision: 519021
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0.4-6mdv2010.0
+ Revision: 425537
- rebuild

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-5mdv2009.1
+ Revision: 315573
- rebuild

* Tue Aug 26 2008 Emmanuel Andry <eandry@mandriva.org> 1.0.4-4mdv2009.0
+ Revision: 276360
- apply devel policy
- fix license
- check major

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.0.4-3mdv2009.0
+ Revision: 222540
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.0.4-2mdv2008.1
+ Revision: 150556
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Nov 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1mdv2007.0
+ Revision: 86137
- Import libesmtp

* Wed Nov 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1mdv2007.1
- 1.0.4
- fix deps
- use the %%mkrel macro
- new P0 from fedora extras
- rediffed P0

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.3r1-3mdk
- added P0,P1 from fedora
- reconstruct the autotools

* Wed Mar 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.3r1-2mdk
- fix deps and conditional %%multiarch

* Sun Aug 22 2004 Abel Cheung <deaddog@mandrake.org> 1.0.3r1-1mdk
- New version

* Wed Jan 28 2004 Abel Cheung <deaddog@deaddog.org> 1.0.2-1mdk
- New version

