
%bcond_without	javadoc		# don't build javadoc

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname		puretls
%define		beta	b5
%define		rel		4
Summary:	Java implementation of SSLv3 and TLSv1
Summary(pl.UTF-8):	Implementacja SSLv3 i TLSv1 w Javie
Name:		java-puretls
Version:	0.9
Release:	0.%{beta}.%{rel}
License:	BSD-like
Group:		Libraries/Java
Source0:	%{srcname}-%{version}%{beta}.tar.gz
# Source0-md5:	f14690ef749f21dc3b98a7293191fff3
URL:		http://www.rtfm.com/puretls/
BuildRequires:	ant
BuildRequires:	java-cryptix >= 3.2.0
BuildRequires:	java-cryptix-asn1 = 0.20011119
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	java-cryptix >= 3.2.0
Requires:	java-cryptix-asn1 = 0.20011119
Provides:	puretls
Obsoletes:	puretls
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		jdkversion	1.4

%description
PureTLS is a free Java-only implementation of the SSLv3 and TLSv1
(RFC2246) protocols. PureTLS was developed by Eric Rescorla for
Claymore Systems, Inc, but is being distributed for free because we
believe that basic network security is a public good and should be a
commodity.

%description -l pl.UTF-8
PureTLS to implementacja w samej Javie protokołów SSLv3 i TLSv1 (RFC
2246). PureTLS został stworzony przez Erica Rescorlę dla Claymore
Systems Inc., ale jest dystrybuowany za darmo, ponieważ właściciele
uznali, że podstawowe bezpieczeństwo sieci jest dobrem publicznym.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils
Provides:	puretls-javadoc
Obsoletes:	puretls-javadoc

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}%{beta}
find -type f | \
	xargs grep -l "/usr/local/bin/perl5" | \
	xargs sed -i -e "s|/usr/local/bin/perl5|/usr/bin/perl|g;"
find -type f | \
	xargs grep -l "/usr/local/bin/perl" | \
	xargs sed -i -e "s|/usr/local/bin/perl|/usr/bin/perl|g;"

# Disable test that uses proprietary SUN API
%if %{without java_sun}
mv src/COM/claymoresystems/provider/test/DSATest.java{,.disabled}
%endif

%build
required_jars="cryptix cryptix-asn1"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
export LC_ALL=en_US # source code not US-ASCII

%ant \
	-Djdk.version=%{jdkversion} \
	clean compile

%{?with_javadoc:%ant javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_javadir},%{_datadir}/%{name}}

cp build/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
ln -sf %{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar

cp build/%{srcname}demo.jar $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/%{srcname}-demo.jar
cp *.pem $RPM_BUILD_ROOT%{_datadir}/%{name}
cp test.pl $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{with javadoc}
# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr build/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT INSTALL LICENSE README
%{_javadir}/*.jar
%{_datadir}/%{name}
%{_examplesdir}/%{name}-%{version}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
