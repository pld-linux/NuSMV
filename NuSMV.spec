#
# Conditional build:
%bcond_with	zchaff	# enable zChaff SAT Solver (zChaff is for non-commercial purposes only)
#
%define	zchaff_ver	2008.10.12
%define minisat_ver	070721
#
Summary:	New Symbolic Model Verifier
Summary(pl.UTF-8):	Nowy weryfikator modeli symbolicznych
Name:		NuSMV
Version:	2.5.4
Release:	11
License:	LGPL
Group:		Applications
Source0:	http://nusmv.fbk.eu/distrib/%{name}-%{version}.tar.gz
# Source0-md5:	4d8ae6136fbd916d875cd48f82d5f327
Source1:	http://minisat.se/downloads/minisat2-%{minisat_ver}.zip
# Source1-md5:	fb12db9a13f86a2133758abfba239546
Source2:	http://www.princeton.edu/~chaff/zchaff/zchaff.%{zchaff_ver}.zip
# Source2-md5:	7398b3e984a5046755cb3ef6b0e44d2e
Patch0:		%{name}-build.patch
Patch1:		%{name}-solvers.patch
Patch2:		format-security.patch
Patch3:		fork.patch
URL:		http://nusmv.fbk.eu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	ghostscript
BuildRequires:	lynx
# alternative for lynx
#BuildRequires:	links
BuildRequires:	perl-base
BuildRequires:	readline-devel
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-bibtex
BuildRequires:	texlive-latex-carlisle
BuildRequires:	texlive-latex-extend
BuildRequires:	texlive-latex-psnfss
BuildRequires:	texlive-makeindex
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# a lot of inter-library deps confusing install_post_check_so
%define		no_install_post_check_so	1

%description
NuSMV is a reimplementation and extension of SMV, the first model
checker based on BDDs. NuSMV has been designed to be an open
architecture for model checking, which can be reliably used for the
verification of industrial designs, as a core for custom verification
tools, as a testbed for formal verification techniques, and applied
to other research areas.

NuSMV2, combines BDD-based model checking component that exploits the
CUDD library developed by Fabio Somenzi at Colorado University and
SAT-based model checking component that includes an RBC-based Bounded
Model Checker, connected to the SIM SAT library developed by the
University of Genova.

%description -l pl.UTF-8
NuSVM to reimplementacja i rozszerzenie SMV - pierwszego weryfikatora
modeli opartego na BDD. NuSMV został zaprojektowany w otwartej
architekturze sprawdzania modeli, przez co może być niezawodnie
używany do weryfikacji projektów przemysłowych, jako podstawa własnych
narzędzi weryfikujących, jako poligon dla technik weryfikacji
formalnej oraz stosowany w innych obszarach badań.

NuSMV2 łączy komponent sprawdzający modele oparty na BDD,
wykorzystujący bibliotekę CUDD stworzoną przez Fabio Somenziniego w
Colorado University i komponent sprawdzający modele oparty na SAT
zawierający weryfikator modeli ograniczonych oparty na RBC, połączony
z biblioteką SIM SAT stworzoną przez University of Genova.

%package devel
Summary:	Header files for NuSMV
Summary(pl.UTF-8):	Pliki nagłówkowe NuSMV
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for NuSMV.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe NuSMV.

%package static
Summary:	Static NuSMV library
Summary(pl.UTF-8):	Statyczna biblioteka NuSMV
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static NuSMV library.

%description static -l pl.UTF-8
Statyczna biblioteka NuSMV.

%prep
%setup -q
install %{SOURCE1} MiniSat/
cd MiniSat
unzip -q *.zip
cd ..
install %{SOURCE2} zchaff/

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
ICFLAGS="%{rpmcflags} -fPIC"
export ICFLAGS

cd MiniSat/
OPTFLAGS="%{rpmcxxflags} -fPIC" COPTIMIZE="%{rpmcxxflags} -fPIC" ./build.sh
%if %{with zchaff}
cd ../zchaff
OPTFLAGS="%{rpmcxxflags} -fPIC" ./build.sh
%endif
cd ../cudd-*
%ifarch %{x8664}
cp -f Makefile Makefile_32bit
cp -f Makefile_64bit Makefile
%endif
%{__make}
cd ..

cd nusmv

%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-shared \
	%{?with_zchaff:--enable-zchaff} \
	--enable-minisat

%{__make}

%{__make} -j1 docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -j1 -C nusmv install \
	INSTALL_DATA="cp -a" \
	INSTALL_HEADER="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

cp -a nusmv/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/nusmv/{doc,examples,LGPL*,NEWS,README*}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc nusmv/{AUTHORS,ChangeLog,NEWS,README*}
%doc nusmv/doc/tutorial/tutorial.p*
%doc nusmv/doc/user-man/nusmv.p*
%doc nusmv/doc/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*smv*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*smv*.so.0
%attr(755,root,root) %{_libdir}/librbcdag.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librbcdag.so.0
%dir %{_datadir}/nusmv
%{_datadir}/nusmv/contrib
%{_datadir}/nusmv/help
%{_datadir}/nusmv/master.nusmvrc
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*smv*.so
%attr(755,root,root) %{_libdir}/librbcdag.so
%{_includedir}/cudd*
%{_includedir}/nusmv
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*smv*.a
%attr(755,root,root) %{_libdir}/librbcdag.a
