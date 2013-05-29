%define major	6
%define libname	%mklibname esmtp %{major}
%define devname	%mklibname esmtp -d
%define plugindir %{_libdir}/esmtp%{major}-plugins

Summary:	SMTP client library
Name:		libesmtp
Version:	1.0.6
Release:	6
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.stafford.uklinux.net/libesmtp/
Source0:	ttp://www.stafford.uklinux.net/libesmtp/%{name}-%{version}.tar.gz
Patch0:		libesmtp-build.patch
Patch1:		libesmtp-automake-1.13.patch
BuildRequires:	libtool
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
%setup -q
%apply_patches

rm -f configure
libtoolize --copy --force; aclocal; autoconf; autoheader; automake --gnu --add-missing --copy

if pkg-config openssl ; then
	export CFLAGS="$CFLAGS %{optflags} `pkg-config --cflags openssl`"
	export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I openssl`"
	export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi

%build
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
%{_libdir}/libesmtp.so.%{major}*
%{plugindir}

%files -n %{devname}
%doc AUTHORS COPYING* ChangeLog NEWS Notes README TODO
%{multiarch_bindir}/libesmtp-config
%{_bindir}/libesmtp-config
%{_includedir}/*
%{_libdir}/*.so

