%bcond_without	javadoc		# don't build javadoc

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include	/usr/lib/rpm/macros.java

%define		srcname		puretls
%define		beta	b4
Summary:	Java implementation of SSLv3 and TLSv1
Summary(pl.UTF-8):	Implementacja SSLv3 i TLSv1 w Javie
Name:		puretls
Version:	0.9
Release:	0.%{beta}.1
License:	BSD-like
Group:		Libraries/Java
Source0:	http://www.mirrors.wiretapped.net/security/cryptography/libraries/tls/puretls/%{srcname}-%{version}%{beta}.tar.gz
# Source0-md5:	b2e4e947af30387b86dbf3473fdbd103
URL:		http://www.rtfm.com/puretls/
BuildRequires:	ant
BuildRequires:	java-cryptix
BuildRequires:	java-cryptix-asn1 = 0.20011119
#BuildRequires:	java-gnu-getopt
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	cryptix
Requires:	cryptix-asn1 = 0.20011119
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

cp build/%{srcname}demo.jar $RPM_BUILD_ROOT%{_examplesdir}/%{name}/%{srcname}-demo.jar
cp *.pem $RPM_BUILD_ROOT%{_datadir}/%{srcname}
cp test.pl $RPM_BUILD_ROOT%{_datadir}/%{srcname}

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
