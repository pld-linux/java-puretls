%define		beta	b4
Summary:	Java implementation of SSLv3 and TLSv1
Summary(pl.UTF-8):	Implementacja SSLv3 i TLSv1 w Javie
Name:		puretls
Version:	0.9
Release:	0.%{beta}.1
License:	BSD-like
Group:		Development/Languages/Java
Source0:	http://www.mirrors.wiretapped.net/security/cryptography/libraries/tls/puretls/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	b2e4e947af30387b86dbf3473fdbd103
URL:		http://www.rtfm.com/puretls/
BuildRequires:	ant
BuildRequires:	cryptix
BuildRequires:	cryptix-asn1 = 0.20011119
BuildRequires:	java-gnu-getopt
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
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}a.

%prep
%setup -q -n %{name}-%{version}%{beta}
find -type f | \
	xargs grep -l "/usr/local/bin/perl5" | \
	xargs sed -i -e "s|/usr/local/bin/perl5|/usr/bin/perl|g;"
find -type f | \
	xargs grep -l "/usr/local/bin/perl" | \
	xargs sed -i -e "s|/usr/local/bin/perl|/usr/bin/perl|g;"

%build
required_jars="cryptix cryptix-asn1 gnu-getopt"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
export LC_ALL=en_US # source code not US-ASCII

%ant \
	-Djdk.version=%{jdkversion} \
	clean compile

%ant \
	javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_datadir}/%{name}}

cp build/%{name}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

cp build/%{name}demo.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-demo.jar
cp *.pem $RPM_BUILD_ROOT%{_datadir}/%{name}
cp test.pl $RPM_BUILD_ROOT%{_datadir}/%{name}

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT INSTALL LICENSE README
%{_javadir}/*.jar
%{_datadir}/%{name}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
