#
# TODO:
#	- external cudd
#	- update all BRs
#
Summary:	New Symbolic Model Verifier
Summary(pl.UTF-8):   Nowy weryfikator modeli symbolicznych
Name:		NuSMV
Version:	2.4.0
Release:	0.1
License:	LGPL
Group:		Applications
Source0:	http://nusmv.irst.itc.it/distrib/%{name}-%{version}.tar.gz
# Source0-md5:	cd1328fc70e9f48d2c4a96c0b8eb5a28
Patch0:		%{name}-build.patch
URL:		http://nusmv.irst.itc.it/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	ghostscript
BuildRequires:	lynx
# alternative for lynx
#BuildRequires:	links
BuildRequires:	perl-base
BuildRequires:	readline-devel
BuildRequires:	tetex-dvips
BuildRequires:	tetex-makeindex
BuildRequires:	tetex-latex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary(pl.UTF-8):   Pliki nagłówkowe NuSMV
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for NuSMV.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe NuSMV.

%package static
Summary:	Static NuSMV library
Summary(pl.UTF-8):   Statyczna biblioteka NuSMV
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static NuSMV library.

%description static -l pl.UTF-8
Statyczna biblioteka NuSMV.

%prep
%setup -q
%patch0 -p1

%build
cd nusmv
mkdir -p src/{sa/{fmea,stsa},mbp,mathsat}
touch src/sa/Makefile.in src/sa/fmea/Makefile.in src/sa/stsa/Makefile.in \
	src/mbp/Makefile.in src/mathsat/Makefile.in

%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	--enable-psl
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C nusmv install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a nusmv/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
%attr(755,root,root) %{_libdir}/libnusmv*.so.*.*.*
%dir %{_datadir}/nusmv
%{_datadir}/nusmv/contrib
%{_datadir}/nusmv/help
%{_datadir}/nusmv/master.nusmvrc
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnusmv*.so
%{_libdir}/libnusmv*.la
%{_includedir}/cudd*
%{_includedir}/nusmv
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnusmv*.a
