%define oname libESMTP
%define major	6
%define libname	%mklibname esmtp %{major}
%define devname	%mklibname esmtp -d
%define plugindir %{_libdir}/esmtp%{major}-plugins

Summary:	SMTP client library
Name:		libesmtp
Version:	1.1.0
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/libesmtp/libESMTP
Source0:	https://github.com/libesmtp/libESMTP/archive/refs/tags/v%{version}/%{oname}-%{version}.tar.gz

BuildRequires:	meson
BuildRequires:	libltdl-devel
BuildRequires:	pkgconfig(openssl)

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

%package -n	%{devname}
Summary:	Headers and development libraries for libESMTP
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The libesmtp-devel package contains headers and development libraries
necessary for building programs against libesmtp.

%prep
%setup -qn %{oname}-%{version}
%autopatch -p1

if pkg-config openssl ; then
	export CFLAGS="$CFLAGS %{optflags} `pkg-config --cflags openssl`"
	export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I openssl`"
	export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi

%build
%meson

%meson_build

%install
%meson_install

%files -n %{libname}
%{_libdir}/libesmtp.so.%{major}*
%{_libdir}/esmtp-plugins-*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libesmtp-1.0.pc
