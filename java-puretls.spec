%define		beta		b4

Name:		puretls
Version:	0.9
Release:	0.%{beta}.1
Summary:	Java implementation of SSLv3 and TLSv1
License:	BSD style
Group:		Development/Languages/Java
Source0:	http://www.mirrors.wiretapped.net/security/cryptography/libraries/tls/%{name}/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	b2e4e947af30387b86dbf3473fdbd103
URL:		http://www.rtfm.com/puretls
Requires:	cryptix
Requires:	cryptix-asn1 = 0.20011119
BuildRequires:	jakarta-ant
BuildRequires:	cryptix
BuildRequires:	cryptix-asn1 = 0.20011119
BuildRequires:	gnu.getopt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java
%define		jdkversion	1.4

%description
PureTLS is a free Java-only implementation of the SSLv3 and TLSv1
(RFC2246) protocols. PureTLS was developed by Eric Rescorla for Claymore
Systems, Inc, but is being distributed for free because we believe that
basic network security is a public good and should be a commodity.

%prep
%setup -q -n %{name}-%{version}%{beta}
#%patch
find . -type f |
    xargs grep -l "/usr/local/bin/perl5" | \
    xargs perl -pi -e "s|/usr/local/bin/perl5|/usr/bin/perl|g;"
find . -type f |
    xargs grep -l "/usr/local/bin/perl" | \
    xargs perl -pi -e "s|/usr/local/bin/perl|/usr/bin/perl|g;"

find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%build
ant \
    -Dcryptix.jar=%{_javalibdir}/cryptix.jar \
    -Dcryptix-asn1.jar=%{_javalibdir}/cryptix-asn1.jar \
    -Dgnugetopt.jar=%{_javalibdir}/gnu.getopt.jar \
    -Djdk.version=%{jdkversion} \
    clean compile
    
ant -Dcryptix.jar=%{_javalibdir}/cryptix.jar \
    -Dcryptix-asn1.jar=%{_javalibdir}/cryptix-asn1.jar \
    -Dgnugetopt.jar=%{_javalibdir}/gnu.getopt.jar \
    javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp build/%{name}.jar $RPM_BUILD_ROOT%{_javalibdir}
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javalibdir}/%{name}-%{version}.jar

cp build/%{name}demo.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-demo.jar
cp *.pem $RPM_BUILD_ROOT%{_datadir}/%{name}
cp test.pl $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT INSTALL LICENSE README build/doc/*
%{_javalibdir}/*.jar
%{_datadir}/%{name}
