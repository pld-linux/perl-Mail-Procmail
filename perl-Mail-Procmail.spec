#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define		pdir	Mail
%define		pnam	Procmail
%include	/usr/lib/rpm/macros.perl
Summary:	Mail::Procmail - Procmail-like facility for creating easy mail filters
Name:		perl-%{pdir}-%{pnam}
Version:	1.08
Release:	1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	4a8d3c3d90553a98f702c851c27be320
Patch0:		%{name}-modify_headers.patch
URL:		http://search.cpan.org/dist/%{pdir}-%{pnam}/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-LockFile-Simple
BuildRequires:	perl-MailTools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
procmail is a great mail filter program, but it has weird recipe
format. It's pattern matching capabilities are basic and often
insufficient. I wanted something flexible whereby I could filter my
mail using the power of Perl.

I've been considering to write a procmail replacement in Perl for a
while, but it was Simon Cozen's Mail::Audit module, and his article in
The Perl Journal #18, that set it off.

I first started using Simon's great module, and then decided to write
my own since I liked certain things to be done differently. And I
couldn't wait for his updates.

Mail::Procmail allows a piece of email to be logged, examined,
delivered into a mailbox, filtered, resent elsewhere, rejected, and so
on. It is designed to allow you to easily create filter programs to
stick in a .forward or .procmailrc file, or similar.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%{perl_vendorlib}/%{pdir}/*.pm
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
