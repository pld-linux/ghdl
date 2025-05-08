#
# Conditional build:
%bcond_without	llvm	# LLVM-JIT backend instead of mcode
%bcond_with	nonfree	# full IEEE library, but not GPL-compatible

Summary:	Open-source analyzer, compiler, simulator and synthesizer for VHDL
Summary(pl.UTF-8):	Analizator, kompilator, symulator i syntezator VHDL o otwartych źródłach
Name:		ghdl
Version:	5.0.1
Release:	1
License:	GPL v2, CC-BY-SA v4.0, other
Group:		Applications
#Source0Download: https://github.com/ghdl/ghdl/releases
Source0:	https://github.com/ghdl/ghdl/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	344ee6f1c8164ec5aa2930f13902b355
URL:		http://ghdl.free.fr/
BuildRequires:	gcc-ada >= 6:8.1
%{?with_llvm:BuildRequires:	llvm-devel >= 6.0}
%{?with_llvm:BuildRequires:	llvm-devel < 20}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GHDL is the open-source analyzer, compiler, simulator and
(experimantal) synthesizer for VHDL, a Hardware Description Language.

%description -l pl.UTF-8
GHDL to mający otwarte źródła analizator, kompilator, symulator i
(eksperymentalny) syntezator VHDL - języka opisu sprzętu.

%package devel
Summary:	Header files for GHDL libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek GHDL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GHDL libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek GHDL.

%package static
Summary:	Static GHDL library
Summary(pl.UTF-8):	Biblioteka statyczna GHDL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GHDL library.

%description static -l pl.UTF-8
Biblioteka statyczna GHDL.

%prep
%setup -q

%{__sed} -i -e '1s, /usr/bin/env bash,/bin/bash,' scripts/vendors/*.sh

%build
# not autoconf configure
./configure \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	--prefix=%{_prefix} \
	--libdir=%{_lib} \
	%{__enable_disable nonfree gplcompat} \
	%{?with_llvm:--with-llvm-jit} \
	--with-readline

# TODO: --with-sundials (BR: libsundials_ida)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ghdl/vendors/*.{psm1,ps1}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS.md README.md
%attr(755,root,root) %{_bindir}/ghdl
%attr(755,root,root) %{_bindir}/ghwdump
%attr(755,root,root) %{_libdir}/libghdl-5_0_1.so
%attr(755,root,root) %{_libdir}/libghdlvpi.so
%attr(755,root,root) %{_libdir}/libghw.so
%dir %{_libdir}/ghdl
%{_libdir}/ghdl/ansi_color.sh
%{_libdir}/ghdl/ieee
%{_libdir}/ghdl/src
%{_libdir}/ghdl/std
%dir %{_libdir}/ghdl/vendors
%attr(755,root,root) %{_libdir}/ghdl/vendors/compile-*.sh
%attr(755,root,root) %{_libdir}/ghdl/vendors/filter.analyze.sh
%doc %{_libdir}/ghdl/vendors/README.md
%{_libdir}/ghdl/vendors/config.sh
%{_libdir}/ghdl/vendors/shared.sh

%files devel
%defattr(644,root,root,755)
%{_libdir}/libghdl.link
%{_includedir}/ghdl

%files static
%defattr(644,root,root,755)
%{_libdir}/libghdl.a
