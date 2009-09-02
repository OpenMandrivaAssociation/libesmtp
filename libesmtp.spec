%define major 5
%define libname	%mklibname esmtp %{major}
%define develname %mklibname esmtp -d

%define plugindir %{_libdir}/esmtp%{major}-plugins

Summary:	SMTP client library
Name:		libesmtp
Version:	1.0.4
Release:	%mkrel 6
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.stafford.uklinux.net/libesmtp/
Source0:	ttp://www.stafford.uklinux.net/libesmtp/%{name}-%{version}.tar.bz2
Patch0:		libesmtp-build.patch
Patch1:		libesmtp-ssl.diff
BuildRequires:	openssl-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	libltdl-devel
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Obsoletes:	%{name}

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
Obsoletes:	%{libname}-devel

%description -n	%{develname}
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim.

The libesmtp-devel package contains headers and development libraries
necessary for building programs against libesmtp.

%prep 

%setup -q
%patch0 -p1 -b .build
%patch1 -p0 -b .ssl

%build
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf; autoheader; automake-1.7 --gnu --add-missing --copy

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
    --enable-ntlm

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# remove unneeded files
rm -f %{buildroot}%{plugindir}/*.a

%multiarch_binaries %{buildroot}%{_bindir}/libesmtp-config

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog NEWS Notes README TODO
%{_libdir}/libesmtp.so.%{major}*
%{plugindir}

%files -n %{develname}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/libesmtp-config
%{_bindir}/libesmtp-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


